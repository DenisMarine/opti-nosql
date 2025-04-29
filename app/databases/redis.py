import redis as Redis
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis = Redis.StrictRedis(host=REDIS_HOST, 
                      port=REDIS_PORT, 
                      db=REDIS_DB, 
                      decode_responses=True)