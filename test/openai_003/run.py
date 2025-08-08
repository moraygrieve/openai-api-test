import json, os
from openai import OpenAI
from pysys.basetest import BaseTest

class PySysTest(BaseTest):
    def execute(self):

        # Create the client (API key is taken from the environment)
        client = OpenAI()

        # Read in the input prompt from file and log out the response
        with open(os.path.join(self.input, 'prompt.json'), 'r') as f:
            input_messages = json.load(f)

        response = client.responses.create(
            model="gpt-4.1",
            input=input_messages
        )

        self.log.info('The models response was: %s', response.output_text)

        # Close the client
        client.close()
