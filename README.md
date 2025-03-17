# Solara AI Data Analysis

A modern, responsive data analysis application with AI chat capabilities built with Solara and integrated with OpenAI's GPT models.

## Features

- Clean, modern UI with a slide-out chat panel
- Integration with OpenAI's GPT-3.5 Turbo model
- Responsive design that works on various screen sizes
- Smooth animations and transitions
- Prompt suggestions to help users get started with data analysis

## Requirements

- Python 3.8+
- Solara 1.14.0+
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/solara_ai_data_analysis.git
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
python -m solara_ai_chat.app
```

Then open your browser to `http://localhost:8765` to view the application.

## Project Structure

- `solara_ai_chat/app.py`: Main application code
- `solara_ai_chat/__init__.py`: Package initialization
- `.env`: Environment variables (not tracked by Git)
- `requirements.txt`: Project dependencies

## License

MIT
