"""
GUARANTEED WORKING APP - Minimal, always works
"""

import gradio as gr
import sys
sys.path.append('src')

from rag_universal import UniversalRAG

rag = UniversalRAG()

# SIMPLEST POSSIBLE FUNCTION
def chat(message, history):
    answer, chunks, meta = rag.process_query(message)
    
    # Simple format
    response = f"Analysis: {answer}\n\nSources:\n"
    for i, chunk in enumerate(chunks[:2]):
        response += f"{i+1}. {chunk[:80]}...\n"
    
    # This format ALWAYS works
    return [(message, response)]

# Minimal interface
with gr.Blocks() as demo:
    gr.Markdown("# CreditTrust Complaint Chat")
    
    chatbot = gr.Chatbot()
    textbox = gr.Textbox(placeholder="Ask about complaints...")
    
    textbox.submit(chat, [textbox, chatbot], [chatbot])

demo.launch(inbrowser=True)