from abc import ABC, abstractmethod
from typing import Any, Dict

class Block(ABC):
    cacheable = True
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    @abstractmethod
    def process(self, data: Any, context: Any) -> Any:
        """Process the input data and return the result."""
        pass
