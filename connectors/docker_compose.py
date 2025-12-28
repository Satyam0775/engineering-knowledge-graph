import yaml
from connectors.base import BaseConnector


class DockerComposeConnector(BaseConnector):
    def __init__(self):
        self.data = {}
        self.nodes = []
        self.edges = []

    def load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

        if not self.data:
            raise ValueError("docker-compose.yml could not be loaded or is empty")

    def parse(self):
        services = self.data.get("services")

        if not services:
            raise ValueError("No services found in docker-compose.yml")

        for name, cfg in services.items():
            node_id = f"service:{name}"

            # ---- Node ----
            self.nodes.append({
                "id": node_id,
                "type": "service",
                "name": name,
                "properties": cfg.get("labels", {})
            })

            # ---- depends_on ----
            for dep in cfg.get("depends_on", []):
                self.edges.append({
                    "id": f"edge:{name}-depends-{dep}",
                    "type": "depends_on",
                    "source": node_id,
                    "target": f"service:{dep}",
                    "properties": {}
                })

            # ---- env SERVICE_URL ----
            for env in cfg.get("environment", []):
                if "SERVICE_URL" in env:
                    try:
                        target = env.split("http://")[1].split(":")[0]
                        self.edges.append({
                            "id": f"edge:{name}-calls-{target}",
                            "type": "calls",
                            "source": node_id,
                            "target": f"service:{target}",
                            "properties": {}
                        })
                    except Exception:
                        pass  # graceful failure

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges
