import yaml
from connectors.base import BaseConnector

class TeamsConnector(BaseConnector):
    def __init__(self):
        self.nodes = []
        self.edges = []

    def load(self, path):
        with open(path, "r") as f:
            self.data = yaml.safe_load(f)

    def parse(self):
        for team in self.data.get("teams", []):
            team_id = f"team:{team['name']}"

            self.nodes.append({
                "id": team_id,
                "type": "team",
                "name": team["name"],
                "properties": {
                    "lead": team["lead"],
                    "slack": team["slack_channel"]
                }
            })

            for asset in team.get("owns", []):
                self.edges.append({
                    "id": f"edge:{team['name']}-owns-{asset}",
                    "type": "owns",
                    "source": team_id,
                    "target": f"service:{asset}",
                    "properties": {}
                })

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges
