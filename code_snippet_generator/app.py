from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate_snippet():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        language = data.get('language', 'Python')

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        # Create a detailed prompt for code generation
        full_prompt = f"Generate a {language} code snippet for: {prompt}. Provide only the code without any explanation or markdown formatting."

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful code generator. Generate clean, efficient code snippets."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )

        code_snippet = response.choices[0].message.content.strip()

        # Remove any markdown code blocks if present
        if code_snippet.startswith('```'):
            code_snippet = code_snippet.split('```')[1]
            if code_snippet.startswith(language.lower()):
                code_snippet = code_snippet.split('\n', 1)[1]
            code_snippet = code_snippet.rstrip('```').strip()

        return jsonify({'code': code_snippet})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
