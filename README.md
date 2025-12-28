# Engineering Knowledge Graph (EKG)

## Overview

This project implements a prototype **Engineering Knowledge Graph (EKG)** that unifies engineering knowledge across code, infrastructure, and operations into a single, queryable graph with a natural language interface.

Engineering context is often fragmented across Docker, Kubernetes, and team ownership files. This system parses those sources, builds a unified graph representation in **Neo4j**, and enables engineers to ask high-level questions such as:

- Who owns a service or database?
- What breaks if a dependency goes down?
- What is the blast radius of a failure?
- How are two components connected?

The focus of this prototype is **systems thinking, correct graph modeling, and end-to-end reasoning**, rather than UI polish.

---

## Repository Structure

# Engineering Knowledge Graph (EKG)

## Overview

This project implements a prototype **Engineering Knowledge Graph (EKG)** that unifies engineering knowledge across code, infrastructure, and operations into a single, queryable graph with a natural language interface.

Engineering context is often fragmented across Docker, Kubernetes, and team ownership files. This system parses those sources, builds a unified graph representation in **Neo4j**, and enables engineers to ask high-level questions such as:

- Who owns a service or database?
- What breaks if a dependency goes down?
- What is the blast radius of a failure?
- How are two components connected?

The focus of this prototype is **systems thinking, correct graph modeling, and end-to-end reasoning**, rather than UI polish.

---

## Repository Structure

engineering-knowledge-graph/
├── README.md # Documentation
├── docker-compose.yml # Optional single-command startup
├── data/
│ ├── docker-compose.yml # Provided infrastructure config
│ ├── teams.yaml # Provided team ownership config
│ └── k8s-deployments.yaml # Optional Kubernetes config
├── connectors/
│ ├── docker_compose.py # Docker Compose connector
│ ├── teams.py # Teams connector
│ └── kubernetes.py # Kubernetes connector (bonus)
├── graph/
│ ├── storage.py # Neo4j graph storage layer
│ └── query.py # Query engine
├── chat/
│ ├── app.py # Chat interface
│ ├── parser.py # Intent parsing
│ └── context.py # Conversation context
├── scripts/
│ └── ingest.py # End-to-end ingestion pipeline
├── tests/
│ └── test_basic.py # Basic correctness tests
└── requirements.txt


---

## A. Setup & Usage

### Prerequisites

- Python 3.10+
- Neo4j AuraDB (Free tier)
- Virtual environment (recommended)

---

### Environment Variables

Create a `.env` file in the project root:

```env
NEO4J_URI=neo4j+s://<your-instance>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<your-password>
NEO4J_DATABASE=neo4j


Create a `.env` file in the project root:

```env
NEO4J_URI=neo4j+s://<your-instance>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<your-password>
NEO4J_DATABASE=neo4j
Install Dependencies

pip install -r requirements.txt
Start the System
Step 1: Build the Graph

python -m scripts.ingest
This step:

Parses Docker Compose, Teams, and Kubernetes configs
Builds nodes and relationships
Stores everything in Neo4j

Step 2: Start the Chat Interface
python -m chat.app
Example queries:

Who owns payment-service?
What breaks if redis-main goes down?
How does api-gateway connect to payments-db?
B. Architecture Overview
Data Flow
java

Config Files
(docker-compose.yml, teams.yaml, k8s)
        ↓
Pluggable Connectors
        ↓
Neo4j Graph Storage
        ↓
Query Engine (Traversal Logic)
        ↓
Chat Interface (Natural Language)
Key Components
Connectors: Parse raw configuration files into nodes and edges

Graph Storage: Persists the unified graph in Neo4j

Query Engine: Executes dependency, blast radius, and path queries

Chat Interface: Translates natural language into graph queries

C. Design Questions
1. Connector Pluggability
Each connector follows a shared interface and outputs nodes and edges in a consistent format. To add a new connector (e.g., Terraform), a new parser can be added without modifying the core ingestion or query logic.

2. Graph Updates
The ingestion pipeline clears and rebuilds the graph on each run. This ensures the graph always reflects the current state of configuration files without requiring complex diffing logic.

3. Cycle Handling
All traversals rely on Neo4j’s native graph traversal engine, which safely handles cycles. This prevents infinite loops during upstream and downstream dependency analysis.

4. Query Mapping
Common query patterns (ownership, blast radius, paths) are mapped deterministically. For ambiguous input, the system requests clarification instead of guessing.

5. Failure Handling
When a query cannot be answered, the chat interface returns a safe fallback message. The system avoids hallucination by only answering from graph data.

6. Scale Considerations
At larger scale (10K+ nodes), indexing and relationship filtering would be required. Neo4j supports this natively and would scale with minimal changes.

7. Graph Database Choice
Neo4j was chosen because it is explicitly optimized for relationship-heavy queries such as dependency traversal and blast radius analysis. These queries are significantly more complex in relational databases.

D. Tradeoffs & Limitations
The chat interface is CLI-based instead of a full web UI
Authentication and authorization are not production-grade
The LLM layer is intentionally minimal to avoid hallucination
With more time, this could be extended with:
A web-based UI
Incremental graph updates

Additional connectors (Terraform, GitHub)

E. AI Usage
AI tools were used to:
Accelerate prototyping
Validate traversal logic
Improve natural language query coverage

All final logic, graph modeling, and integrations were manually verified and corrected where required.

Demo Video
The demo video includes:
System startup
Graph ingestion
Neo4j visualization
Natural language queries
Blast radius and path analysis
Explanation of a key design decision

Conclusion
This project demonstrates how an Engineering Knowledge Graph can unify infrastructure, ownership, and dependencies into a single system that supports both programmatic and natural language access, enabling faster reasoning and safer operational decisions.
