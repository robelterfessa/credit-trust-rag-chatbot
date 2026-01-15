"""
SIMPLIFIED Task 2: Text Chunking and Vector Store
No langchain, no tqdm - uses basic Python only
"""

import pandas as pd
import numpy as np
import os
import json
import re

print("=" * 70)
print("SIMPLIFIED TASK 2: Creating Vector Store")
print("=" * 70)

def simple_text_splitter(text, chunk_size=500, chunk_overlap=50):
    """Simple text splitter without langchain"""
    chunks = []
    
    # Split by sentences first (simple approach)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    current_chunk = ""
    for sentence in sentences:
        # If adding this sentence would exceed chunk size
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Keep overlap
            overlap_start = max(0, len(current_chunk) - chunk_overlap)
            current_chunk = current_chunk[overlap_start:] + " " + sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    
    # Add the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def main():
    print("\nStep 1: Loading data...")
    
    try:
        df = pd.read_csv('../data/filtered_complaints.csv')
        print(f"✓ Loaded {len(df)} complaints")
        
        # Take a smaller sample for speed
        sample_size = min(5000, len(df))
        sample_df = df.sample(n=sample_size, random_state=42)
        print(f"Using sample of {sample_size} complaints")
        
        print("\nStep 2: Chunking text...")
        all_chunks = []
        all_metadata = []
        
        for idx, row in sample_df.iterrows():
            # Get narrative text
            narrative = ""
            for col in ['cleaned_narrative', 'Consumer complaint narrative']:
                if col in row and isinstance(row[col], str):
                    narrative = row[col]
                    break
            
            if not narrative or len(narrative.strip()) < 50:
                continue
            
            # Split into chunks
            chunks = simple_text_splitter(narrative, chunk_size=500, chunk_overlap=50)
            
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({
                    'complaint_id': idx,
                    'product': row.get('Product', 'Unknown'),
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                })
        
        print(f"✓ Created {len(all_chunks)} chunks")
        
        print("\nStep 3: Creating simple vector store (CSV-based)...")
        
        # Create a simple vector store using pandas
        vector_data = pd.DataFrame({
            'chunk_text': all_chunks,
            'metadata': [json.dumps(m) for m in all_metadata]
        })
        
        # Save to CSV
        vector_data.to_csv('../vector_store/simple_vector_store.csv', index=False)
        
        # Save info
        sample_info = {
            'total_complaints_sampled': sample_size,
            'total_chunks_created': len(all_chunks),
            'chunk_size': 500,
            'chunk_overlap': 50,
            'vector_store': 'simple_csv_store'
        }
        
        with open('../vector_store/sample_info.json', 'w') as f:
            json.dump(sample_info, f, indent=2)
        
        print("\n" + "=" * 70)
        print("✓ SIMPLIFIED TASK 2 COMPLETED!")
        print("=" * 70)
        print(f"Created: {len(all_chunks)} chunks")
        print(f"Saved to: vector_store/simple_vector_store.csv")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()