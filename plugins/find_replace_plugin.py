from core.plugin_base import BasePlugin
import re


class FindReplacePlugin(BasePlugin):
    """
   Replace all occurrences of a string (or regex pattern) with another string.
    """

    @property
    def name(self) -> str:
        return "Find & Replace"

    def __init__(self) -> None:
        self.pattern = ""
        self.replacement = ""
        self.use_regex = False

    def process(self, text: str) -> str:
        if self.use_regex:
            return re.sub(self.pattern, self.replacement, text)
        else:
            return text.replace(self.pattern, self.replacement)
