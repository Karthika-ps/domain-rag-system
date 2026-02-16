# Domain-Adaptive Retrieval-Augmented Generation (RAG) System

A production-oriented Retrieval-Augmented Generation (RAG) system designed for technical document question answering.  
This project implements structured ingestion, similarity-based retrieval using FAISS, evaluation-driven threshold tuning, grounded summarization, and Dockerized REST API deployment.

---

## 🚀 Project Overview

This system enables users to query complex technical PDF documents via a REST API.  
It uses semantic retrieval to fetch relevant document chunks and generates grounded answers using an LLM.

Key capabilities:

- PDF ingestion with structured chunking
- FAISS vector indexing
- L2-distance similarity tuning
- Retrieval evaluation framework
- Guardrail-based hallucination mitigation
- Page-level traceability
- Dockerized API deployment

---

## 🏗 Architecture

User Query  
→ Embed Query  
→ FAISS Similarity Search (L2 Distance)  
→ Threshold Filtering  
→ Context Assembly (Top-k Ranking)  
→ Grounded LLM Summarization  
→ JSON Response with Source Pages  

---

## 📂 Project Structure

domain-rag-assistant/
│
├── src/
│ ├── ingest.py # PDF ingestion and FAISS index creation
│ ├── retrieval.py # Similarity search and L2 threshold filtering
│ ├── rag_pipeline.py # Context assembly and grounded generation
│ └── app.py # Flask REST API
│
├── evaluation/
│ ├── test_queries.json # Evaluation dataset
│ └── evaluate.py # Retrieval coverage evaluation
│
├── data/raw_pdfs/ # Source PDFs
├── vector_store/ # Persisted FAISS index
├── requirements.txt
├── Dockerfile
└── README.md

---

## 🔎 Retrieval Engineering

- Chunk size: 1000 tokens
- Overlap: 200 tokens
- Vector store: FAISS
- Similarity metric: L2 (Euclidean distance)
- Threshold tuning via empirical inspection
- Top-k retrieval balancing precision and recall

### Why L2?

FAISS defaults to L2 distance.  
Lower distance indicates stronger semantic similarity.

Threshold was tuned (~0.40–0.42) based on observed clustering of relevant chunks.

---

## 📊 Retrieval Evaluation

A lightweight evaluation framework measures keyword coverage across test queries.

Metrics:

- Coverage ratio per query
- Average keyword coverage
- Threshold sensitivity tuning

Example:

Average coverage achieved: ~0.79  
All evaluation queries passed minimum relevance threshold.

---

## 🛡 Guardrails

To reduce hallucination risk:

- Refusal if no relevant chunks pass threshold
- Prompt constraint: answers must be derived from retrieved context
- Page-level source traceability included in API response

---


## 🌐 API Usage

### 🔧 Setup

1. Place your PDF documents inside `data/raw_pdfs/`
2. Run ingestion:

```bash
python src/ingest.py
```

3. Start API:

```bash
python src/app.py
```

Example request:

``` bash
curl -X POST http://127.0.0.1:5000/query

-H "Content-Type: application/json"
-d '{"question": "What operational risks were identified?"}'
```


Example response:

{
"answer": "...",
"sources": [
{
"distance": 0.35,
"page": "54",
"preview": "..."
}
]
}

---

## 🐳 Docker Deployment

Build image:

``` bash
docker build -t domain-rag-api .
```

Run container:

``` bash 
docker run -p 5000:5000 --env-file .env domain-rag-api
```

Environment variables are injected securely at runtime.

---

## 📌 Future Improvements

- Hybrid search (BM25 + vector retrieval)
- Re-ranking model integration
- Automated evaluation expansion
- Streaming responses
- Multi-document ingestion

---

## 📎 Notes

This implementation demonstrates a modular, evaluation-aware RAG architecture suitable for enterprise technical documentation environments.
