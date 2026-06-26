# Arquitectura do Sistema

```
Utilizador
    │
    ▼
┌─────────────────┐
│  Streamlit UI   │  ← Interface web (localhost:8501)
│   (app.py)      │
└────────┬────────┘
         │
    ┌────▼────────────────────────┐
    │     LangChain RAG Pipeline  │
    │      (rag_pipeline.py)      │
    └────┬──────────────┬─────────┘
         │              │
    ┌────▼────┐    ┌────▼──────┐
    │ChromaDB │    │  Ollama   │
    │(vetores)│    │ Phi3:mini │
    └─────────┘    └───────────┘
         ▲
    ┌────┴────────────┐
    │ document_loader │
    │ PDF/TXT/DOCX    │
    └─────────────────┘
```

**Fluxo de dados:**
1. Utilizador carrega documento → `document_loader.py` extrai texto
2. Texto dividido em chunks → `nomic-embed-text` converte em vetores
3. Vetores guardados localmente no `ChromaDB`
4. Pergunta do utilizador → vetorizada → 3 chunks mais relevantes recuperados
5. Chunks + pergunta → `Phi-3 Mini` via Ollama → resposta gerada localmente