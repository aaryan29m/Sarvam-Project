import litellm
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

from app.config import settings
from app.compressor import PromptCompressor
from app.cache import SemanticCache
from app.router import ModelRouter
from app.analytics import analytics

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

compressor = PromptCompressor(aggressive=True)
cache = SemanticCache(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
router = ModelRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    bypass_cache: Optional[bool] = False

@app.get("/analytics")
def get_analytics():
    return analytics.get_summary()

@app.post("/v1/chat/completions")
async def chat_completion(request: ChatCompletionRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="Empty messages.")

    last_user_msg = next((m.content for m in reversed(request.messages) if m.role == "user"), "")
    routing_info = router.score_complexity(last_user_msg)
    target_model = request.model or routing_info["selected_model"]

    if not request.bypass_cache:
        cached = cache.get(last_user_msg, target_model)
        if cached:
            analytics.record_hit(tokens_saved=cached.get("original_tokens_est", 50))
            return {
                "id": f"opti-cache-{hash(last_user_msg)}",
                "model": target_model,
                "content": cached["content"],
                "cached": True,
                "tier": routing_info["tier"]
            }

    compressed_text, orig_tok, saved_tok = compressor.compress(last_user_msg)
    processed_messages = [{"role": m.role, "content": compressed_text if m.role == "user" and m.content == last_user_msg else m.content} for m in request.messages]

    try:
        response = litellm.completion(model=target_model, messages=processed_messages, temperature=request.temperature)
        output_text = response.choices[0].message.content
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Provider failed: {str(exc)}")

    cache.set(last_user_msg, target_model, {"content": output_text, "original_tokens_est": orig_tok})
    analytics.record_miss(orig_tok, saved_tok)

    return {
        "id": getattr(response, "id", f"opti-{hash(output_text)}"),
        "model": target_model,
        "content": output_text,
        "cached": False,
        "tokens_saved": saved_tok,
        "tier": routing_info["tier"]
    }
