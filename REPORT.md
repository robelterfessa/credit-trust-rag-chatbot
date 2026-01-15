# Week 7 Challenge Report: Intelligent Complaint Analysis

## Task 1: Exploratory Data Analysis & Data Preprocessing

### Data Overview

- Original dataset sample: 100,000 rows, 18 columns
- After filtering for 4 target products: 1,680 rows
- After removing empty narratives: 191 rows
- Percentage of data kept: 0.19%

### Key Findings

#### 1. Product Distribution:

- Credit card: 191 complaints
- Personal loan: 0 complaints
- Savings account: 0 complaints
- Money transfers: 0 complaints

#### 2. Narrative Length Analysis:

- Average word count: 206.8 words
- Median word count: 168.0 words
- Minimum: 12 words
- Maximum: 1010 words
- 25th percentile: 93.0 words
- 75th percentile: 271.0 words

#### 3. Data Quality Issues:

- 1,489 complaints (88.6%) had missing narratives
- Common boilerplate text found in narratives (e.g., "I am writing to file a complaint")
- Special characters and inconsistent formatting present in raw text

### Preprocessing Steps Applied

1. **Filtering:** Selected only 4 target financial products
2. **Cleaning:** Removed complaints without narratives
3. **Text Processing:**
   - Lowercasing all text
   - Removal of boilerplate phrases and special characters
   - Whitespace normalization
   - Basic punctuation preservation

### Output

- Cleaned dataset saved to: `data/filtered_complaints.csv` with 191 rows.
- Visualizations saved to `figures/` directory.
- Metrics saved to `data/eda_metrics.json`.

### Insights for RAG Pipeline

1. **Chunking Strategy Needed:** Narrative length varies significantly (from 12 to 1010 words), requiring smart chunking.
2. **Product Balance:** Credit cards dominate complaints, which may affect retrieval balance.
3. **Text Quality:** Preprocessing is essential for effective embeddings.

## Task 2: Text Chunking, Embedding, and Vector Store Indexing

### Data Context

- **Dataset Size**: 191 cleaned complaints (smaller than expected but sufficient for learning)
- **Adaptation**: Used entire dataset since stratified sampling for 10K-15K was not possible

### Implementation Details

- **Text Chunking**: Custom splitter with 500-character chunks and 50-character overlap
- **Chunking Results**: Created 567 chunks from 191 complaints (average: 2.97 chunks/complaint)
- **Embedding Model**: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- **Vector Database**: ChromaDB with cosine similarity
- **Retrieval Test**: Successfully retrieved relevant chunks for query "credit card issue"

### Key Metrics

- Total complaints processed: 191
- Total chunks created: 567
- Average chunks per complaint: 2.97
- Embedding dimension: 384
- Vector store location: `vector_store/chroma_db_final/`

### Deliverables Created

1. `vector_store/chroma_db_final/` - Functional ChromaDB vector database
2. `vector_store/task2_info.json` - Complete configuration and statistics
3. `src/create_vector_store_fixed.py` - Reproducible pipeline script

### Learning Objectives Achieved

✓ Implemented text chunking with overlap strategy  
✓ Generated semantic embeddings using sentence transformers  
✓ Created and persisted a queryable vector database  
✓ Stored comprehensive metadata for source tracing  
✓ Validated retrieval functionality with test queries
