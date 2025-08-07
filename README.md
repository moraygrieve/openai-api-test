# OpenAI API Test

A Python project for experimenting with the OpenAI API, featuring examples and automated testing using PySys.

## Features
- **Weather Assistant**: Uses OpenAI's function calling to answer weather-related questions with real-time data from Open-Meteo API
- **Automated Testing**: PySys-based test framework for validating OpenAI API and Docker responses
- **Modular Examples**: Organized code structure for easy extension and experimentation

## Project Structure
```
openai-api-test/
├── src/
│   └── examples/
│       └── weather.py      # Weather assistant with function calling
├── test/
│   ├── openai_001/        # PySys test for OpenAI API validation
│   │   ├── run.py         # Test implementation
│   │   ├── pysystest.xml  # Test configuration
│   │   └── Output/        # Test output directory
│   └── docker_001/        # PySys test for Docker API validation
│       ├── run.py         # Test implementation
│       ├── pysystest.xml  # Test configuration
│       └── Output/        # Test output directory
├── pysysproject.xml       # PySys project configuration
└── README.md
```

## Requirements
- Python 3.11+
- `openai` Python package
- `requests` Python package
- `docker` Python package (for Docker tests)
- `pysys` Python package (for testing)

## Setup
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd openai-api-test
   ```

2. **Install dependencies:**
   ```bash
   pip install openai requests docker pysys
   ```

3. **Set up OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **(Optional) Set up Docker:**
   Ensure Docker is installed and running for Docker-based tests.

## Usage

### Running Examples

**Weather Assistant:**
```bash
python src/examples/weather.py
```
This example demonstrates OpenAI's function calling feature to:
- Parse natural language weather queries
- Extract location coordinates from user input
- Call the Open-Meteo API to fetch current weather data
- Provide formatted responses with temperature and weather details

### Running Tests

**Execute all PySys tests:**
```bash
pysys run
```

**Run specific test:**
```bash
pysys run openai_001
pysys run docker_001
```

- The OpenAI test validates that the OpenAI API correctly responds to a specific prompt about the answer to the universe and asserts the expected answer (42).
- The Docker test validates that Docker containers can be started, interacted with, and produce the expected output.

## How it Works

### Weather Assistant
The weather assistant uses OpenAI's function calling feature to:
1. Parse natural language weather queries
2. Extract location information and convert to coordinates
3. Call the Open-Meteo API to fetch current weather data
4. Provide formatted responses with temperature, conditions, and other weather details

### Testing Framework
The project uses PySys for automated testing:
- Validates OpenAI API and Docker responses
- Asserts expected outcomes
- Provides detailed logging and output capture
- Supports multiple test modes and configurations

## API Dependencies
- **OpenAI API**: For natural language processing and function calling (requires API key)
- **Open-Meteo API**: For free weather data (no API key required)
- **Docker**: For container-based tests (requires Docker to be installed)

## Customization
- Modify examples in `src/examples/` to experiment with different OpenAI API features
- Add new PySys tests in `test/` directory for additional validation
- Extend function calling capabilities by adding new API integrations
- Customize test configurations in `pysysproject.xml`

## License
MIT
