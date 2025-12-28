class QueryEngine:
    def __init__(self, storage):
        self.driver = storage.driver

    # ---------- OWNER ----------
    def get_owner(self, service_id):
        with self.driver.session() as session:
            record = session.run(
                """
                MATCH (t)-[:OWNS]->(s {id: $sid})
                RETURN t.id AS owner
                """,
                sid=service_id
            ).single()
            return record["owner"] if record else None

    # ---------- DOWNSTREAM ----------
    def downstream(self, node_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (n {id: $id})-[:CALLS|DEPENDS_ON*1..]->(d)
                RETURN DISTINCT d.id AS node
                """,
                id=node_id
            )
            return [r["node"] for r in result]

    # ---------- UPSTREAM ----------
    def upstream(self, node_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u)-[:CALLS|DEPENDS_ON*1..]->(n {id: $id})
                RETURN DISTINCT u.id AS node
                """,
                id=node_id
            )
            return [r["node"] for r in result]

    # ---------- BLAST RADIUS ----------
    def blast_radius(self, node_id):
        return {
            "upstream": self.upstream(node_id),
            "downstream": self.downstream(node_id)
        }

    # ---------- SHORTEST PATH ----------
    def path(self, src, tgt):
        with self.driver.session() as session:
            record = session.run(
                """
                MATCH p = shortestPath(
                  (a {id: $src})-[:CALLS|DEPENDS_ON*..10]->(b {id: $tgt})
                )
                RETURN [n IN nodes(p) | n.id] AS path
                """,
                src=src,
                tgt=tgt
            ).single()
            return record["path"] if record else None
