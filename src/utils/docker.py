import docker, select, time
import asyncio, threading

class DockerFactory:

    @classmethod
    def non_interactive(cls, image="ubuntu"):
        return DockerNonInteractiveShell(image)

    @classmethod
    def interactive(cls, image="ubuntu"):
        return DockerInteractiveShell(image)

    @classmethod
    def asynchronous(cls, image="ubuntu"):
        return DockerAsynchronousShell(image)


class DockerShell:

    def __init__(self, image):
        self.client = docker.from_env()
        self.cmd_whitelist = None

    def with_whitelist(self, commands):
        self.cmd_whitelist = commands
        return self

    def run(self, command):
        cmd = command.split()[0] # assume first word is always the command
        if self.cmd_whitelist is None: return
        if (cmd not in self.cmd_whitelist):
            raise Exception('Command is prohibited')


class DockerNonInteractiveShell(DockerShell):

    def __init__(self, image):
        super().__init__(image)
        self.container = self.client.containers.run(image, command="bash", tty=False, stdin_open=True, detach=True)

    def run(self, command):
        super().run(command)
        result = self.container.exec_run("bash -c \'%s\'" % command)
        result = result.output.decode().strip()
        return result.splitlines()

    def close(self):
        try:
            self.container.stop()
            self.container.remove(force=True)
        except Exception:
            pass

    def __del__(self):
        self.close()


class DockerInteractiveShell(DockerShell):

    def __init__(self, image):
        super().__init__(image)
        self.container = self.client.containers.run(image, command=["bash", "-c", "export PS1=''; exec sh"],
            tty=False, stdin_open=True, detach=True, )
        self.sock = self.container.attach_socket(params={"stdin": 1, "stdout": 1, "stream": 1})
        self.sock._sock.setblocking(False)

    def run(self, command, timeout=5):
        super().run(command)
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
        try:
            self.sock._sock.close()
        except Exception as e:
            pass

        try:
            self.container.stop()
            self.container.remove(force=True)
        except Exception:
            pass

    def __del__(self):
        self.close()


class DockerAsynchronousShell(DockerShell):

    def __init__(self, image):
        super().__init__(image)
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self._future = None
        self.container = self.client.containers.run(image, command="bash", tty=False, stdin_open=True, detach=True)

    def run(self, command):
        super().run(command)
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

    def close(self):
        try:
            self.container.stop()
            self.container.remove(force=True)
        except Exception as e:
            pass

        if self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join(timeout=2)

        if not self._loop.is_closed():
            self._loop.close()

    def __del__(self):
        self.close()


