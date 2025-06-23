import litellm
from typing import AsyncGenerator, List


class Embeddings:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model

    async def embed(self, text: str) -> List[float]:
        """
        Returns the embedding vector for a single string.
        """
        # litellm.aembedding returns a dict with 'data' key containing embeddings
        result = await litellm.aembedding(
            model=self.model,
            input=[text]
        )
        return result["data"][0]["embedding"]

    async def embed_batch(self, texts: List[str], batch_size: int = 16) -> List[List[float]]:
        """
        Returns a list of embedding vectors for a list of strings.
        Processes texts in batches to avoid API limits.
        """
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i: i + batch_size]
            result = await litellm.aembedding(
                model=self.model,
                input=batch
            )
            all_embeddings.extend([item["embedding"]
                                  for item in result["data"]])
        return all_embeddings


class LLM:
    def __init__(self, model: str = "gpt-4.1"):
        self.model = model

    async def generate(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        """
        Streams output from the LLM as it is generated.
        """
        # messages: list of {"role": "user"|"assistant", "content": str}
        result = await litellm.acompletion(
            model=self.model,
            messages=messages,
            stream=True,
        )
        async for chunk in result:
            delta = chunk["choices"][0]["delta"].get("content", "")
            if delta:
                yield delta
