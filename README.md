# OpenAI API Test

A Python project for experimenting with the OpenAI API, featuring examples and automated testing using PySys.

## Features
- **Automated Testing**: PySys-based test framework for validating OpenAI API and Docker responses
- **Modular Examples**: Organized code structure for easy extension and experimentation

## Project Structure
```
openai-api-test/
├── README.md
├── pysysproject.xml
├── src
│   └── utils        # Utility classes
└── test
    ├── docker_001   # Docker tests
    ├── docker_002
    ├── openai_001   # OpenAI tests
    ├── openai_002
    └── openai_003
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

## How it Works

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
- Add new PySys tests in `test/` directory for additional validation
- Extend function calling capabilities by adding new API integrations
- Customize test configurations in `pysysproject.xml`

## License
MIT
