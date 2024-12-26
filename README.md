# AI Model Compare - AISuite UI

A web interface for testing and comparing responses from different Language Models using AISuite Library. This project provides a simple, intuitive way to experiment with multiple LLMs side by side.

![AI Model Compare UI Screenshot](https://github.com/lesteroliver911/ai-model-compare-aisuit/blob/main/lesteroliver-aisuit-ui-screenshot.png)

## Overview
This UI tool lets you:
- Compare responses from different AI models in real-time (openai, anthropic, groq)
- Adjust temperature settings for each request
- Customize system messages to control AI behavior
- View responses in a clean, parallel layout

## Built With
- [Streamlit](https://streamlit.io/) - For the web interface
- [AISuite](https://github.com/andrewyng/aisuite) - Andrew Ng's library for LLM integration
- Python 3.8+

## About AISuite
AISuite (by Andrew Ng) provides a standardized interface for interacting with multiple LLMs. It uses an OpenAI-like interface, making it easy to switch between different AI providers without changing your code. The library currently supports chat completions from providers like OpenAI, Anthropic, Groq, and more.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/lesteroliver911/ai-model-compare-aisuit.git
   cd ai-model-compare-aisuit
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_key
   ANTHROPIC_API_KEY=your_key
   GROQ_API_KEY=your_key
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Currently Integrated Models
- OpenAI: GPT-4o
- Anthropic: Claude 3.5 Sonnet
- Groq: LLaMA 3 8B

## Contributing
Feel free to fork this repository and submit pull requests. You can also add support for more models by updating the `models` list in the code.

## Credits
- AISuite Library by Andrew Ng - For making it simple to interact with multiple LLMs through a unified interface
- Streamlit - For the web framework

## License
MIT
