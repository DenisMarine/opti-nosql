from neo4j import AsyncGraphDatabase
from app.config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER

neo4j_driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))