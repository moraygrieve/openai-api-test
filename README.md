# OpenAI API Test

A Python project for experimenting with the OpenAI API and weather data integration.

## Features
- Uses OpenAI's function calling to answer weather-related questions.
- Fetches real-time weather data from the Open-Meteo API.
- Modular code structure with packages for easy extension.

## Project Structure
```
src/
├── hello/
│   ├── __init__.py
│   └── hello_world.py
└── weather/
    ├── __init__.py
    └── weather.py
```

## Requirements
- Python 3.11 (recommended: `/opt/homebrew/opt/python@3.11/bin/python3.11`)
- `openai` Python package
- `requests` Python package

## Setup
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd openai-api-test
   ```
2. **(Optional) Create a virtual environment:**
   ```bash
   /opt/homebrew/opt/python@3.11/bin/python3.11 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install openai requests
   ```

## Usage
To run the weather assistant example:
```bash
python src/weather/weather.py
```

This will use OpenAI's function calling to answer a weather question and fetch real-time data for the requested location.

## Customization
- Modify `src/weather/weather.py` to change the prompt or add new tools.
- Add new packages in `src/` for additional experiments.

## License
MIT