####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

import click
import docker

from pathlib import Path
from shutil import rmtree
from os import remove as remove_file
from os import rename
from time import sleep
from sys import platform
from subprocess import call
from sqlalchemy import inspect

from wilfred.database import session, Server, EnvironmentVariable
from wilfred.keyboard import KeyboardThread
from wilfred.container_variables import ContainerVariables
from wilfred.api.images import Images
from wilfred.errors import WilfredException, WriteError


class ServerNotRunning(WilfredException):
    """Server is not running"""


class Servers(object):
    def __init__(
        self, docker_client: docker.DockerClient, configuration: dict, images: Images
    ):
        """
        Initiates wilfred.api.Servers, method for controlling servers

        Args:
            docker_client (docker.DockerClient): DockerClient object from Docker module
            configuration (dict): Dictionary of Wilfred config
            images (Images): wilfred.api.Images object
        """

        self._images = images
        self._configuration = configuration
        self._docker_client = docker_client

    def all(self, cpu_load=False, memory_usage=False):
        """
        Returns data of all servers

        Args:
            cpu_load (bool): Include the CPU load of the container. Defaults to `None` if server is not running.
            memory_usage (bool): Include RAM usage of the container. Defaults to `None` if server is not running.
        """

        servers = [
            {c.key: getattr(u, c.key) for c in inspect(u).mapper.column_attrs}
            for u in session.query(Server).all()
        ]

        for server in servers:
            if cpu_load or memory_usage:
                for server in servers:
                    _running = True

                    try:
                        container = self._docker_client.containers.get(
                            f"wilfred_{server['id']}"
                        )
                        d = container.stats(stream=False)
                    except docker.errors.NotFound:
                        server.update({"cpu_load": "-"})
                        server.update({"memory_usage": "-"})
                        _running = False
                    except Exception:
                        server.update({"cpu_load": "error"})
                        server.update({"memory_usage": "error"})
                        _running = False

                    if cpu_load and _running:
                        cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
                        cpu_percent = 0.0
                        cpu_delta = float(
                            d["cpu_stats"]["cpu_usage"]["total_usage"]
                        ) - float(d["precpu_stats"]["cpu_usage"]["total_usage"])
                        system_delta = float(
                            d["cpu_stats"]["system_cpu_usage"]
                        ) - float(d["precpu_stats"]["system_cpu_usage"])
                        if system_delta > 0.0:
                            cpu_percent = f"{round(cpu_delta / system_delta * 100.0 * cpu_count)}%"

                        server.update({"cpu_load": cpu_percent if cpu_percent else "-"})

                    if memory_usage and _running:
                        server.update(
                            {
                                "memory_usage": f"{round(d['memory_stats']['usage'] / 10**6)} MB"
                            }
                        )

        return servers

    def set_status(self, server, status):
        server.status = status
        session.commit()

    def sync(self):
        """
        Performs sync, checks for state of containers
        """

        for server in session.query(Server).all():
            if server.status == "installing":
                try:
                    self._docker_client.containers.get(f"wilfred_{server.id}")
                except docker.errors.NotFound:
                    self.set_status(server, "stopped")

            # stopped
            if server.status == "stopped":
                self._stop(server)

            # start
            if server.status == "running":
                try:
                    self._docker_client.containers.get(f"wilfred_{server.id}")
                except docker.errors.NotFound:
                    self._start(server)

    def remove(self, server: Server):
        """
        Removes specified server

        Args:
            server (wilfred.database.Server): Server database object
        """

        path = f"{self._configuration['data_path']}/{server.name}_{server.id}"

        for x in (
            session.query(EnvironmentVariable).filter_by(server_id=server.id).all()
        ):
            session.delete(x)

        session.delete(server)
        session.commit()

        try:
            container = self._docker_client.containers.get(f"wilfred_{server.id}")
            container.kill()
        except docker.errors.NotFound:
            pass

        rmtree(path, ignore_errors=True)

    def console(self, server: Server, disable_user_input=False):
        """
        Enters server console

        Args:
            server (wilfred.database.Server): Server database object
            disable_user_input (bool): Blocks user input if `True`. By default this is `False`.

        Raises:
            :py:class:`ServerNotRunning`
                If server is not running
        """

        try:
            container = self._docker_client.containers.get(f"wilfred_{server.id}")
        except docker.errors.NotFound:
            raise ServerNotRunning(f"server {server.id} is not running")

        if platform.startswith("win"):
            click.echo(container.logs())
            call(["docker", "attach", container.id])
        else:
            if not disable_user_input:
                KeyboardThread(self._console_input_callback, params=server)

            try:
                for line in container.logs(stream=True, tail=200):
                    click.echo(line.strip())
            except docker.errors.NotFound:
                raise ServerNotRunning(f"server {server.id} is not running")

    def install(self, server: Server, skip_wait=False, spinner=None):
        """
        Performs installation

        Args:
            server (wilfred.database.Server): Server database object
            skip_wait (bool): Doesn't stall while waiting for server installation to complete if `True`.
            spinner (Halo): If `Halo` spinner object is defined, will then write and perform actions to it.

        Raises:
            :py:class:`WriteError`
                If not able to create directory or write to it
        """

        path = f"{self._configuration['data_path']}/{server.name}_{server.id}"
        image = self._images.get_image(server.image_uid)

        if platform.startswith("win"):
            path = path.replace("/", "\\")

        try:
            Path(path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise WriteError(f"could not create server data directory, {str(e)}")

        with open(f"{path}/install.sh", "w", newline="\n") as f:
            f.write("cd /server\n" + "\n".join(image["installation"]["script"]))

        if spinner:
            spinner.info(
                "Pulling Docker image and creating installation container, do not exit"
            )
            spinner.start()

        self._docker_client.containers.run(
            image["installation"]["docker_image"],
            f"{image['installation']['shell']} /server/install.sh",
            volumes={path: {"bind": "/server", "mode": "rw"}},
            name=f"wilfred_{server.id}",
            environment=ContainerVariables(server, image, install=True).get_env_vars(),
            remove=True,
            detach=True,
        )

        if skip_wait and spinner:
            spinner.info(
                "Installation will continue in background, use `wilfred servers` to see if process has finished."
            )
            spinner.start()

        if not skip_wait:
            if spinner:
                spinner.info(
                    "You can safely press CTRL+C, the installation will continue in the background."
                )
                spinner.info(
                    "Run `wilfred servers` too see when the status changes from `installing` to `stopped`."
                )
                spinner.info(
                    f"You can also follow the installation log using `wilfred console {server.name}`"
                )
                spinner.start()
            while self._container_alive(server):
                sleep(1)

    def kill(self, server):
        """
        Kills server container

        Args:
            server (wilfred.database.Server): Server database object

        Raises:
            :py:class:`ServerNotRunning`
                If server is not running
        """

        try:
            container = self._docker_client.containers.get(f"wilfred_{server.id}")
        except docker.errors.NotFound:
            raise ServerNotRunning(f"server {server.id} is not running")

        container.kill()

    def rename(self, server, name):
        """
        Renames server and moves server folder

        Args:
            server (wilfred.database.Server): Server database object
            name (str): New name of the server

        Raises:
            :py:class:`WilfredException`
                If server is running
            :py:class:`WriteError`
                If not able to move folder
        """

        if self._container_alive(server):
            raise WilfredException("You cannot rename the server while it is running")

        try:
            rename(
                f"{self._configuration['data_path']}/{server.name}_{server.id}",
                f"{self._configuration['data_path']}/{name}_{server.id}",
            )
        except Exception as e:
            raise WriteError(f"could not rename folder, {str(e)}")

        server.name = name
        session.commit()

    def _console_input_callback(self, payload, server):
        self.command(server, payload)

    def command(self, server, command):
        """
        Sends command to server console

        Args:
            server (wilfred.database.Server): Server database object
            command (str): The command to send to the stdin of the server

        Raises:
            :py:class:`ServerNotRunning`
                If server is not running
        """

        _cmd = f"{command}\n".encode("utf-8")

        try:
            container = self._docker_client.containers.get(f"wilfred_{server.id}")
        except docker.errors.NotFound:
            raise ServerNotRunning(f"server {server.id} is not running")

        s = container.attach_socket(params={"stdin": 1, "stream": 1})
        s.send(_cmd) if platform.startswith("win") else s._sock.send(_cmd)
        s.close()

    def _running_docker_sync(self):
        for server in session.query(Server).all():
            try:
                self._docker_client.containers.get(f"wilfred_{server.id}")
            except docker.errors.NotFound:
                self.set_status(server, "stopped")

    def _parse_startup_command(self, cmd, server, image):
        return ContainerVariables(server, image).parse_startup_command(
            cmd.replace("{{SERVER_MEMORY}}", str(server.memory)).replace(
                "{{SERVER_PORT}}", str(server.port)
            )
        )

    def _container_alive(self, server):
        try:
            self._docker_client.containers.get(f"wilfred_{server.id}")
        except docker.errors.NotFound:
            return False

        return True

    def _start(self, server):
        path = f"{self._configuration['data_path']}/{server.name}_{server.id}"
        image = self._images.get_image(server.image_uid)

        try:
            remove_file(f"{path}/install.sh")
        except Exception:
            pass

        self._docker_client.containers.run(
            image["docker_image"],
            self._parse_startup_command(server.custom_startup, server, image)
            if server.custom_startup is not None
            else f"{self._parse_startup_command(image['command'], server, image)}",
            volumes={path: {"bind": "/server", "mode": "rw"}},
            name=f"wilfred_{server.id}",
            remove=True,
            ports={f"{server.port}/tcp": server.port},
            detach=True,
            working_dir="/server",
            mem_limit=f"{server.memory}m",
            oom_kill_disable=True,
            stdin_open=True,
            environment=ContainerVariables(server, image).get_env_vars(),
            user=image["user"] if image["user"] else "root",
        )

    def _stop(self, server):
        image = self._images.get_image(server.image_uid)

        try:
            container = self._docker_client.containers.get(f"wilfred_{server.id}")
        except docker.errors.NotFound:
            return

        if not image["stop_command"]:
            container.stop()

            return

        self.command(server, image["stop_command"])

        stopped = False

        while not stopped:
            try:
                self._docker_client.containers.get(f"wilfred_{server.id}")
            except docker.errors.NotFound:
                stopped = True
