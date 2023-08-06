"""
FiftyOne Services.

| Copyright 2017-2020, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import itertools
import logging
import multiprocessing
import os
import re
import subprocess
import sys

from packaging.version import Version
import psutil
import requests
from retrying import retry

import eta.core.utils as etau

import fiftyone.constants as foc


logger = logging.getLogger(__name__)


class ServiceException(Exception):
    """Base class for service-related exceptions."""

    pass


class ServiceListenTimeout(ServiceException):
    """Exception raised when a network-bound service fails to bind to a port."""

    def __init__(self, name, port=None):
        self.name = name
        self.port = port

    def __str__(self):
        message = "%s failed to bind to port" % self.name
        if self.port is not None:
            message += " " + str(self.port)
        return message


class Service(object):
    """Interface for FiftyOne services.

    All services must define a ``command`` property.

    Services are run in an isolated Python subprocess (see ``_service_main.py``)
    to ensure that they are shut down when the main Python process exits. The
    ``command`` and ``working_dir`` properties control the execution of the
    service in the subprocess.
    """

    working_dir = "."
    allow_headless = False

    def __init__(self):
        """Creates (starts) the Service."""
        self._system = os.system
        self._disabled = (
            os.environ.get("FIFTYONE_SERVER", False)
            or os.environ.get("FIFTYONE_DISABLE_SERVICES", False)
            or multiprocessing.current_process().name != "MainProcess"
            or (
                os.environ.get("FIFTYONE_HEADLESS", False)
                and not self.allow_headless
            )
        )
        self.child = None
        if not self._disabled:
            self.start()

    def __del__(self):
        """Deletes (stops) the Service."""
        if not self._disabled:
            try:
                self.stop()
            except:
                # something probably failed due to interpreter shutdown, which
                # will be handled by _service_main.py
                pass

    @property
    def command(self):
        raise NotImplementedError("subclasses must define `command`")

    def start(self):
        """Starts the Service."""
        service_main_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "_service_main.py",
        )
        # use psutil's Popen wrapper because its wait() more reliably waits
        # for the process to exit on Windows
        self.child = psutil.Popen(
            [sys.executable, service_main_path] + self.command,
            cwd=self.working_dir,
            stdin=subprocess.PIPE,
        )

    def stop(self):
        """Stops the Service."""
        self.child.stdin.close()
        self.child.wait()

    def wait(self):
        """Waits for the Service to exit and returns its exit code."""
        return self.child.wait()

    def _wait_for_child_port(self, port=None, timeout=10):
        """
        Waits for any child process of this service to bind to a TCP port.

        Args:
            port: if specified, wait for a child to bind to this port
            timeout: the number of seconds to wait before failing

        Returns:
            the port the child has bound to (equal to the ``port`` argument
            if specified)

        Raises:
            ServiceListenTimeout: if the timeout was exceeded
        """

        @retry(
            wait_fixed=250,
            stop_max_delay=timeout * 1000,
            retry_on_exception=lambda e: isinstance(e, ServiceListenTimeout),
        )
        def find_port():
            child_connections = itertools.chain.from_iterable(  # flatten
                child.connections(kind="tcp")
                for child in self.child.children(recursive=True)
            )
            for conn in child_connections:
                if (
                    not conn.raddr  # not connected to a remote socket
                    and conn.status == psutil.CONN_LISTEN
                ):
                    local_port = conn.laddr[1]
                    if port is None or port == local_port:
                        return local_port
            raise ServiceListenTimeout(etau.get_class_name(self), port)

        return find_port()


class DatabaseService(Service):
    """Service that controls the underlying MongoDB database."""

    allow_headless = True

    MONGOD_EXE_NAME = "mongod"
    if sys.platform.startswith("win"):
        MONGOD_EXE_NAME += ".exe"

    MIN_MONGO_VERSION = "3.6"

    @property
    def command(self):
        return [
            DatabaseService.find_mongod(),
            "--dbpath",
            foc.DB_PATH,
            "--logpath",
            foc.DB_LOG_PATH,
        ]

    def start(self):
        """Starts the DatabaseService."""
        for folder in (foc.DB_PATH, os.path.dirname(foc.DB_LOG_PATH)):
            if not os.path.isdir(folder):
                os.makedirs(folder)

        super().start()

        # Set up a default connection
        import fiftyone.core.odm as foo

        foo.get_db_conn()

        # Drop non-persistent datasets
        import fiftyone.core.dataset as fod

        fod.delete_non_persistent_datasets()

    @staticmethod
    def find_mongod():
        """Returns the path to the `mongod` executable."""
        search_paths = [
            foc.FIFTYONE_DB_BIN_DIR,
            os.path.join(foc.FIFTYONE_CONFIG_DIR, "bin"),
        ] + os.environ["PATH"].split(os.pathsep)
        searched = set()
        attempts = []
        for folder in search_paths:
            if folder in searched:
                continue
            searched.add(folder)
            mongod_path = os.path.join(folder, DatabaseService.MONGOD_EXE_NAME)
            if os.path.isfile(mongod_path):
                ok, out, err = etau.communicate([mongod_path, "--version"])
                out = out.decode(errors="ignore").strip()
                err = err.decode(errors="ignore").strip()
                mongod_version = None
                if ok:
                    match = re.search(r"db version.+?([\d\.]+)", out, re.I)
                    if match:
                        mongod_version = match.group(1)
                        if Version(mongod_version) >= Version(
                            DatabaseService.MIN_MONGO_VERSION
                        ):
                            return mongod_path
                attempts.append((mongod_path, mongod_version, err))
        for path, version, err in attempts:
            if version is not None:
                logger.warn("%s: incompatible version %s" % (path, version))
            else:
                logger.error("%s: failed to launch: %s" % (path, err))
        raise RuntimeError(
            "Could not find mongod >= %s" % DatabaseService.MIN_MONGO_VERSION
        )


class ServerService(Service):
    """Service that controls the FiftyOne web server."""

    working_dir = foc.SERVER_DIR
    allow_headless = True

    def __init__(self, port):
        self._port = port
        super().__init__()

    def start(self):
        server_version = None
        try:
            server_version = requests.get(
                "http://127.0.0.1:%i/fiftyone" % self._port, timeout=2
            ).json()["version"]
        except Exception:
            pass

        if server_version is None:
            # There is likely not a fiftyone server running (remote or local),
            # so start a local server. If there actually is a fiftyone server
            # running that didn't respond to /fiftyone, the local server will
            # fail to start but the app will still connect successfully.
            super().start()
            self._wait_for_child_port(self._port)
        else:
            logger.info("Connected to fiftyone on local port %i" % self._port)
            if server_version != foc.VERSION:
                logger.warn(
                    "Server version (%s) does not match client version (%s)"
                    % (server_version, foc.VERSION)
                )

    @property
    def command(self):
        command = [
            sys.executable,
            "main.py",
            "--port",
            str(self.port),
        ]
        return command

    @property
    def port(self):
        """Getter for the current port"""
        return self._port


class AppService(Service):
    """Service that controls the FiftyOne app."""

    working_dir = foc.FIFTYONE_APP_DIR

    @property
    def command(self):
        with etau.WorkingDir(foc.FIFTYONE_APP_DIR):
            if os.path.isfile("FiftyOne.AppImage"):
                # Linux
                args = ["./FiftyOne.AppImage"]
            elif os.path.isdir("FiftyOne.app"):
                # macOS
                args = ["./FiftyOne.app/Contents/MacOS/FiftyOne"]
            elif os.path.isfile("FiftyOne.exe"):
                # Windows
                args = ["./FiftyOne.exe"]
            elif os.path.isfile("package.json"):
                # dev build
                args = ["yarn", "dev"]
            else:
                raise RuntimeError(
                    "Could not find FiftyOne app in %r" % foc.FIFTYONE_APP_DIR
                )
        return args
