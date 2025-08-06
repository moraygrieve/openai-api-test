import requests, json, logging, sys
from openai import OpenAI

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', stream=sys.stdout, level=logging.INFO)


def get_weather(latitude, longitude):
    """Client side function to return weather."""
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']


if __name__ == "__main__":
    client = OpenAI()

    # make a definition of a weather function known to the model on the request
    tools = [{
        "type": "function",
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }]

    # start with a single input message that makes the request for the weather
    input_messages = [
    {"role": "system", "content": "You are a helpful assistant that reasons step-by-step before answering."},
    {"role": "user", "content": "What's the weather like in Paris today? Please think step-by-step and explain your reasoning."}
    ]

    response1 = client.responses.create(
        model="gpt-4.1",
        input=input_messages,
        tools=tools,
    )

    tool_call = None
    for x in response1.output:
        if x.type == 'function_call': tool_call = x

    # extract the models requested arguments to the function call, make the function call and store the result
    args = json.loads(tool_call.arguments)
    result = get_weather(args["latitude"], args["longitude"])

    # we now chain up the input message to include the full input (assumes determinism)
    input_messages.append(tool_call)
    input_messages.append({
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": str(result)
    })

    response2 = client.responses.create(
        model="gpt-4.1",
        input=input_messages,
        tools=tools,
    )
    logging.info(response2.output_text)