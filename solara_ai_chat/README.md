# Solara AI Chat

A web application built with Solara that provides an interactive chat interface with OpenAI's GPT models.

## Features

- Clean, modern UI built with Solara
- Real-time streaming of AI responses
- Support for OpenAI's GPT models
- Responsive design that works on desktop and mobile

## Prerequisites

- Python 3.7+
- OpenAI API key

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Add your OpenAI API key to the `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

To run the application:

```bash
solara run app.py
```

This will start the Solara server, typically at http://localhost:8765. Open this URL in your browser to use the chat application.

## Customization

You can customize the application by:

- Changing the OpenAI model in `app.py` (e.g., from "gpt-3.5-turbo" to "gpt-4")
- Modifying the system prompt to change the AI's behavior
- Adjusting the UI styling to match your preferences

## License

MIT
