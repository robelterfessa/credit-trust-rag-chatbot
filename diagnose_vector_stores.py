# diagnose_vector_stores.py
import os
import chromadb
from chromadb.config import Settings

print("DIAGNOSING VECTOR STORE LOCATIONS")
print("=" * 60)

# Check all possible locations
locations = [
    'vector_store/chroma_db_final',
    'vector_store/chroma_db_proper',
    'vector_store/chroma_db',
    'vector_store',
    'chroma_db_final',
    '../vector_store/chroma_db_final'
]

for location in locations:
    if os.path.exists(location):
        print(f"\n✓ Found: {location}")
        print(f"  Type: {'Directory' if os.path.isdir(location) else 'File'}")
        
        # Try to load as ChromaDB
        try:
            client = chromadb.PersistentClient(path=location)
            collections = client.list_collections()
            print(f"  Collections: {len(collections)}")
            for col in collections:
                print(f"    - '{col.name}' with {col.count()} items")
        except Exception as e:
            print(f"  Not a ChromaDB or error: {e}")
    else:
        print(f"\n✗ Not found: {location}")

print("\n" + "=" * 60)
print("Checking directory structure...")
print("Current directory:", os.getcwd())
print("\nContents of vector_store/:")
if os.path.exists('vector_store'):
    for item in os.listdir('vector_store'):
        item_path = os.path.join('vector_store', item)
        size = "dir" if os.path.isdir(item_path) else f"{os.path.getsize(item_path):,} bytes"
        print(f"  - {item} ({size})")