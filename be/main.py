from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import StreamingResponse
from llm import LLM, Embeddings
from chromadb_client import ChromaDbClient
from rag import RAG
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
def read_hello():
    return {"message": "Hello, world!"}


@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    conversation = data.get("conversation")
    llm = LLM()
    embeddings = Embeddings()
    chroma_client = ChromaDbClient()
    rag = RAG(chroma_client, embeddings)

    # Find the latest user message for retrieval
    user_messages = [m for m in conversation if m.get("role") == "user"]
    latest_user_message = user_messages[-1]["content"] if user_messages else ""

    # Retrieve relevant context from ChromaDB using RAG
    context_chunks = await rag.retrieve_relevant_chunks(latest_user_message, k=4)
    context_text = "\n\n".join(context_chunks)
    if context_text:
        # Prepend context as a system message
        conversation = (
            [{"role": "system", "content": f"Relevant context:\n{context_text}"}]
            + conversation
        )

    async def event_stream():
        async for chunk in llm.generate(conversation):
            # SSE format: data: <chunk>\n\n
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
