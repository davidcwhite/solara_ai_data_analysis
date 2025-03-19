# Solara AI Data Analysis

A modern, responsive data analysis application with AI chat capabilities built with Solara and integrated with OpenAI's GPT models.

## Features

- Clean, modern UI with a slide-out chat panel
- Integration with OpenAI's GPT models
- Responsive design that works on various screen sizes
- Smooth animations and transitions
- Prompt suggestions to help users get started with data analysis
- Real-time streaming of AI responses

## Requirements

- Python 3.8+
- Solara 1.14.0+
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/davidcwhite/solara_ai_data_analysis.git
cd solara_ai_data_analysis
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the application with:

```bash
solara run app.py
```

Then open your browser to `http://localhost:8765` to view the application.

## Customization

You can customize the application by:

- Changing the OpenAI model in `app.py` (e.g., from "gpt-3.5-turbo" to "gpt-4")
- Modifying the system prompt to change the AI's behavior
- Adjusting the UI styling to match your preferences

## Project Structure

- `app.py`: Main application code
- `.env`: Environment variables (not tracked by Git)
- `requirements.txt`: Project dependencies

## License

MIT
