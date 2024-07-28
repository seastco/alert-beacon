from typing import List, Tuple
from .alert_factory import AlertFactory
from .notification_service import NotificationService
from storage.alerts import SentAlerts
from storage.subscribers import Subscribers


class AlertManager:
    def __init__(
        self,
        notification_service: NotificationService = None,
        sent_alerts_table: SentAlerts = None,
        subscribers_table: Subscribers = None,
    ):
        self.notification_service = notification_service or NotificationService()
        self.sent_alerts_table = sent_alerts_table or SentAlerts()
        self.subscribers_table = subscribers_table or Subscribers()

    def process_alerts(self, alert_types: List[str]) -> None:
        alerts_to_send: List[Tuple[str, str]] = []
        alert_ids_to_store: List[str] = []

        for alert_type in alert_types:
            alert = AlertFactory.create_alert(alert_type)
            data = alert.fetch_data()
            for item in data:
                should_alert = alert.should_alert(item)
                id = alert.get_id(item)
                if should_alert and not self.sent_alerts_table.alert_already_sent(id):
                    message = alert.format_alert(item)
                    alerts_to_send.append((alert.get_id(item), message))

        if alerts_to_send:
            subscribers = self.subscribers_table.get_subscribers()
            for alert_id, message in alerts_to_send:
                self.notification_service.send_alert(message, subscribers)
                alert_ids_to_store.append(alert_id)

            self.sent_alerts_table.store_sent_alerts(alert_ids_to_store)
