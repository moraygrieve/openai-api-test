from pysys.constants import PASSED, FAILED
from pysys.basetest import BaseTest
from utils.docker import DockerFactory

class PySysTest(BaseTest):

    def execute(self):
        shell = DockerFactory.non_interactive().with_whitelist(['echo', 'export', 'pwd'])
        self.assertTrue(shell.run("echo hello world")[0] == 'hello world', assertMessage='Simple echo command')
        self.assertTrue(shell.run("export MYVAR=42") == [], assertMessage='Export environment variable')
        self.assertTrue(shell.run("echo $MYVAR") == [], assertMessage='Echo back the environment variable')
        self.assertTrue(shell.run("pwd")[0] == '/', assertMessage='Print working directory')

        try:
            shell.run("cd /home")
            self.addOutcome(FAILED)
        except Exception as e:
            self.log.warning('Attempt on restricted command detected')
            self.addOutcome(PASSED)

        self.assertTrue(shell.run("pwd")[0] == '/', assertMessage='Print working directory is still the same')


