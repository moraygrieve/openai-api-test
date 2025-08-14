# OpenAI API Test

A Python project for experimenting with the OpenAI API, with Docker utilities and automated testing using PySys.

## Features
- **Automated testing**: PySys-based test suite for OpenAI and Docker workflows
- **Docker utilities**: Reusable shells for non-interactive, interactive, and asynchronous container execution

## Project Structure
```
openai-api-test/
├── README.md
├── pysysproject.xml
├── src
│   └── utils
│       └── docker.py         # Docker shell helpers
└── test
    ├── docker_001            # Non-interactive shell tests
    ├── docker_002            # Interactive shell tests
    ├── docker_003            # Asynchronous shell tests
    ├── openai_001            # Basic OpenAI response test
    ├── openai_002            # Function-calling/tool-use test
    └── openai_003            # YAML-driven prompt test
```

## Requirements
- Python 3.8+ (matches `pysysproject.xml`)
- Python packages:
  - `openai`
  - `pysys`
  - `docker` (for Docker tests)
  - `PyYAML` (for `openai_003`)

## Setup
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd openai-api-test
   ```

2. **Install dependencies:**
   ```bash
   pip install openai pysys docker PyYAML
   ```

3. **Set up OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. Ensure Docker is installed and running (required for the Docker tests).

## Usage

### Running Tests

- Run all tests:
  ```bash
  pysys run
  ```

- Run a specific test:
  ```bash
  pysys run docker_001
  pysys run docker_002
  pysys run docker_003
  pysys run openai_001
  pysys run openai_002
  pysys run openai_003
  ```

## How it Works

### Testing Framework
The project uses PySys for automated testing:
- Validates OpenAI API and Docker responses
- Asserts expected outcomes
- Provides detailed logging and output capture
- Supports multiple test modes and configurations

## API Dependencies
- **OpenAI API**: Requires `OPENAI_API_KEY` in the environment for OpenAI tests
- **Docker**: Required and must be running to execute Docker tests

## Test Overview

- **docker_001 (Non-interactive shell)**: Executes single commands in a fresh shell each time (no persistent environment variables or working directory).
- **docker_002 (Interactive shell)**: Keeps a shell session open; environment variables and working directory persist across commands.
- **docker_003 (Asynchronous shell)**: Starts a long-running command and polls until completion, then captures the result.
- **openai_001**: Simple response sanity check using `gpt-4.1` and verifies the model returns `42`.
- **openai_002**: Demonstrates tool/function calling; handles both direct model responses and function-call paths.
- **openai_003**: Loads a prompt from YAML (`test/openai_003/Input/prompt.yaml`) and asserts the model avoids a deceptive answer.

## How it Works

- PySys configuration is defined in `pysysproject.xml` (adds `./src` to the path).
- Docker utilities live in `src/utils/docker.py` and provide:
  - `DockerNonInteractiveShell`
  - `DockerInteractiveShell`
  - `DockerAsynchronousShell`

## License
MIT
