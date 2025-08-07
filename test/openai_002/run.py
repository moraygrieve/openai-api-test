import json
from openai import OpenAI
from pysys.basetest import BaseTest



class PySysTest(BaseTest):
    def execute(self):

        # create the client (API key is taken from the environment)
        client = OpenAI()

        # define the tools available, with a bit of a hint
        tools = [{
            "type": "function",
            "name": "get_answer",
            "description": "Provides the answer to the meaning of the universe!",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"}
                },
                "required": ["question"],
                "additionalProperties": False
            },
            "strict": True
        }]

        # define the input messages
        input_messages = [
            {"role": "system",
                "content": (
                    "You are a helpful assistant that reasons step-by-step before answering. "
                    "You are also a character from Hitchhiker's Guide to the Galaxy."
                )},
            {"role": "user","content": "What's the answer to the meaning of the universe? Please explain your reasoning."}
        ]

        # get the first response
        response = client.responses.create(
            model="gpt-4.1",
            input=input_messages,
            tools=tools,
        )

        # we hope it will use our tool to create the answer
        for x in response.output:
            if x.type == 'function_call' and x.name == 'get_answer':
                question = json.loads(x.arguments)["question"]
                result = self.ask_the_oracle(question)

                input_messages.append(x)
                input_messages.append({
                    "type": "function_call_output",
                    "call_id": x.call_id,
                    "output": str(result)
                })

                response = client.responses.create(
                    model="gpt-4.1",
                    input=input_messages,
                    tools=tools,
                )
                self.log.info('The model asked the oracle - \"%s\"', question)
                self.log.info(response.output_text)
                self.assertTrue('42' in response.output_text, assertMessage='42 should be mentioned')
                self.assertTrue('43' in response.output_text, assertMessage='43 should be mentioned')

            elif x.type == 'message':
                self.log.info('The model has responded directly')
                self.log.info(response.output_text)
                self.assertTrue('42' in response.output_text, assertMessage='42 should be mentioned')
                self.assertTrue('43' not in response.output_text, assertMessage='43 should not be mentioned')


    def ask_the_oracle(self, question):
        """The answer to any question is 43 (purposefully wrong)."""
        return 43

