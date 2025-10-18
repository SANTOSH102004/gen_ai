# Code Snippet Generator

A web application that generates code snippets using OpenAI's GPT-4 API based on user descriptions.

## Features

- Generate code snippets in multiple programming languages
- Clean, responsive web interface
- Copy generated code to clipboard
- Loading states and error handling
- Support for Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, Rust, and TypeScript

## Setup Instructions

1. **Clone or download the project files**

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API Key:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

4. **Run the application:**
   ```
   python app.py
   ```

5. **Open your browser and go to:**
   ```
   http://127.0.0.1:5000/
   ```

## Usage

1. Select a programming language from the dropdown
2. Enter a description of the code you want to generate (e.g., "Python function to sort a list")
3. Click "Generate Code"
4. View the generated code snippet
5. Click "Copy Code" to copy it to your clipboard

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **AI:** OpenAI GPT-4 API
- **Styling:** Custom CSS with responsive design

## Notes

- Make sure you have a valid OpenAI API key with sufficient credits
- The application runs in debug mode by default
- CORS is enabled for frontend-backend communication
