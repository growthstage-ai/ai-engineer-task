import os
from typing import List
from llm import Embeddings
from chromadb_client import ChromaDbClient
import PyPDF2


class RAG:
    def __init__(self, chroma_client: ChromaDbClient, embeddings: Embeddings):
        self.chroma_client = chroma_client
        self.embeddings = embeddings

    @staticmethod
    def extract_text_chunks_from_pdf(pdf_path: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        reader = PyPDF2.PdfReader(pdf_path)
        all_text = ""
        for page in reader.pages:
            all_text += page.extract_text() or ""
        # Simple chunking by character count with overlap
        chunks = []
        start = 0
        while start < len(all_text):
            end = min(start + chunk_size, len(all_text))
            chunk = all_text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        return [c.strip() for c in chunks if c.strip()]

    async def ingest_pdf(self, pdf_path: str):
        chunks = self.extract_text_chunks_from_pdf(pdf_path)
        vectors = await self.embeddings.embed_batch(chunks)
        ids = [f"{os.path.basename(pdf_path)}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": pdf_path}] * len(chunks)
        self.chroma_client.add_documents(
            embeddings=vectors,
            documents=chunks,
            ids=ids,
            metadatas=metadatas,
        )

    async def retrieve_relevant_chunks(self, query: str, k: int = 4) -> List[str]:
        query_vec = await self.embeddings.embed(query)
        results = self.chroma_client.query(
            query_embeddings=[query_vec],
            n_results=k,
            include=["documents"],
        )
        return results["documents"][0] if results["documents"] else []
