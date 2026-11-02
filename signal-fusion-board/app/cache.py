import hashlib
import json
import logging
from typing import Optional, Dict, Any

try:
    import redis
except ImportError:
    redis = None

logger = logging.getLogger("optitoken.cache")

class SemanticCache:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, ttl: int = 86400):
        self.ttl = ttl
        self.memory_store: Dict[str, str] = {}
        self.redis_client = None

        if redis:
            try:
                client = redis.Redis(host=host, port=port, db=db, socket_timeout=1.5)
                client.ping()
                self.redis_client = client
            except Exception as e:
                logger.warning(f"Redis unavailable ({e}). Using in-memory fallback.")

    def _hash_key(self, prompt: str, model: str) -> str:
        payload = f"{model.strip().lower()}::{prompt.strip()}"
        return f"optitoken:cache:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"

    def get(self, prompt: str, model: str) -> Optional[Dict[str, Any]]:
        key = self._hash_key(prompt, model)
        if self.redis_client:
            try:
                cached = self.redis_client.get(key)
                if cached:
                    return json.loads(cached.decode("utf-8"))
            except Exception:
                pass
        val = self.memory_store.get(key)
        return json.loads(val) if val else None

    def set(self, prompt: str, model: str, response_data: Dict[str, Any]):
        key = self._hash_key(prompt, model)
        encoded = json.dumps(response_data)
        if self.redis_client:
            try:
                self.redis_client.setex(key, self.ttl, encoded)
                return
            except Exception:
                pass
        self.memory_store[key] = encoded
