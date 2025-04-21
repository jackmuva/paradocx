from app.retrieve.retrieval import run_rag
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def healthcheck():
    return {"Hello": "World"}


@app.get("/chat")
def chat(q:str):
    response, context = run_rag(prompt=q, search_method="hybrid")
    return {"response": response, "context": context}
