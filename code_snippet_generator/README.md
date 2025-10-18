# Code Snippet Generator

A web application that generates code snippets using local transformer models (like GPT-2) via Hugging Face transformers library.

## Features

- Generate code snippets in multiple programming languages
- Clean, responsive web interface
- Copy generated code to clipboard
- Loading states and error handling
- Support for Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, Rust, and TypeScript
- Runs completely offline using local models

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- transformers (Hugging Face library)
- torch (PyTorch for model inference)
- python-dotenv (environment configuration)

### 2. Configure Environment (Optional)

Copy `.env.example` to `.env` if you want to customize settings:
```bash
cp .env.example .env
```

You can optionally specify a different model in the `.env` file:
```
MODEL_PATH=microsoft/DialoGPT-medium  # Alternative model
```

### 3. Run the Application

```bash
python app.py
```

The app will start on `http://127.0.0.1:3000/`

## Usage

1. Select a programming language from the dropdown
2. Enter a description of the code you want to generate (e.g., "Python function to sort a list")
3. Click "Generate Code"
4. View the generated code snippet
5. Click "Copy Code" to copy it to your clipboard

## Model Information

By default, the app uses GPT-2, which is lightweight and runs on most CPUs. GPT-2 is not specifically trained for code generation, so results may vary. For better code generation:

### Alternative Models

You can modify the model in `app.py`:

```python
# For better code generation, try these models:
generator = pipeline('text-generation', model='microsoft/CodeGPT-small-py')  # Python-focused
# or
generator = pipeline('text-generation', model='Salesforce/codegen-350M-mono')  # General code
```

### Model Size Considerations

- **GPT-2** (default): ~500MB, runs on most systems
- **CodeGPT-small-py**: ~500MB, Python-focused
- **CodeGen-350M**: ~700MB, general code generation
- **Larger models**: Better quality but require more RAM/VRAM

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **AI:** Hugging Face transformers with local models
- **Styling:** Custom CSS with responsive design

## Notes

- First run will download the model (~500MB), subsequent runs are faster
- No internet connection required after initial model download
- Runs on CPU by default (can be configured for GPU if available)
- Model generates text based on patterns, not guaranteed correct syntax
