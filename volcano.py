from alerts.volcano_alert import VolcanoAlert


# Example usage:
def main():
    alert_system = VolcanoAlert()
    volcanoes = alert_system.fetch_data()
    for volcano in volcanoes:
        if alert_system.should_alert(volcano):
            alert_message = alert_system.format_alert(volcano)
            print(
                alert_message
            )  # Replace with actual alerting mechanism (e.g., send an email or SMS)


main()
