# Al Mamlaka TV Knowledge Base Assistant

A bilingual (Arabic / English) **Retrieval-Augmented Generation (RAG)** chatbot that answers questions strictly from a set of PDF documents, cites its sources, and flags contradictions between documents.

Built during my practical training at **Al Mamlaka TV** as a training prototype.

>  **Note:** All documents in this repository are **mock data** created for training purposes. They do not contain any real internal information from Al Mamlaka TV.

<!-- Add a screenshot of the interface here -->
<!-- ![Interface](screenshots/interface.png) -->

---

## Features

- **Source-grounded answers:** the assistant answers only from the documents and says so when the answer is not available.
- **Citations:** every claim is cited in the form `[Document Name, p. X]`.
- **Conflict detection:** when two documents disagree (e.g. different dates or budgets), the assistant shows both values and points out the conflict.
- **Bilingual:** replies in the language of the question, using formal Modern Standard Arabic for Arabic.
- **Multi-turn conversation:** keeps the context of the conversation.
- **Prompt-injection resistance:** stays in its role and scope even when asked to ignore its instructions.
- **Branded interface:** designed to match the channel's visual identity, with light and dark modes.

## How It Works

```
PDF documents
   │  pdfplumber (text extraction)
   ▼
Chunking by section headers
   │  Voyage AI  voyage-multilingual-2
   ▼
Embeddings stored in index.json
   │
User question ──► embed ──► cosine similarity ──► top 6 chunks
                                                     │
                                                     ▼
                              Claude API + 11-rule system prompt
                                                     │
                                                     ▼
                                    Answer with citations
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Gunicorn |
| PDF parsing | pdfplumber |
| Embeddings | Voyage AI (`voyage-multilingual-2`) |
| Retrieval | Cosine similarity (top-k = 6) |
| Generation | Anthropic Claude API |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render (connected to GitHub) |

## Project Structure

```
├── app.py              # Flask app: chat endpoint and system prompt
├── build_index.py      # Extracts, chunks, and embeds the PDFs into index.json
├── retrieve.py         # Cosine-similarity retrieval
├── index.json          # Pre-built embeddings index
├── documents/          # Knowledge base PDFs (mock data)
├── templates/          # HTML templates
├── static/             # CSS, JavaScript, and images
├── requirements.txt
└── Procfile            # Start command for deployment
```

## Run Locally

1. Clone the repository and install the requirements:
   ```bash
   git clone https://github.com/wajdalmadi/almamlaka-rag-chatbot.git
   cd almamlaka-rag-chatbot
   python -m venv venv
   venv\Scripts\activate        # On macOS/Linux: source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create a `.env` file with your own API keys:
   ```
   ANTHROPIC_API_KEY=your_key_here
   VOYAGE_API_KEY=your_key_here
   ```
3. (Optional) Rebuild the index if you change the documents:
   ```bash
   python build_index.py
   ```
4. Start the app and open http://127.0.0.1:5000:
   ```bash
   python app.py
   ```

## What I Learned

- Designing a full RAG pipeline, from PDF parsing to grounded generation.
- Writing a strict system prompt to control model behavior, citations, and tone.
- Handling mixed Arabic and English text in extraction and retrieval.
- Keeping API keys secure with environment variables and deploying a Flask app.

## Author

**Wajd Almadi** : AI student at Jordan University of Science and Technology
[LinkedIn](https://www.linkedin.com/in/wajd-almadi) · [GitHub](https://github.com/wajdalmadi)
