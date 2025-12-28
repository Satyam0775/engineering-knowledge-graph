from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()


class GraphStorage:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )

    def close(self):
        self.driver.close()

    def clear(self):
        with self.driver.session(database=self.database) as session:
            session.run("MATCH (n) DETACH DELETE n")

    # ---------- NODE ----------
    def upsert_node(self, node):
        props = node.get("properties", {})

        # build dynamic SET clause
        set_clauses = [
            "n.type = $type",
            "n.name = $name"
        ]

        for key in props.keys():
            set_clauses.append(f"n.{key} = ${key}")

        query = f"""
        MERGE (n {{id: $id}})
        SET {", ".join(set_clauses)}
        """

        params = {
            "id": node["id"],
            "type": node["type"],
            "name": node["name"],
            **props
        }

        with self.driver.session(database=self.database) as session:
            session.run(query, params)

    # ---------- EDGE ----------
    def upsert_edge(self, edge):
        with self.driver.session(database=self.database) as session:
            session.run(
                f"""
                MATCH (a {{id: $source}}), (b {{id: $target}})
                MERGE (a)-[r:{edge["type"].upper()}]->(b)
                SET r.id = $id
                """,
                source=edge["source"],
                target=edge["target"],
                id=edge["id"]
            )
