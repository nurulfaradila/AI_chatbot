# DoDo Quick Start

### Operational Checklist
- [x] Python Environment Configured
- [x] Dependencies Installed
- [x] Ollama (Phi) Downloaded
- [x] Document Index Initialized

### URLs
- **Main App**: http://localhost:8000
- **System Health**: http://localhost:8000/health
- **Technical Docs**: http://localhost:8000/docs

### Quick Commands

**Update Documents:**
1. Put files in `data/documents/`
2. Run: `curl -X POST http://localhost:8000/index`

**Direct Query (API):**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I use DoDo?", "k": 3}'
```

### Setup Notes
- **LLM**: Phi (via Ollama)
- **Database**: local FAISS store
- **Embeddings**: MiniLM-L6-v2 (local)
