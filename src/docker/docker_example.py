import sys, docker, select, time, logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
    level=logging.INFO
)

class DockerInteractiveShell:

    def __init__(self, image="ubuntu"):
        self.client = docker.from_env()
        self.container = self.client.containers.run(
            image,
            command=["bash", "-c", "export PS1=''; exec sh"],
            tty=False,
            stdin_open=True,
            detach=True,
        )
        self.sock = self.container.attach_socket(params={"stdin": 1, "stdout": 1, "stream": 1})
        self.sock._sock.setblocking(False)

    def run(self, command, timeout=5):
        full_cmd = f"{command}\n"
        self.sock._sock.send(full_cmd.encode())

        buffer = b""
        deadline = time.time() + timeout

        result = []
        while time.time() < deadline:
            rlist, _, _ = select.select([self.sock._sock], [], [], 0.1)
            if rlist:
                chunk = self.sock._sock.recv(4096)
                if not chunk: break
                buffer += chunk
                output = buffer.decode(errors="ignore")
                result.extend(output.splitlines())
            else:
                time.sleep(0.01)

        return "\n".join(result).strip()

    def close(self):
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
        self.close()


if __name__ == "__main__":
    shell = DockerInteractiveShell()
    logging.info('Result: %s', shell.run("echo hello world"))
    logging.info('Result: %s', shell.run("export MYVAR=42"))
    logging.info('Result: %s', shell.run("echo $MYVAR"))
    logging.info('Result: %s', shell.run("pwd"))
    logging.info('Result: %s', shell.run("cd /home"))
    logging.info('Result: %s', shell.run("pwd"))
    logging.info('Result: %s', shell.run("ls -al"))
    shell.close()
