import json
from twilio.twiml.messaging_response import MessagingResponse
from ..storage.subscribers import Subscribers


def lambda_handler(event, context):
    body = json.loads(event["body"])
    message = body["Body"].strip().upper()
    from_number = body["From"]

    subscribe_keywords = [
        "SUBSCRIBE",
        "SUBCRIBE",  # typo1
        "SUBSRIBE",  # typo2
        "START",
        "ENROLL",
        "REGISTER",
    ]
    unsubscribe_keywords = [
        "UNSUBSCRIBE",
        "STOP",
        "OPT OUT",
        "OPTOUT",
    ]

    subscribers = Subscribers()
    resp = MessagingResponse()

    if message in subscribe_keywords:
        subscribers.add_subscriber(from_number)
        resp.message("You have successfully subscribed to Tectonic Alert!")
    elif message in unsubscribe_keywords:
        subscribers.remove_subscriber(from_number)
        resp.message("You have unsubscribed from Tectonic Alert.")
    return {"statusCode": 200, "headers": {"Content-Type": "application/xml"}, "body": str(resp)}
