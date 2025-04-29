from typing import List
from app.databases.neo4j import neo4j_driver as driver

async def get_recommendations_service(city: str, k: int) -> List[dict]:
    cypher_query = """
    MATCH (c:City {code: $city})-[r:NEAR]->(n:City)
    RETURN n.code AS city, r.weight AS score
    ORDER BY r.weight DESC
    LIMIT $k
    """
    
    async with driver.session() as session:
        result = await session.run(cypher_query, city=city, k=k)
        
        recommendations = []
        async for record in result:
            print(record)
            recommendations.append({"city": record["city"], "score": record["score"]})
        
        return recommendations
