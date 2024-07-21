from typing import List, Tuple
from .alert_factory import AlertFactory
from .notification_service import NotificationService
from .storage_service import StorageService


class AlertManager:
    def __init__(
        self,
        notification_service: NotificationService = None,
        storage_service: StorageService = None,
    ):
        self.notification_service = notification_service or NotificationService()
        self.storage_service = storage_service or StorageService()

    def process_alerts(self, alert_types: List[str]) -> None:
        alerts_to_send: List[Tuple[str, str]] = []
        alert_ids_to_store: List[str] = []

        for alert_type in alert_types:
            alert = AlertFactory.create_alert(alert_type)
            data = alert.fetch_data()
            for item in data:
                if alert.should_alert(item) and not self.storage_service.alert_already_sent(
                    alert.get_id(item)
                ):
                    message = alert.format_alert(item)
                    alerts_to_send.append((alert.get_id(item), message))

        if alerts_to_send:
            subscribers = self.storage_service.get_subscribers()
            for alert_id, message in alerts_to_send:
                self.notification_service.send_alert(message, subscribers)
                alert_ids_to_store.append(alert_id)

            self.storage_service.store_sent_alerts(alert_ids_to_store)
