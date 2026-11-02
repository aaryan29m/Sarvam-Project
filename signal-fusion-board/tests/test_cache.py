from app.cache import SemanticCache

def test_cache():
    cache = SemanticCache(host="none", port=0)
    cache.set("ping", "gpt", {"content": "pong"})
    assert cache.get("ping", "gpt")["content"] == "pong"
