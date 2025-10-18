import gradio as gr
from transformers import pipeline

# Load the GPT-2 model locally
generator = pipeline('text-generation', model='gpt2')

# Global conversation history
conversation_history = []

def generate_response(prompt, temperature=0.7, max_length=100):
    if not prompt.strip():
        return "Please enter a valid prompt."
    
    try:
        # Add user prompt to history
        conversation_history.append(f"User: {prompt}")
        
        # Build context from history (last 5 exchanges to avoid too long context)
        context = "\n".join(conversation_history[-10:])  # Last 5 user-bot pairs
        
        # Generate response using GPT-2
        result = generator(context, max_length=max_length, num_return_sequences=1, temperature=temperature, do_sample=True, pad_token_id=50256)
        response = result[0]['generated_text']
        
        # Extract only the new response (after the context)
        if response.startswith(context):
            new_response = response[len(context):].strip()
        else:
            new_response = response.strip()
        
        # Clean up response (remove incomplete sentences)
        if new_response and not new_response.endswith(('.', '!', '?')):
            sentences = new_response.split('.')
            if len(sentences) > 1:
                new_response = '.'.join(sentences[:-1]) + '.'
        
        # Add bot response to history
        conversation_history.append(f"Bot: {new_response}")
        
        # Return full conversation
        return "\n\n".join(conversation_history)
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def clear_history():
    global conversation_history
    conversation_history.clear()
    return ""

# Create Gradio interface with chat-like UI
with gr.Blocks(title="Advanced GPT-2 Chatbot") as iface:
    gr.Markdown("# Advanced GPT-2 Chatbot")
    gr.Markdown("Have a conversation with GPT-2. Adjust parameters for different response styles.")
    
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(height=400)
            msg = gr.Textbox(placeholder="Enter your message here...", label="Message")
            with gr.Row():
                submit_btn = gr.Button("Send")
                clear_btn = gr.Button("Clear History")
        
        with gr.Column(scale=1):
            gr.Markdown("### Parameters")
            temperature = gr.Slider(minimum=0.1, maximum=2.0, value=0.7, step=0.1, label="Temperature (Creativity)")
            max_length = gr.Slider(minimum=50, maximum=200, value=100, step=10, label="Max Length")
    
    def respond(message, chat_history, temp, max_len):
        if not message.strip():
            return chat_history, ""
        
        try:
            # Add user message to history
            chat_history = chat_history or []
            chat_history.append((message, None))
            
            # Build context
            context = "\n".join([f"User: {msg}\nBot: {resp}" for msg, resp in chat_history[:-1] if resp]) + f"\nUser: {message}\nBot:"
            
            # Generate response
            result = generator(context, max_length=max_len, num_return_sequences=1, temperature=temp, do_sample=True, pad_token_id=50256)
            response = result[0]['generated_text']
            
            # Extract bot response
            if "Bot:" in response:
                bot_response = response.split("Bot:")[-1].strip()
            else:
                bot_response = response[len(context):].strip()
            
            # Clean response
            if bot_response and not bot_response.endswith(('.', '!', '?')):
                sentences = bot_response.split('.')
                if len(sentences) > 1:
                    bot_response = '.'.join(sentences[:-1]) + '.'
            
            # Update chat history
            chat_history[-1] = (message, bot_response)
            
            return chat_history, ""
        
        except Exception as e:
            chat_history.append((message, f"Error: {str(e)}"))
            return chat_history, ""
    
    def clear_chat():
        return [], ""
    
    msg.submit(respond, [msg, chatbot, temperature, max_length], [chatbot, msg])
    submit_btn.click(respond, [msg, chatbot, temperature, max_length], [chatbot, msg])
    clear_btn.click(clear_chat, [], [chatbot, msg])

if __name__ == "__main__":
    iface.launch()
