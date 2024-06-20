# llm-chat-logger

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

I've always found that using the web GUI for gemini/openai is useful for generating responses but does not allow for searching through past conversations or easy sharing with others. This project aims to provide a simple CLI tool to log conversations with OpenAI or Gemini LLMs and save the output as markdown files for convenient reading and sharing. Additionally, the tool allows for easy integration with your favorite LLM API to generate responses and provides context and instructions to the AI model for more accurate responses.

## Features

- CLI tool to log conversations with OpenAI or Gemini LLMs
- Save output as markdown files for convenient reading and sharing
- Integrate with your favorite LLM API to generate responses
- Provide context and instructions to the AI model for more accurate responses
  - Context markdown files saved in prompts/ folder
  - Inspired by patterns found in https://github.com/danielmiessler/fabric

## Installation

### Prerequisites

- Python 3.8 or higher
- Pip
- OpenAI or Gemini LLM API key

### Clone the Repository

```bash
git clone https://github.com/aday913/llm-chat-logger.git
cd llm-chat-logger
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Create a copy of the .env-template file and rename it to .env. Fill in the required values, namely the API key of whichever llm you want to use and the default output path of your output markdown files.

## Usage

By default, the program will use GPT-4o as the AI model and save the output markdown file as the current datetime (YYYYMMDD-HHMMSS).md in the .env's default directory output folder. If this is desired, simply run the following command:
```bash
python main.py
```

If you would like to specify the AI model or output file name, you can use the following command:
```bash
python main.py --model gemini --output my-output-file.md
```

You will be prompted for an input with a colon ":" symbol. When you are ready for your input to be sent to the AI model, simply press enter 3 times. The AI model will then generate a response that will be printed on screen. Continue this process until you are finished with the conversation. When finished, either type "exit" or "quit" as an input, and the conversation will end. The output will be saved as a markdown file.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (git checkout -b feature/your-feature)
3. Commit your changes (git commit -m 'Add some feature')
4. Push to the branch (git push origin feature/your-feature)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, send me a message or submit a GitHub issue.
