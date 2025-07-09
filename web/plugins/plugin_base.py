class Plugin:
    def can_handle(self, message: str) -> bool:
        raise NotImplementedError
    
    def handle(self, message: str) -> list[str]:
        raise NotImplementedError