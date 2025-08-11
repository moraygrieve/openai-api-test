import docker, select, time

class DockerShell:

    def wait_container(self, container, timeout=10):
        """Wait for a container to be running."""
        start = time.time()
        container.reload()
        while container.status != 'running':
            if (time.time() - start) > timeout:
                raise Exception('Timed out waiting %d secs for container to be running'%timeout)
            time.sleep(0.5)
            container.reload()


class DockerNonInteractiveShell(DockerShell):

    def __init__(self, image="ubuntu"):
        """Initialize a docker container with a non-interactive shell."""
        self.client = docker.from_env()
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
        self.client = docker.from_env()
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

    def __del__(self):
        """Ensure container is closed cleanly on object deletion."""
        self.close()
