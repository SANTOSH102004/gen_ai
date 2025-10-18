from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from transformers import pipeline
import markdown

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load GPT-2 model for text generation
generator = pipeline('text-generation', model='gpt2')

def generate_code(prompt, language):
    """Generate code snippet based on prompt and language."""
    full_prompt = f"Generate a {language} code snippet for: {prompt}. Provide only the code without any explanation or markdown formatting."
    try:
        result = generator(full_prompt, max_new_tokens=150, num_return_sequences=1, temperature=0.3, do_sample=True, pad_token_id=50256)
        code = result[0]['generated_text'].replace(full_prompt, '').strip()
        # Clean up markdown if present
        if code.startswith('```'):
            code = code.split('```')[1]
            if code.startswith(language.lower()):
                code = code.split('\n', 1)[1] if '\n' in code else code
            code = code.rstrip('```').strip()
        return code
    except Exception as e:
        return f"Error generating code: {str(e)}"

def debug_code(code):
    """Debug and fix code."""
    prompt = f"Debug and fix this code. Provide the corrected code and a brief explanation:\n{code}\n\nFixed code:"
    try:
        result = generator(prompt, max_new_tokens=200, num_return_sequences=1, temperature=0.2, do_sample=True, pad_token_id=50256)
        response = result[0]['generated_text'].replace(prompt, '').strip()
        return response
    except Exception as e:
        return f"Error debugging code: {str(e)}"

def explain_code(code):
    """Explain what the code does in plain English."""
    prompt = f"Explain what this code does in simple terms:\n{code}\n\nExplanation:"
    try:
        result = generator(prompt, max_new_tokens=150, num_return_sequences=1, temperature=0.3, do_sample=True, pad_token_id=50256)
        explanation = result[0]['generated_text'].replace(prompt, '').strip()
        return explanation
    except Exception as e:
        return f"Error explaining code: {str(e)}"

def generate_unit_tests(code):
    """Generate unit tests for the given code."""
    prompt = f"Generate pytest unit tests for this code:\n{code}\n\nUnit tests:"
    try:
        result = generator(prompt, max_new_tokens=200, num_return_sequences=1, temperature=0.3, do_sample=True, pad_token_id=50256)
        tests = result[0]['generated_text'].replace(prompt, '').strip()
        return tests
    except Exception as e:
        return f"Error generating tests: {str(e)}"

def translate_code(code, target_language):
    """Translate code to another language."""
    prompt = f"Translate this code to {target_language}:\n{code}\n\nTranslated code:"
    try:
        result = generator(prompt, max_new_tokens=150, num_return_sequences=1, temperature=0.3, do_sample=True, pad_token_id=50256)
        translated = result[0]['generated_text'].replace(prompt, '').strip()
        return translated
    except Exception as e:
        return f"Error translating code: {str(e)}"

def generate_regex(description):
    """Generate regex based on description."""
    prompt = f"Generate a regex pattern for: {description}. Provide the regex and a brief explanation."
    try:
        result = generator(prompt, max_new_tokens=100, num_return_sequences=1, temperature=0.3, do_sample=True, pad_token_id=50256)
        regex = result[0]['generated_text'].replace(prompt, '').strip()
        return regex
    except Exception as e:
        return f"Error generating regex: {str(e)}"

def nl_to_sql(natural_language):
    """Convert natural language to SQL."""
    prompt = f"Convert this natural language query to SQL: {natural_language}\n\nSQL query:"
    try:
        result = generator(prompt, max_new_tokens=100, num_return_sequences=1, temperature=0.3, do_sample=True, pad_token_id=50256)
        sql = result[0]['generated_text'].replace(prompt, '').strip()
        return sql
    except Exception as e:
        return f"Error converting to SQL: {str(e)}"

def markdown_to_html(markdown_text):
    """Convert markdown to HTML."""
    try:
        html = markdown.markdown(markdown_text)
        return html
    except Exception as e:
        return f"Error converting markdown: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')
    language = data.get('language', 'Python')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    code = generate_code(prompt, language)
    return jsonify({'result': code})

@app.route('/debug', methods=['POST'])
def debug():
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    result = debug_code(code)
    return jsonify({'result': result})

@app.route('/explain', methods=['POST'])
def explain():
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    result = explain_code(code)
    return jsonify({'result': result})

@app.route('/unittest', methods=['POST'])
def unittest():
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    result = generate_unit_tests(code)
    return jsonify({'result': result})

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    code = data.get('code')
    target_language = data.get('target_language')
    if not code or not target_language:
        return jsonify({'error': 'Code and target language are required'}), 400
    result = translate_code(code, target_language)
    return jsonify({'result': result})

@app.route('/regex', methods=['POST'])
def regex():
    data = request.get_json()
    description = data.get('description')
    if not description:
        return jsonify({'error': 'Description is required'}), 400
    result = generate_regex(description)
    return jsonify({'result': result})

@app.route('/nl2sql', methods=['POST'])
def nl2sql():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    result = nl_to_sql(query)
    return jsonify({'result': result})

@app.route('/md2html', methods=['POST'])
def md2html():
    data = request.get_json()
    markdown_text = data.get('markdown')
    if not markdown_text:
        return jsonify({'error': 'Markdown text is required'}), 400
    result = markdown_to_html(markdown_text)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
