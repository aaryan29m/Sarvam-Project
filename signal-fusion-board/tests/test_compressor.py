from app.compressor import PromptCompressor

def test_compression():
    comp = PromptCompressor(aggressive=True)
    c, orig, saved = comp.compress("Please note that this is a critical test.")
    assert "Please note that" not in c
    assert saved > 0
