from graph.storage import GraphStorage
from graph.query import QueryEngine
from chat.parser import parse_intent
from chat.context import ChatContext

store = GraphStorage()
engine = QueryEngine(store)
context = ChatContext()

print("🚀 Engineering Knowledge Graph Chat (type 'exit')")

while True:
    q = input(">> ").strip()

    if not q:
        continue

    if q.lower() == "exit":
        print("Exiting chat.")
        break

    intent = parse_intent(q)

    # ---------- OWNER ----------
    if intent.get("intent") == "owner":
        entity = intent.get("entity") or context.last_entity

        if not entity:
            print("Please specify a service or resource.")
            continue

        context.last_entity = entity
        owner = engine.get_owner(f"service:{entity}")

        if owner:
            print(f"Owner: {owner}")
        else:
            print("Owner not found.")

    # ---------- BLAST RADIUS ----------
    elif intent.get("intent") == "blast_radius":
        entity = intent.get("entity") or context.last_entity

        if not entity:
            print("Please specify a service or resource.")
            continue

        context.last_entity = entity
        result = engine.blast_radius(f"service:{entity}")

        print("Blast Radius:")
        print("Upstream:", result.get("upstream", []))
        print("Downstream:", result.get("downstream", []))

    # ---------- PATH ----------
    elif intent.get("intent") == "path":
        try:
            src, tgt = intent["entity"]
            path = engine.path(f"service:{src}", f"service:{tgt}")

            if path:
                print("Path:", " → ".join(path))
            else:
                print("No path found.")
        except Exception:
            print("Please specify both source and target services.")

    # ---------- FALLBACK ----------
    else:
        print("Sorry, I could not understand. Try ownership, blast radius, or path queries.")
