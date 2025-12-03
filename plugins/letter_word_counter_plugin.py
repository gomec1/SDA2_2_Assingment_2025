from __future__ import annotations
import re

from core.plugin_base import BasePlugin


class LetterWordCounterPlugin(BasePlugin):
    """Counts letters and words, then prepares a short report."""

    @property
    def name(self) -> str:
        return "Letter + Word Counter"

    def process(self, text: str) -> str:
        word_count = len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))
        letter_count = sum(1 for ch in text if ch.isalpha())

        report = [
            "--- Letter + Word Counter ---",
            f"Words: {word_count}",
            f"Letters: {letter_count}",
            "",
        ]

        return "\n".join(report) + text
