# AI Dev Toolkit

A full-stack web application providing a suite of AI-powered tools for developers, using local language models for offline functionality.

## Features

- **Code Snippet Generator**: Generate code snippets from natural language descriptions
- **Code Debugger**: Debug and fix buggy code with AI assistance
- **Code Explainer**: Get plain English explanations of complex code
- **Unit Test Generator**: Automatically generate pytest unit tests for your code
- **Code Translator**: Translate code between programming languages
- **Regex Generator**: Generate regex patterns from descriptions
- **Natural Language to SQL**: Convert natural language queries to SQL
- **Markdown to HTML Previewer**: Convert markdown to HTML with live preview

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Hugging Face Transformers with GPT-2 (local, offline)

## Installation

1. Clone or download the project files.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. (Optional) Set up environment variables by copying `.env.example` to `.env` and modifying as needed.

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Select a tool from the tabs at the top of the page.
2. Fill in the required fields for the selected tool.
3. Click the submit button to process your request.
4. View the AI-generated result in the result area.

## Notes

- The app uses GPT-2, a general-purpose language model, so results may vary in quality.
- All processing is done locally on your machine - no data is sent to external servers.
- First run may take longer as the model downloads and loads.
- For better performance, consider using a machine with more RAM.

## Requirements

- Python 3.7+
- Internet connection for initial model download (subsequent runs work offline)
- Sufficient RAM for model loading (GPT-2 requires ~500MB)
