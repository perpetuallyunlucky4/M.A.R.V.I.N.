import datetime
from plugins.plugin_base import Plugin

class timePlugin(Plugin):
    def can_handle(self, message: str) -> bool:
        return "[TIME]" in message

    def handle(self, message: str) -> list[str]:
        return [str(datetime.datetime.now())]
    
