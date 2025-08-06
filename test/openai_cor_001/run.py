from openai import OpenAI
from pysys.constants import *
from pysys.basetest import BaseTest

class PySysTest(BaseTest):
	def execute(self):

		# create the client and using gpt-4.1 request a response
		client = OpenAI()
		response = client.responses.create(
			model="gpt-4.1",
			input="Write a one-sentence bedtime story about a unicorn."
		)
	
		# log out the response
		self.log.info(response.output_text)

		# Assert that the response is not empty
		self.assertTrue(bool(response.output_text), "Response text should not be empty")

	