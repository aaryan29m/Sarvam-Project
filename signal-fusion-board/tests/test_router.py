from app.router import ModelRouter

def test_router():
    router = ModelRouter()
    res = router.score_complexity("hello")
    assert res["tier"] == "fast"
