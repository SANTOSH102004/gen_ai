from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Local LLM server configuration
LOCAL_LLM_URL = os.getenv('LOCAL_LLM_URL', 'http://localhost:5000/v1/chat/completions')

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

        # Prepare payload for local LLM API (compatible with text-generation-webui or similar)
        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful code generator. Generate clean, efficient code snippets."},
                {"role": "user", "content": full_prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.3,
            "stream": False
        }

        # Call local LLM API
        response = requests.post(LOCAL_LLM_URL, json=payload, timeout=60)

        if response.status_code != 200:
            return jsonify({'error': f'LLM server error: {response.status_code}'}), 500

        result = response.json()
        code_snippet = result['choices'][0]['message']['content'].strip()

        # Remove any markdown code blocks if present
        if code_snippet.startswith('```'):
            code_snippet = code_snippet.split('```')[1]
            if code_snippet.startswith(language.lower()):
                code_snippet = code_snippet.split('\n', 1)[1]
            code_snippet = code_snippet.rstrip('```').strip()

        return jsonify({'code': code_snippet})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to connect to local LLM server: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)  # Run on port 3000 to avoid conflict with LLM server
