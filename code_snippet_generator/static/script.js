document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('snippet-form');
    const generateBtn = document.getElementById('generate-btn');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const error = document.getElementById('error');
    const codeOutput = document.getElementById('code-output');
    const copyBtn = document.getElementById('copy-btn');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const prompt = document.getElementById('prompt').value.trim();
        const language = document.getElementById('language').value;

        if (!prompt) {
            showError('Please enter a prompt for the code snippet.');
            return;
        }

        // Show loading state
        showLoading();

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    language: language
                })
            });

            const data = await response.json();

            if (response.ok) {
                showResult(data.code);
            } else {
                showError(data.error || 'An error occurred while generating the code.');
            }
        } catch (err) {
            showError('Network error. Please check your connection and try again.');
        }
    });

    copyBtn.addEventListener('click', function() {
        const code = codeOutput.textContent;
        navigator.clipboard.writeText(code).then(function() {
            // Temporarily change button text to show success
            const originalText = copyBtn.textContent;
            copyBtn.textContent = 'Copied!';
            copyBtn.style.backgroundColor = '#17a2b8';
            setTimeout(() => {
                copyBtn.textContent = originalText;
                copyBtn.style.backgroundColor = '';
            }, 2000);
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
            alert('Failed to copy code to clipboard.');
        });
    });

    function showLoading() {
        loading.style.display = 'block';
        result.style.display = 'none';
        error.style.display = 'none';
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
    }

    function showResult(code) {
        loading.style.display = 'none';
        result.style.display = 'block';
        error.style.display = 'none';
        codeOutput.textContent = code;
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Code';
    }

    function showError(message) {
        loading.style.display = 'none';
        result.style.display = 'none';
        error.style.display = 'block';
        document.getElementById('error-message').textContent = message;
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Code';
    }
});
