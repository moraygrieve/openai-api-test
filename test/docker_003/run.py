import time
from pysys.constants import TIMEDOUT
from pysys.basetest import BaseTest
from utils.docker import DockerFactory

class PySysTest(BaseTest):
    def execute(self):
        shell = DockerFactory.asynchronous()
        shell.run("sleep 10; echo hello world")

        start = time.time()
        while shell.poll_done() == False:
            self.log.info('Command has not yet completed ...')
            time.sleep(1)
            if (time.time() - start) > 20:
                self.addOutcome(TIMEDOUT, outcomeReason='Timedout waiting for docker response', abortOnError=True)
        result = shell.get_result()
        self.log.info('Result obtained: %s' % result)

        self.assertTrue(result[0]== 'hello world', assertMessage='Simple echo command')
        shell.close()


