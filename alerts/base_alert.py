from abc import ABC, abstractmethod

class BaseAlert(ABC):
    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def should_alert(self, data):
        pass

    @abstractmethod
    def format_alert(self, data):
        pass
    