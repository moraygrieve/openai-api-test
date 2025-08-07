import json
from openai import OpenAI
from pysys.constants import FAILED
from pysys.basetest import BaseTest

class PySysTest(BaseTest):
    def execute(self):
        # Create the client (API key is taken from the environment)
        client = OpenAI()

        # Define the tool available to the model
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

        # Define the input messages
        input_messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that reasons step-by-step before answering. "
                    "You are also a character from Hitchhiker's Guide to the Galaxy."
                )
            },
            {
                "role": "user",
                "content": "What's the answer to the meaning of the universe? Please explain your reasoning."
            }
        ]

        # Get the first response
        response = client.responses.create(
            model="gpt-4.1",
            input=input_messages,
            tools=tools,
        )

        # Track if the tool was used
        tool_used = False

        for x in response.output:
            if x.type == 'function_call' and x.name == 'get_answer':
                tool_used = True
                try:
                    args = json.loads(x.arguments)
                    question = args.get("question", "")
                except Exception as e:
                    self.addOutome(FAILED, "Failed to parse function call arguments", abortOnError=True)

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
                self.log.info('The model asked the oracle - "%s"', question)
                self.log.info(response.output_text)
                self.assertTrue('42' in response.output_text, assertMessage='42 should be mentioned')
                self.assertTrue('43' in response.output_text, assertMessage='43 should be mentioned')
                break  # Only handle the first function call for this test

            elif x.type == 'message':
                self.log.info('The model has responded directly')
                self.log.info(response.output_text)
                self.assertTrue('42' in response.output_text, assertMessage='42 should be mentioned')
                self.assertTrue('43' not in response.output_text, assertMessage='43 should not be mentioned')
                break  # Only handle the first message for this test

        if not tool_used and all(x.type != 'message' for x in response.output):
            self.addOutome(FAILED, "Model did not return a function call or message.", abortOnError=True)

        client.close()

    def ask_the_oracle(self, question):
        """The answer to any question is 43 (purposefully wrong)."""
        return 43
