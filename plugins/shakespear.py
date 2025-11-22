import re
from core.plugin_base import BasePlugin


class ShakespeareanFilter(BasePlugin):
    """It transforms any text as if it had been written by Shakespeare."""

    @property
    def name(self) -> str:
        return "Shakespearean Filter"

    SHAKESPEARE_MAP = {
            "you": "thou",
            "are": "art",
            "your": "thy",
            "yours": "thine",
            "have": "hast",
            "has": "hath",
            "do": "dost",
            "does": "doth",
            "go": "goest",
            "come": "comest",
            "think": "think’st",
            "friend": "good sir",
            "hello": "hail",
            "hi": "well met",
            "yes": "aye",
            "no": "nay",
            "please": "prithee",
            "food": "victuals",
            "money": "coin",
        }

    def match_case(self, original: str, replacement: str) -> str:

            if original.islower():
                return replacement.lower()
            
            if original.isupper():
                return replacement.upper()
            
            if original.istitle():
                return replacement.capitalize()
            
            return "".join(
            rep_char.upper() if orig_char.isupper() else rep_char.lower()
            for orig_char, rep_char in zip(
                original, replacement.ljust(len(original), replacement[-1])
            )
        )
    
    def process(self, text: str) -> str:
            if text is None:
                return ""
            
            tokens = re.findall(r"\w+|\W+", text)

            result = []
            for token in tokens:
                if token.isalpha():
                    key = token.lower()
                    if key in self.SHAKESPEARE_MAP:
                        base = self.SHAKESPEARE_MAP[key]
                        token = self.match_case(token, base)
                result.append(token)
            
            return "".join(result)

    