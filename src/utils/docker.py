import docker, select, time
import asyncio, threading

class DockerShell:

    def __init__(self, image="ubuntu"):
        """Initialize a docker container with a non-interactive shell."""
        self.client = docker.from_env()

    def wait_container(self, container, timeout=10):
        """Wait for a container to be running."""
        start = time.time()
        container.reload()
        while container.status != 'running':
            if (time.time() - start) > timeout:
                raise Exception('Timed out waiting %d secs for container to be running'%timeout)
            time.sleep(0.5)
            container.reload()

    def close(self):
        """Close a running container cleanly."""
        try:
            self.container.stop(timeout=1)
            self.container.remove(force=True)
        except Exception:
            pass

    def __del__(self):
        """Ensure container is closed cleanly on object deletion."""
        self.close()

class DockerNonInteractiveShell(DockerShell):

    def __init__(self, image="ubuntu"):
        """Initialize a docker container with a non-interactive shell."""
        super().__init__(image)
        self.container = self.client.containers.run(image, command="bash", tty=False, stdin_open=True, detach=True)

    def run(self, command):
        """Execute a shell command inside the running Docker container (new shell). """
        result = self.container.exec_run("bash -c \'%s\'" % command)
        result = result.output.decode().strip()
        return result.splitlines()

    def close(self):
        """Close a running container cleanly."""
        try:
            self.container.stop(timeout=1)
            self.container.remove(force=True)
        except Exception:
            pass

    def __del__(self):
        """Ensure container is closed cleanly on object deletion."""
        self.close()


class DockerInteractiveShell(DockerShell):

    def __init__(self, image="ubuntu"):
        """ Initialize a Docker container with an interactive shell session."""
        super().__init__(image)
        self.container = self.client.containers.run(image, command=["bash", "-c", "export PS1=''; exec sh"],
            tty=False, stdin_open=True, detach=True, )
        self.sock = self.container.attach_socket(params={"stdin": 1, "stdout": 1, "stream": 1})
        self.sock._sock.setblocking(False)

    def run(self, command, timeout=5):
        """ Execute a shell command inside the running Docker container. """
        full_cmd = f"{command}\n"
        self.sock._sock.send(full_cmd.encode())

        buffer = b""
        deadline = time.time() + timeout

        header = False
        while time.time() < deadline:
            rlist, _, _ = select.select([self.sock._sock], [], [], 0.1)
            if rlist:
                if not header:
                    self.sock._sock.recv(8)
                    header = True

                chunk = self.sock._sock.recv(4096)
                if not chunk: break
                buffer += chunk
            else:
                time.sleep(0.01)

        output = buffer.decode(errors="ignore")
        return output.splitlines()

    def close(self):
        """Close a running container cleanly."""
        try:
            self.sock._sock.close()
        except Exception as e:
            pass
        try:
            self.container.stop(timeout=1)
            self.container.remove(force=True)
        except Exception:
            pass

class DockerAsynchronousShell(DockerShell):

    def __init__(self, image="ubuntu"):
        """Initialize a docker container with a non-interactive shell."""
        super().__init__(image)
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self._future = None
        self.container = self.client.containers.run(image, command="bash", tty=False, stdin_open=True, detach=True)

    def run(self, command, timeout=5):
        if self._future is None or self._future.done():
            self._future = asyncio.run_coroutine_threadsafe(self._run_command(command), self._loop)

    def poll_done(self):
        return self._future is not None and self._future.done()

    def get_result(self):
        if self.poll_done():
            return self._future.result()
        return None

    async def _run_command(self, command):
        result = self.container.exec_run("bash -c \'%s\'" % command)
        result = result.output.decode().strip()
        return result.splitlines()

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()
