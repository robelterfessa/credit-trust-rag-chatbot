# CreditTrust RAG Complaint Analysis System

## 🚀 Live Demo

Run the application:

```bash
python app.py
Then open: http://127.0.0.1:7860

📋 Project Overview
AI-powered chatbot that analyzes customer complaints using Retrieval-Augmented Generation (RAG). Built for CreditTrust Financial to transform unstructured complaint data into actionable insights.

✅ Features
Semantic Search: 567 complaint chunks searchable via embeddings

AI-Powered Analysis: Rule-based insights from complaint patterns

Source Citation: Every answer shows supporting complaint excerpts

Web Interface: Clean Gradio interface for business users

Fast Processing: <2 second response time

🏗️ Architecture
Data Pipeline: CFPB complaints → Cleaning → Chunking → Embedding

Vector Store: ChromaDB with 567 complaint embeddings

RAG Engine: Semantic search + rule-based analysis

Web Interface: Gradio frontend for natural language Q&A

📁 Project Structure

credit-trust-rag-chatbot/
├── app.py              # Working web application
├── src/               # Source code
│   ├── rag_universal.py  # Universal RAG system
│   └── ...            # Other task implementations
├── data/              # Processed data and evaluations
├── vector_store/      # ChromaDB with 567 embeddings
├── notebooks/         # EDA and analysis
├── screenshots/       # Proof of functionality
└── REPORT.md         # Complete project documentation
🔧 Installation
bash
# Clone repository
git clone https://github.com/robelterfessa/credit-trust-rag-chatbot.git

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
📊 Results
567 complaint chunks processed and searchable

<2 second response time for queries

3 relevant sources cited per answer

End-to-end RAG implementation complete

📸 Screenshots
https://screenshots/terminal_proof.png
https://screenshots/working_query.png

🎯 Business Impact
Enables CreditTrust to:

Reduce complaint analysis time from days to seconds

Provide evidence-backed insights for product improvements

Proactively identify emerging issues

Empower non-technical teams with AI tools
```
