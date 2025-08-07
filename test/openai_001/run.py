from openai import OpenAI
from pysys.basetest import BaseTest

class PySysTest(BaseTest):
    def execute(self):

        # create the client (API key is taken from the environment)
        client = OpenAI()

        # using gpt-4.1 make a request for a question where we assume a known answer
        input_messages = [
            {"role": "system", "content": "You are a character from Hitchhiker's Guide to the Galaxy."},
            {"role": "user", "content": "What's the answer to the meaning of the universe? Just give the number, no other characters."}
        ]
        response = client.responses.create(
            model="gpt-4.1",
            input=input_messages
        )

        # log out the response
        self.log.info('The answer to the universe is %s', response.output_text)

        # assert that the response is not empty
        self.assertTrue(int(response.output_text) == 42, assertMessage = "Assert the answer is correct")

        # close the client
        client.close()
