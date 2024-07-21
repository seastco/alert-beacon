from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseAlert(ABC):
    @abstractmethod
    def fetch_data(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def should_alert(self, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def format_alert(self, data: Dict[str, Any]) -> str:
        pass
