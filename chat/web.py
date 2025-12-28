from fastapi import FastAPI, Query
from graph.storage import GraphStorage
from graph.query import QueryEngine
from chat.parser import parse_intent

app = FastAPI()

store = GraphStorage()
engine = QueryEngine(store)

@app.get("/")
def health():
    return {"status": "Engineering Knowledge Graph running"}

@app.get("/ask")
def ask(q: str = Query(..., description="Natural language question")):
    intent = parse_intent(q)

    if intent["intent"] == "owner":
        entity = intent["entity"]
        owner = engine.get_owner(f"service:{entity}")
        return {"question": q, "answer": owner}

    if intent["intent"] == "blast_radius":
        entity = intent["entity"]
        result = engine.blast_radius(f"service:{entity}")
        return {"question": q, "answer": result}

    if intent["intent"] == "path":
        src, tgt = intent["entity"]
        path = engine.path(f"service:{src}", f"service:{tgt}")
        return {"question": q, "answer": path}

    return {"question": q, "answer": "Could not understand the query"}
