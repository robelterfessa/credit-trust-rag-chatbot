# diagnostics.py
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(
    path='vector_store/chroma_db_final',
    settings=Settings(anonymized_telemetry=False)
)

print("Available collections:")
print(client.list_collections())