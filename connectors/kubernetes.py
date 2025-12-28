import yaml
from connectors.base import BaseConnector


class KubernetesConnector(BaseConnector):
    def __init__(self):
        self.nodes = []
        self.edges = []

    def load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.docs = list(yaml.safe_load_all(f))

    def parse(self):
        for doc in self.docs:
            if not doc:
                continue

            kind = doc.get("kind")
            metadata = doc.get("metadata", {})
            name = metadata.get("name")
            namespace = metadata.get("namespace")

            if not name:
                continue

            # ---------------- DEPLOYMENT ----------------
            if kind == "Deployment":
                spec = doc.get("spec", {})
                replicas = spec.get("replicas")

                self.nodes.append({
                    "id": f"service:{name}",
                    "type": "service",
                    "name": name,
                    "properties": {
                        "namespace": namespace,
                        "replicas": replicas,
                        "source": "kubernetes"
                    }
                })

                # Safely traverse template -> spec -> containers
                template = spec.get("template", {})
                pod_spec = template.get("spec", {})
                containers = pod_spec.get("containers", [])

                for container in containers:
                    for env in container.get("env", []):
                        value = env.get("value")
                        if value and "svc.cluster.local" in value:
                            try:
                                target = value.split("http://")[1].split(".")[0]
                                self.edges.append({
                                    "id": f"edge:{name}-calls-{target}",
                                    "type": "calls",
                                    "source": f"service:{name}",
                                    "target": f"service:{target}",
                                    "properties": {
                                        "via": "kubernetes"
                                    }
                                })
                            except Exception:
                                pass

            # ---------------- SERVICE ----------------
            elif kind == "Service":
                self.nodes.append({
                    "id": f"service:{name}",
                    "type": "service",
                    "name": name,
                    "properties": {
                        "namespace": namespace,
                        "source": "kubernetes-service"
                    }
                })

            # ---------------- IGNORE OTHER KINDS ----------------
            else:
                continue

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges
