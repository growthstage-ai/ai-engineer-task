# Admin Utilities

This directory contains scripts for managing the backend database and document ingestion pipeline. These utilities are primarily for development, testing, and administrative tasks.

## What Does This Contain?

- **create_database.py**: Creates a fresh SQLite database with the required schema.
- **populate_data.py**: Populates the database with mock data (customers, products, orders, etc.).
- **download_data.py**: Downloads product manuals (PDFs) and generates policy documents (returns, shipping, FAQ).
- **gen_policy_docs.py**: Generates policy documents as PDFs.
- **ingest_pdfs.py**: Ingests all PDFs in the `pdfs/` directory into the vector database for retrieval-augmented generation (RAG).

## One-Stop Setup: `setup.py`

To (re)initialize the backend database, download all manuals, generate policy docs, and ingest all PDFs, simply run:

```bash
python setup.py
```

This will:

1. Destroy any existing database and create a new one.
2. Populate the database with mock data.
3. Download all product manuals and generate policy documents.
4. Ingest all PDFs into the vector database.

**Note:**  
You generally do **not** need to edit these scripts during normal operation. The backend will function without manual intervention here.  
However, if you need to reset the backend state (e.g., after schema changes or to start fresh), use `setup.py` as described above.

## When Should I Use This?

- If you want to reset or recreate the database and all ingested documents.
- If you add new PDFs or change the schema and need to re-ingest everything.
- For development, testing, or troubleshooting backend data issues.
