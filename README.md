# Basic RAG (PDF + Qdrant + OpenRouter)

This project is a simple Retrieval-Augmented Generation (RAG) demo that:

- Loads a PDF document
- Splits it into chunks
- Creates embeddings using OpenAI-compatible APIs (via OpenRouter)
- Stores vectors in Qdrant
- Answers user questions by retrieving relevant chunks and sending context to an LLM

## Project Files

- `index.py` - Ingests/indexes a PDF into Qdrant
- `chat.py` - CLI chat script that retrieves context and answers questions
- `docker-compose.yml` - Runs Qdrant locally
- `requirements.txt` - Python dependencies

## Prerequisites

- Python 3.10+ (recommended)
- Docker Desktop (for local Qdrant)
- OpenRouter API key (stored as `OPENAI_API_KEY`)

## 1) Clone and Install

```bash
git clone https://github.com/amol127/Basic_RAG.git
cd Basic_RAG
python -m venv .venv
```

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS/Linux

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Start Qdrant

```bash
docker compose up -d
```

Qdrant will be available at `http://localhost:6333`.

## 3) Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openrouter_api_key_here
```

> This project uses `OPENAI_API_KEY` with OpenRouter base URL in both scripts.

## 4) Add the PDF

Place your PDF at:

`docs/python_programming.pdf`

The current indexing script expects this exact path:

```python
file_path = Path(__file__).parent / "docs/python_programming.pdf"
```

## 5) Index the Document

Run:

```bash
python index.py
```

Expected output:

`Indexing of documents done ....`

This creates/updates the `learning_rag` collection in Qdrant.

## 6) Ask Questions

Run:

```bash
python chat.py
```

You will see:

`Ask something:`

Type your question and the script retrieves relevant chunks from Qdrant, then sends context to the model (`openai/gpt-4o-mini` in current code).

## How It Works (Flow)

1. PDF loaded with `PyPDFLoader`
2. Text split via `RecursiveCharacterTextSplitter`
3. Embeddings created using `text-embedding-3-large`
4. Chunks stored in Qdrant collection `learning_rag`
5. Similarity search done for user query
6. Retrieved context passed to chat completion model

## Troubleshooting

- **`OPENAI_API_KEY` missing**  
  Ensure `.env` exists and has a valid key.

- **Qdrant connection error**  
  Confirm Docker is running and `docker compose up -d` succeeded.

- **PDF not found**  
  Make sure `docs/python_programming.pdf` exists.

- **No useful answers**  
  Re-run indexing after updating the PDF:
  - `python index.py`

## Notes

- The project currently uses OpenRouter endpoints hardcoded in both scripts.
- Collection name is fixed as `learning_rag`.
- If you change embedding model or chunk settings, re-index the document.

## License

Add your preferred license (MIT, Apache-2.0, etc.) if you plan to publish.