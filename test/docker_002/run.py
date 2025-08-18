
from pysys.constants import *
from pysys.basetest import BaseTest
from utils.docker import DockerFactory

class PySysTest(BaseTest):
    def execute(self):
        shell = DockerFactory.interactive()
        self.assertTrue(shell.run("echo hello world")[0] == 'hello world', assertMessage='Simple echo command')
        self.assertTrue(shell.run("export MYVAR=42") == [], assertMessage='Export environment variable')
        self.assertTrue(shell.run("echo $MYVAR")[0] == '42', assertMessage='Echo back the environment variable')
        self.assertTrue(shell.run("pwd")[0] == '/', assertMessage='Print working directory')
        self.assertTrue(shell.run("cd /home") == [], assertMessage='Change working directory')
        self.assertTrue(shell.run("pwd")[0] == '/home', assertMessage='Print new working directory')
        shell.close()


