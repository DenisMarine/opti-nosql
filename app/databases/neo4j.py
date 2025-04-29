from neo4j import GraphDatabase
from app.config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))