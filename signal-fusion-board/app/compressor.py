import re
from typing import Tuple

class PromptCompressor:
    FILLER_PATTERNS = [
        r"(?i)\b(please note that|kindly be advised that|as you know|in other words)\b",
        r"(?i)\b(feel free to|let me know if you need anything else|thank you in advance)\b"
    ]

    def __init__(self, aggressive: bool = True):
        self.aggressive = aggressive

    def compress(self, text: str) -> Tuple[str, int, int]:
        if not text:
            return text, 0, 0
        orig_char = len(text)
        orig_tok = max(1, orig_char // 4)
        compressed = text
        compressed = re.sub(r'\r\n', '\n', compressed)
        compressed = re.sub(r'\n{3,}', '\n\n', compressed)
        compressed = re.sub(r'[ \t]{2,}', ' ', compressed)

        if self.aggressive:
            for pattern in self.FILLER_PATTERNS:
                compressed = re.sub(pattern, '', compressed)

        compressed = compressed.strip()
        new_tok = max(1, len(compressed) // 4)
        saved_tok = max(0, orig_tok - new_tok)
        return compressed, orig_tok, saved_tok
