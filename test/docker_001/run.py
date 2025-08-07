import time, docker
from pysys.constants import TIMEDOUT
from pysys.basetest import BaseTest

class PySysTest(BaseTest):

    def execute(self):
        client = docker.from_env()

        # Check running a container in the foreground (executes a task and dies)
        self.log.info('Check running a docker container in the foreground')
        result = client.containers.run("alpine", ["echo", "hello", "world"])
        result = result.decode().strip()
        self.log.info('Returned output is %s', result)
        self.assertTrue(result == 'hello world', assertMessage='Assert expected response')

        # Check running a container in the background (stays alive to allow command execution)
        self.log.info('Check running a docker container in the background')
        container = client.containers.run( "alpine", tty=True, stdin_open=True, command="sh", detach=True)
        try:
            self.wait_container(container)
            result = container.exec_run("echo 'hello world from inside the container'")
            result = result.output.decode().strip()
            self.log.info("Returned output is %s", result)
            self.assertTrue(result == 'hello world from inside the container', assertMessage='Assert expected response')
        finally:
            container.stop()
            container.remove()

    def wait_container(self, container, timeout=10):
        """Wait for a container to be running."""
        start = time.time()
        container.reload()
        while container.status != 'running':
            if (time.time() - start) > timeout:
                self.addOutcome(TIMEDOUT, 'Timed out waiting %d secs for container to be running'%timeout, abortOnError=True)
            time.sleep(0.5)
            container.reload()
