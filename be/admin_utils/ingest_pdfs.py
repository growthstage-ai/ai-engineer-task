import os
import asyncio
from llm import Embeddings
from chromadb_client import ChromaDbClient
from rag import RAG

PDF_DIR = os.path.join(os.path.dirname(__file__), "..", "pdfs")


async def main():
    embeddings = Embeddings()
    chroma_client = ChromaDbClient()
    rag = RAG(chroma_client, embeddings)
    pdf_files = [
        os.path.join(PDF_DIR, f)
        for f in os.listdir(PDF_DIR)
        if f.lower().endswith(".pdf")
    ]
    for pdf_path in pdf_files:
        print(f"Ingesting {pdf_path} ...")
        await rag.ingest_pdf(pdf_path)
        print(f"Done ingesting {pdf_path}")

if __name__ == "__main__":
    asyncio.run(main())
