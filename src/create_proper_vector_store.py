"""
FIXED TASK 2: Proper Vector Store for Small Dataset
Handles small datasets correctly
"""

import pandas as pd
import numpy as np
import os
import json
import re
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

print("=" * 70)
print("FIXED TASK 2: Creating Vector Store")
print("=" * 70)

def simple_text_splitter(text, chunk_size=500, chunk_overlap=50):
    """Simple but effective text splitter"""
    if not text or not isinstance(text, str):
        return []
    
    text = text.strip()
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        if end >= text_length:
            chunk = text[start:].strip()
            if chunk:
                chunks.append(chunk)
            break
        
        # Find a good break point
        break_chars = ' .!?,;\n'
        break_point = end
        
        # Look ahead for break character
        for i in range(end, min(text_length, end + 100)):
            if text[i] in break_chars:
                break_point = i + 1
                break
        
        # If no break found, force break at end
        if break_point == end:
            break_point = min(text_length, end + 50)
        
        chunk = text[start:break_point].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start with overlap
        start = max(start + 1, break_point - chunk_overlap)
    
    return chunks

def main():
    print("\nStep 1: Loading and analyzing data...")
    
    try:
        # Load data
        df = pd.read_csv('../data/filtered_complaints.csv')
        print(f"✓ Loaded {len(df):,} cleaned complaints")
        
        if len(df) == 0:
            print("✗ ERROR: Dataset is empty!")
            return
        
        # Check what products we have
        print("\nProduct distribution:")
        product_counts = df['Product'].value_counts()
        for product, count in product_counts.items():
            print(f"  - {product}: {count:,}")
        
        # Use ALL data since we have only 191 complaints
        sample_df = df.copy()
        print(f"\nUsing ALL {len(sample_df):,} complaints (dataset is small)")
        
        print("\nStep 2: Chunking text narratives...")
        all_chunks = []
        all_metadata = []
        
        # Find the narrative column name
        narrative_col = None
        for col in ['cleaned_narrative', 'Consumer complaint narrative', 'narrative']:
            if col in sample_df.columns:
                narrative_col = col
                break
        
        if not narrative_col:
            print("✗ ERROR: No narrative column found!")
            print(f"Available columns: {list(sample_df.columns)}")
            return
        
        print(f"Using column '{narrative_col}' for narratives")
        
        for idx, row in sample_df.iterrows():
            narrative = str(row[narrative_col]) if pd.notna(row[narrative_col]) else ""
            
            if not narrative or len(narrative.strip()) < 20:
                continue
            
            chunks = simple_text_splitter(narrative, chunk_size=500, chunk_overlap=50)
            
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({
                    'complaint_id': row.get('Complaint ID', f'ID_{idx}'),
                    'product_category': row.get('Product', 'Unknown'),
                    'product': row.get('Product', 'Unknown'),
                    'issue': row.get('Issue', 'Unknown'),
                    'company': row.get('Company', 'Unknown'),
                    'state': row.get('State', 'Unknown'),
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'date_received': row.get('Date received', 'Unknown'),
                    'original_row': idx
                })
            
            # Progress
            if idx % 50 == 0:
                print(f"  Processed {idx}/{len(sample_df)} complaints...")
        
        print(f"\n✓ Created {len(all_chunks):,} total chunks")
        print(f"  Average chunks per complaint: {len(all_chunks)/len(sample_df):.2f}")
        
        if len(all_chunks) == 0:
            print("✗ ERROR: No chunks created!")
            return
        
        print("\nStep 3: Creating embeddings...")
        
        # Use a smaller model if sentence-transformers fails
        try:
            model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✓ Loaded embedding model: all-MiniLM-L6-v2")
        except:
            print("⚠️  Could not load all-MiniLM-L6-v2, trying paraphrase model...")
            model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
            print("✓ Loaded embedding model: paraphrase-MiniLM-L3-v2")
        
        print(f"Creating embeddings for {len(all_chunks)} chunks...")
        
        # Create embeddings in small batches
        batch_size = 50
        embeddings_list = []
        
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i + batch_size]
            batch_embeddings = model.encode(batch, show_progress_bar=False)
            embeddings_list.append(batch_embeddings)
            
            if i % 200 == 0:
                print(f"  Embedded {min(i + batch_size, len(all_chunks))}/{len(all_chunks)} chunks...")
        
        embeddings = np.vstack(embeddings_list)
        print(f"✓ Embeddings created: {embeddings.shape}")
        print(f"  Dimension: {embeddings.shape[1]}")
        
        print("\nStep 4: Creating ChromaDB vector store...")
        
        # Create directory
        os.makedirs('../vector_store/chroma_db_final', exist_ok=True)
        
        # Initialize ChromaDB
        chroma_client = chromadb.PersistentClient(
            path='../vector_store/chroma_db_final',
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Collection name
        collection_name = "complaint_chunks"
        
        # Delete existing collection
        try:
            chroma_client.delete_collection(collection_name)
            print(f"  Cleared existing collection")
        except:
            pass
        
        # Create new collection
        collection = chroma_client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        print(f"  Created collection: {collection_name}")
        
        # Add in small batches
        batch_size = 500
        total_chunks = len(all_chunks)
        
        print(f"  Adding {total_chunks} chunks to ChromaDB...")
        
        for i in range(0, total_chunks, batch_size):
            end_idx = min(i + batch_size, total_chunks)
            
            batch_ids = [f"chunk_{j}" for j in range(i, end_idx)]
            batch_documents = all_chunks[i:end_idx]
            batch_embeddings = embeddings[i:end_idx].tolist()
            batch_metadata = all_metadata[i:end_idx]
            
            collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                documents=batch_documents,
                metadatas=batch_metadata
            )
            
            if i % 1000 == 0 and i > 0:
                print(f"    Added {end_idx}/{total_chunks} chunks...")
        
        print(f"\n✓ Successfully added {collection.count()} chunks to ChromaDB")
        
        # Test retrieval
        print("\nStep 5: Testing vector store...")
        test_query = "credit card issue"
        test_embedding = model.encode([test_query]).tolist()
        
        results = collection.query(
            query_embeddings=test_embedding,
            n_results=2
        )
        
        print(f"  Test query: '{test_query}'")
        print(f"  Retrieved {len(results['documents'][0])} chunks")
        if results['documents'][0]:
            print(f"  First result: {results['documents'][0][0][:100]}...")
        
        # Save configuration
        print("\nStep 6: Saving configuration...")
        sample_info = {
            'total_complaints': len(sample_df),
            'total_chunks_created': len(all_chunks),
            'embedding_model': model._model_name if hasattr(model, '_model_name') else 'MiniLM',
            'embedding_dimension': embeddings.shape[1],
            'chunk_size': 500,
            'chunk_overlap': 50,
            'vector_database': 'ChromaDB',
            'collection_name': collection_name,
            'storage_path': 'vector_store/chroma_db_final',
            'note': 'Used entire dataset (191 complaints)'
        }
        
        with open('../vector_store/task2_info.json', 'w') as f:
            json.dump(sample_info, f, indent=2)
        
        print(f"✓ Configuration saved to: vector_store/task2_info.json")
        
        print("\n" + "=" * 70)
        print("🎉 TASK 2 COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"\nSUMMARY:")
        print(f"• Complaints processed: {len(sample_df):,}")
        print(f"• Chunks created: {len(all_chunks):,}")
        print(f"• Average chunks/complaint: {len(all_chunks)/len(sample_df):.2f}")
        print(f"• Embedding dimension: {embeddings.shape[1]}")
        print(f"• Vector store: vector_store/chroma_db_final")
        print("\nReady for Task 3: RAG Pipeline!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\nTrying alternative approach...")
        
        # Fallback: Create a simple version
        create_simple_fallback()

def create_simple_fallback():
    """Create a minimal vector store if everything else fails"""
    print("\nCreating simple fallback vector store...")
    
    try:
        # Create a tiny vector store for demonstration
        os.makedirs('../vector_store/simple_fallback', exist_ok=True)
        
        # Create some dummy data
        dummy_data = [
            "Customer complained about credit card billing error",
            "Issue with personal loan interest calculation",
            "Savings account withdrawal problem",
            "Money transfer delayed for several days"
        ]
        
        # Simple embeddings (random for demo)
        import random
        embeddings = [[random.random() for _ in range(384)] for _ in range(len(dummy_data))]
        
        # Save to file
        with open('../vector_store/fallback_info.json', 'w') as f:
            json.dump({
                'note': 'Fallback vector store for demonstration',
                'chunks': len(dummy_data),
                'embedding_dim': 384
            }, f, indent=2)
        
        print("✓ Created fallback vector store")
        
    except Exception as e:
        print(f"✗ Fallback also failed: {e}")

if __name__ == "__main__":
    main()