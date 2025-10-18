# Code Snippet Generator

A web application that generates code snippets using a local LLM server (like text-generation-webui or llama.cpp) based on user descriptions.

## Features

- Generate code snippets in multiple programming languages
- Clean, responsive web interface
- Copy generated code to clipboard
- Loading states and error handling
- Support for Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, Rust, and TypeScript
- Runs completely offline using local LLM models

## Setup Instructions

### 1. Set up Local LLM Server

Choose one of the following options:

#### Option A: text-generation-webui (Recommended)
```bash
# Install text-generation-webui
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui
pip install -r requirements.txt

# Download a code-focused model (e.g., CodeLlama or StarCoder)
# Visit https://huggingface.co/models and search for "codellama" or "starcoder"
# Download the model files to models/ directory

# For smaller models, try:
# - codellama-7b-instruct (needs ~14GB RAM)
# - codellama-13b-instruct (needs ~26GB RAM)
# - starcoder-7b (needs ~14GB RAM)

# Run the server
python server.py --api --model codellama-7b-instruct --listen
```

#### Option B: llama.cpp
```bash
# Download llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build the project
make

# Download a model (GGUF format)
# Visit https://huggingface.co/TheBloke and search for code models
# Example: download codellama-7b-instruct.Q4_K_M.gguf

# Run the server
./server -m models/codellama-7b-instruct.Q4_K_M.gguf --host 0.0.0.0 --port 8080 -c 2048 --threads 8
```

### 2. Configure the Web App

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Update the `LOCAL_LLM_URL` if your server runs on a different port:
     ```
     LOCAL_LLM_URL=http://localhost:5000/v1/chat/completions  # text-generation-webui default
     # or
     LOCAL_LLM_URL=http://localhost:8080/v1/chat/completions  # llama.cpp default
     ```

### 3. Run the Application

1. **Start your local LLM server** (from step 1)

2. **Run the web app:**
   ```
   python app.py
   ```

3. **Open your browser and go to:**
   ```
   http://127.0.0.1:3000/
   ```

## Usage

1. Select a programming language from the dropdown
2. Enter a description of the code you want to generate (e.g., "Python function to sort a list")
3. Click "Generate Code"
4. View the generated code snippet
5. Click "Copy Code" to copy it to your clipboard

## Model Recommendations

For best code generation results, use models specifically trained for code:

- **CodeLlama**: Meta's code-focused Llama models
- **StarCoder**: Large code model from BigCode
- **DeepSeek-Coder**: Good performance with smaller sizes
- **WizardCoder**: Fine-tuned for code generation

### Quantization Tips

To run larger models on consumer hardware:
- Use GGUF format with llama.cpp
- Try Q4_K_M quantization (good balance of size/speed/quality)
- For very limited RAM, try Q3_K_L or even Q2_K

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **AI:** Local LLM via HTTP API (text-generation-webui or llama.cpp)
- **Styling:** Custom CSS with responsive design

## Notes

- The app runs on port 3000 to avoid conflicts with LLM servers
- No internet connection required after setup (completely offline)
- First generation may be slower as the model loads into memory
- Adjust model parameters in the LLM server for different creativity levels
