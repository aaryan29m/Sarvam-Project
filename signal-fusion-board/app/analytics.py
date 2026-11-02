import time
from typing import Dict, Any

class TokenAnalytics:
    def __init__(self):
        self.total_requests = 0
        self.cache_hits = 0
        self.tokens_saved = 0
        self.tokens_processed = 0
        self.start_time = time.time()

    def record_hit(self, tokens_saved: int):
        self.total_requests += 1
        self.cache_hits += 1
        self.tokens_saved += tokens_saved

    def record_miss(self, prompt_tokens: int, tokens_saved_by_compression: int):
        self.total_requests += 1
        self.tokens_processed += prompt_tokens
        self.tokens_saved += tokens_saved_by_compression

    def get_summary(self) -> Dict[str, Any]:
        hit_rate = (self.cache_hits / self.total_requests) if self.total_requests > 0 else 0.0
        return {
            "uptime_seconds": round(time.time() - self.start_time, 2),
            "total_requests": self.total_requests,
            "cache_hits": self.cache_hits,
            "hit_rate_percentage": round(hit_rate * 100, 2),
            "tokens_saved": self.tokens_saved,
            "tokens_processed": self.tokens_processed,
            "estimated_dollars_saved": round(self.tokens_saved * 0.000003, 4)
        }

analytics = TokenAnalytics()
