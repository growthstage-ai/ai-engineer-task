import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional

CHROMA_COLLECTION_NAME = "documents"
CHROMA_DB_DIR = "chroma_db"


class ChromaDbClient:
    def __init__(self, collection_name: str = CHROMA_COLLECTION_NAME, persist_directory: str = CHROMA_DB_DIR):
        self.client = chromadb.PersistentClient(
            persist_directory,
        )
        self.collection = self._get_or_create_collection(collection_name)

    def _get_or_create_collection(self, collection_name: str):
        if collection_name in [c.name for c in self.client.list_collections()]:
            return self.client.get_collection(collection_name)
        return self.client.create_collection(collection_name)

    def add_documents(
        self,
        embeddings: List[List[float]],
        documents: List[str],
        ids: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ):
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            ids=ids,
            metadatas=metadatas,
        )

    def query(
        self,
        query_embeddings: List[List[float]],
        n_results: int = 4,
        include: List[str] = ["documents"],
    ) -> Dict[str, Any]:
        return self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            include=include,
        )
