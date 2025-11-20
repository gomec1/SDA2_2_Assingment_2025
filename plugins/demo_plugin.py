# IMPORTANT - use the BasePlugin class

# If you create another plugin please create a seperate file for it, copy the code from this file and remember - the text you put in """ """ will be 
# the description of your plugin on the side bar, and text you put in name function will be the oficial name of your plugin :)


from core.plugin_base import BasePlugin


class DemoPlugin(BasePlugin):
    """Demo plugin that does absolutely nothing :)"""

    @property
    def name(self) -> str:
        return "Demo"

    def process(self, text: str) -> str:
        return text

