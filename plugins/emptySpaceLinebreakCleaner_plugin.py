import re
from core.plugin_base import BasePlugin


class EmptySpaceLinebreakCleaner(BasePlugin):
    """This plugin removes any whitespace and line breaks from the text."""

    @property
    def name(self) -> str:
        return "Whitespace & linebreak cleaner"

    def process(self, text: str) -> str:
        if text is None:
            return ""
      
        # Harmonize Windows/Mac Linebreaks 
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Tabs -> Space
        text = text.replace("\t", " ")

        # Trim each line
        lines = [line.strip() for line in text.split("\n")]
        text = "\n".join(lines)

        # Reduce multiple Spaces in one line
        text = re.sub(r"[ ]{2,}", " ", text)

        # Reduce multiple empy lines to exactly one empty line
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text