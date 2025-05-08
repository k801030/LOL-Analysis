import json
import logging
from typing import Optional

import redis


logger = logging.getLogger(__name__)


class APICache:
    def __init__(self, host="localhost", port=6379, db=0, ttl_seconds=600):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.ttl = ttl_seconds  # cache TTL in seconds
        self.prefix = "api|"

    def build_cache_key(self, key):
        return self.prefix + key

    def get(self, url: str) -> Optional[dict]:
        key = self.build_cache_key(url)
        data = self.client.get(key)
        if data:
            logger.debug(f"cache hit: {key}")
            return json.loads(data)
        logger.debug(f"cache not found: {key}")
        return None

    def set(self, url: str, json_string) -> None:
        key = self.build_cache_key(url)
        data = json.dumps(json_string)
        self.client.set(key, data)
