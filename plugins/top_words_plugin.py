import re
from collections import Counter
from core.plugin_base import BasePlugin


class TopWordsFrequencyPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "Top Words (Frequency)"

    @property
    def description(self) -> str:
        return (
            "Counts the most frequent words in the text and inserts a report of the top "
            "words before the original text."
        )

    # Small stop word list to filter out common words
    STOP_WORDS = {
        "the", "and", "or", "but", "a", "an", "is", "are", "was", "were",
        "i", "you", "he", "she", "it", "we", "they",
        "of", "to", "in", "on", "for", "with", "at", "by", "from", "this",
        "that", "these", "those", "not", "be", "have", "has", "do", "does", "did",
        "as", "if", "so", "no", "yes", "all", "any", "some", "what", "which", "who", "whom",
        "my", "your", "his", "her", "its", "our", "their", "me", "him", "them",
        "about", "into", "over", "after", "before", "between", "under", "again", "further", "then", "once",

    }

    def process(self, text: str) -> str:
        # Extract words (alphanumeric sequences)
        words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)

        # Normalize to lowercase and remove stop words
        normalized = [
            w.lower()
            for w in words
            if w.strip() and w.lower() not in self.STOP_WORDS
        ]

        counter = Counter(normalized)
        # top_n = 10 #Change this value to get more or fewer top words
        top_n = 10
        most_common = counter.most_common(top_n)

        if not most_common:
            report = (
                "--- Top Words (Frequency) ---\n"
                "No countable words found.\n\n"
            )
            return report + text

        lines = [
            "--- Top Words (Frequency) ---",
            f"Top {len(most_common)} words (without simple stop words):",
            "",
        ]
        for word, count in most_common:
            lines.append(f"{word}: {count}")

        report = "\n".join(lines) + "\n\n"

        # Insert report before the original text
        return report + text
