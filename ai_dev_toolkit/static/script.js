function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-button');
    tabs.forEach(tab => tab.classList.remove('active'));
    buttons.forEach(button => button.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

async function submitForm(formId, endpoint, data, resultId) {
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const result = document.getElementById(resultId);

    loading.style.display = 'block';
    error.style.display = 'none';
    result.textContent = '';

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const responseData = await response.json();

        if (response.ok) {
            result.textContent = responseData.result;
        } else {
            error.textContent = responseData.error;
            error.style.display = 'block';
        }
    } catch (err) {
        error.textContent = 'Network error. Please try again.';
        error.style.display = 'block';
    } finally {
        loading.style.display = 'none';
    }
}

document.getElementById('generate-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const prompt = document.getElementById('gen-prompt').value.trim();
    const language = document.getElementById('gen-language').value;
    if (!prompt) {
        alert('Please enter a prompt.');
        return;
    }
    submitForm('generate-form', '/generate', { prompt, language }, 'gen-result');
});

document.getElementById('debug-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const code = document.getElementById('debug-code').value.trim();
    if (!code) {
        alert('Please enter code to debug.');
        return;
    }
    submitForm('debug-form', '/debug', { code }, 'debug-result');
});

document.getElementById('explain-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const code = document.getElementById('explain-code').value.trim();
    if (!code) {
        alert('Please enter code to explain.');
        return;
    }
    submitForm('explain-form', '/explain', { code }, 'explain-result');
});

document.getElementById('unittest-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const code = document.getElementById('unittest-code').value.trim();
    if (!code) {
        alert('Please enter code to generate tests for.');
        return;
    }
    submitForm('unittest-form', '/unittest', { code }, 'unittest-result');
});

document.getElementById('translate-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const code = document.getElementById('translate-code').value.trim();
    const targetLanguage = document.getElementById('translate-target').value;
    if (!code || !targetLanguage) {
        alert('Please enter code and select target language.');
        return;
    }
    submitForm('translate-form', '/translate', { code, target_language: targetLanguage }, 'translate-result');
});

document.getElementById('regex-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const description = document.getElementById('regex-desc').value.trim();
    if (!description) {
        alert('Please enter a description.');
        return;
    }
    submitForm('regex-form', '/regex', { description }, 'regex-result');
});

document.getElementById('nl2sql-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const query = document.getElementById('nl2sql-query').value.trim();
    if (!query) {
        alert('Please enter a natural language query.');
        return;
    }
    submitForm('nl2sql-form', '/nl2sql', { query }, 'nl2sql-result');
});

document.getElementById('md2html-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const markdown = document.getElementById('md2html-markdown').value.trim();
    if (!markdown) {
        alert('Please enter markdown text.');
        return;
    }
    submitForm('md2html-form', '/md2html', { markdown }, 'md2html-result').then(() => {
        // Update preview
        const result = document.getElementById('md2html-result').textContent;
        document.getElementById('md2html-preview').innerHTML = result;
    });
});
