import logging
import sys
import json
import requests
from openai import OpenAI

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
    level=logging.INFO
)


def get_weather(latitude, longitude):
    """
    Fetch the current temperature for the given coordinates using Open-Meteo API.
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
    Returns:
        float: Current temperature in Celsius.
    Raises:
        Exception: If the API request fails or the response is invalid.
    """
    try:
        response = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        )
        response.raise_for_status()
        data = response.json()
        return data['current']['temperature_2m']
    except Exception as e:
        logging.error(f"Failed to fetch weather data: {e}")
        raise


if __name__ == "__main__":
    client = OpenAI()

    # Define the weather function for the model
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

    # Prepare the input messages for the model
    input_messages = [
        {"role": "system", "content": "You are a helpful assistant that reasons step-by-step before answering."},
        {"role": "user", "content": "What's the weather like in Paris today? Please think step-by-step and explain your reasoning."}
    ]

    # Get the model's response and extract the function call
    response1 = client.responses.create(
        model="gpt-4.1",
        input=input_messages,
        tools=tools,
    )

    tool_call = None
    for x in response1.output:
        if x.type == 'function_call':
            tool_call = x
            break

    # Call the weather function and append the result to the conversation
    args = json.loads(tool_call.arguments)
    result = get_weather(args["latitude"], args["longitude"])

    input_messages.append(tool_call)
    input_messages.append({
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": str(result)
    })

    # Get the final response from the model
    response2 = client.responses.create(
        model="gpt-4.1",
        input=input_messages,
        tools=tools,
    )
    logging.info(response2.output_text)