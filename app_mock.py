"""
Mock version to test the UI first
"""

import gradio as gr
import pandas as pd
from datetime import datetime

# Mock RAG system
class MockRAG:
    def process_query(self, query, k=3):
        answers = {
            "credit card": "Common credit card issues include unauthorized charges, billing errors, and high fees.",
            "billing": "Customers report billing problems such as incorrect charges, hidden fees, and late payment penalties.",
            "service": "Service complaints mention long wait times, unhelpful representatives, and unresolved issues.",
            "fees": "Fee-related complaints focus on unexpected charges, high interest rates, and penalty fees."
        }
        
        # Find matching answer
        query_lower = query.lower()
        answer = "Based on complaint analysis: "
        
        for key, response in answers.items():
            if key in query_lower:
                answer += response
                break
        else:
            answer += "Customers report various issues across financial products including billing disputes and service problems."
        
        # Mock sources
        chunks = [
            f"Complaint about {query_lower}: Customer reported issue on XX/XX/XXXX.",
            f"Related complaint involving similar {query_lower.split()[0] if query_lower.split() else ''} problem.",
            "Additional complaint data shows pattern across multiple customers."
        ]
        
        metadata = [
            {"product_category": "Credit Card", "issue": "General complaint"},
            {"product_category": "Various", "issue": "Related issue"},
            {"product_category": "Multiple", "issue": "Pattern analysis"}
        ]
        
        return answer, chunks, metadata

# Initialize
rag = MockRAG()
history = []

def respond(message, chat_history):
    answer, chunks, meta = rag.process_query(message)
    
    # Format with sources
    response = f"**Answer:** {answer}\n\n**Sources:**\n"
    for i, chunk in enumerate(chunks[:2]):
        response += f"{i+1}. {chunk}\n"
    
    chat_history.append((message, response))
    return "", chat_history

# Simple interface
with gr.Blocks(title="CreditTrust Mock Demo") as demo:
    gr.Markdown("# CreditTrust Complaint Analysis (Mock Demo)")
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Ask about complaints")
    clear = gr.Button("Clear")
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot)

demo.launch()