"""
ULTIMATE SIMPLE APP - No fancy components, guaranteed to work
"""

import gradio as gr
import sys
sys.path.append('src')

from rag_universal import UniversalRAG

print("=" * 70)
print("ULTIMATE SIMPLE WORKING APP")
print("=" * 70)

# Initialize RAG
rag = UniversalRAG()
print("✅ RAG system ready!")

def analyze_question(question):
    """Simple function that always works"""
    if not question.strip():
        return "Please enter a question."
    
    print(f"Processing: {question}")
    
    try:
        # Get RAG response
        answer, chunks, metadata = rag.process_query(question)
        
        # Build simple response
        response = f"## 🔍 Analysis Results\n\n"
        response += f"{answer}\n\n"
        
        if chunks:
            response += f"## 📋 Evidence ({len(chunks)} sources)\n\n"
            for i, chunk in enumerate(chunks[:3]):
                response += f"{i+1}. {chunk[:100]}...\n\n"
        
        return response
        
    except Exception as e:
        return f"Error: {str(e)}"

# SIMPLEST POSSIBLE INTERFACE
with gr.Blocks() as demo:
    gr.Markdown("# CreditTrust Complaint Analysis")
    gr.Markdown("Ask questions about customer complaints")
    
    # Just two textboxes and a button - NOTHING ELSE
    question_box = gr.Textbox(
        label="Your Question",
        placeholder="Example: What are common credit card issues?"
    )
    
    output_box = gr.Textbox(
        label="Analysis Results", 
        lines=10
    )
    
    analyze_btn = gr.Button("Analyze")
    
    # Connect
    analyze_btn.click(analyze_question, question_box, output_box)
    question_box.submit(analyze_question, question_box, output_box)
    
    # Simple examples as text
    gr.Markdown("### Try these questions:")
    gr.Markdown("- What are common credit card issues?")
    gr.Markdown("- Tell me about billing problems")
    gr.Markdown("- Any customer service complaints?")
    gr.Markdown("- Fee-related issues reported?")

print("\n" + "=" * 70)
print("🚀 SIMPLEST APP RUNNING")
print("Open: http://127.0.0.1:7860")
print("=" * 70)

demo.launch(server_port=7860, inbrowser=True)