from graph.storage import GraphStorage
from graph.query import QueryEngine


def test_graph_basic_functions():
    store = GraphStorage()
    store.clear()

    store.upsert_node({
        "id": "service:test-service",
        "type": "service",
        "name": "test-service",
        "properties": {}
    })

    store.upsert_node({
        "id": "team:test-team",
        "type": "team",
        "name": "test-team",
        "properties": {}
    })

    store.upsert_edge({
        "id": "edge:test-team-owns-test-service",
        "type": "owns",
        "source": "team:test-team",
        "target": "service:test-service",
        "properties": {}
    })

    engine = QueryEngine(store)
    owner = engine.get_owner("service:test-service")

    assert owner == "team:test-team"
