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
