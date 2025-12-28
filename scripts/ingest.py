from connectors.docker_compose import DockerComposeConnector
from connectors.teams import TeamsConnector
from connectors.kubernetes import KubernetesConnector
from graph.storage import GraphStorage


def run_ingestion():
    store = GraphStorage()

    # 🔥 Clear existing graph (important for re-runs)
    store.clear()

    all_nodes = []
    all_edges = []

    # ---------- Docker Compose ----------
    dc = DockerComposeConnector()
    dc.load("data/docker-compose.yml")
    dc.parse()
    all_nodes.extend(dc.get_nodes())
    all_edges.extend(dc.get_edges())

    # ---------- Teams ----------
    tc = TeamsConnector()
    tc.load("data/teams.yaml")
    tc.parse()
    all_nodes.extend(tc.get_nodes())
    all_edges.extend(tc.get_edges())

    # ---------- Kubernetes (BONUS) ----------
    try:
        kc = KubernetesConnector()
        kc.load("data/k8s-deployments.yaml")
        kc.parse()
        all_nodes.extend(kc.get_nodes())
        all_edges.extend(kc.get_edges())
        print("✅ Kubernetes data ingested")
    except FileNotFoundError:
        print("⚠️ Kubernetes config not found, skipping (optional)")

    # ---------- PHASE 1: INSERT ALL NODES ----------
    for node in all_nodes:
        store.upsert_node(node)

    # ---------- PHASE 2: INSERT ALL EDGES ----------
    for edge in all_edges:
        store.upsert_edge(edge)

    print("✅ Graph built successfully and stored in Neo4j")


if __name__ == "__main__":
    run_ingestion()
