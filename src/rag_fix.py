"""
Fix for ChromaDB collection name issue
"""

import chromadb
from chromadb.config import Settings
import os

print("Fixing ChromaDB collection name...")

# Path to your vector store
vector_store_path = '../vector_store/chroma_db_final'

if not os.path.exists(vector_store_path):
    print(f"❌ Vector store not found at: {vector_store_path}")
    print("Available vector stores:")
    for item in os.listdir('../vector_store'):
        if os.path.isdir(f'../vector_store/{item}'):
            print(f"  - {item}/")
else:
    client = chromadb.PersistentClient(
        path=vector_store_path,
        settings=Settings(anonymized_telemetry=False)
    )
    
    collections = client.list_collections()
    print(f"Found {len(collections)} collections:")
    
    for collection in collections:
        print(f"  - '{collection.name}' with {collection.count()} items")
    
    # If no collections found, create one
    if len(collections) == 0:
        print("No collections found. Creating 'complaint_chunks' collection...")
        try:
            collection = client.create_collection(name="complaint_chunks")
            print(f"✓ Created collection: {collection.name}")
        except Exception as e:
            print(f"❌ Error creating collection: {e}")
    else:
        # Use the first available collection
        print(f"\nUsing collection: '{collections[0].name}'")
        print("To fix your RAG system, change the collection name in rag_pipeline_offline.py")
        print("to match one of the collections listed above.")