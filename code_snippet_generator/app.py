from flask import Flask, request, jsonify
from transformers import pipeline
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load the GPT-2 model locally (you can change this to a code-focused model like CodeLlama if available)
model_name = os.getenv('MODEL_PATH', 'gpt2')
generator = pipeline('text-generation', model=model_name)

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
        full_prompt = f"Write a {language} code snippet for: {prompt}. Only provide the code, no explanations."

        # Generate code using local transformer model
        result = generator(
            full_prompt,
            max_new_tokens=100,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            pad_token_id=50256
        )

        generated_text = result[0]['generated_text']

        # Extract only the code part (after the prompt)
        if generated_text.startswith(full_prompt):
            code_snippet = generated_text[len(full_prompt):].strip()
        else:
            code_snippet = generated_text.strip()

        # Clean up the code (remove incomplete sentences)
        if code_snippet:
            # Split by newlines and take the first complete code block
            lines = code_snippet.split('\n')
            # Try to find a reasonable stopping point
            clean_lines = []
            for line in lines:
                if line.strip() and not line.startswith('#') and len(clean_lines) < 10:  # Limit to 10 lines
                    clean_lines.append(line)
                elif len(clean_lines) >= 10:
                    break
            code_snippet = '\n'.join(clean_lines).strip()

        return jsonify({'code': code_snippet})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
