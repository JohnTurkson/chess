import base64


def get_event_body(event):
    body = event["body"]
    if event["isBase64Encoded"]:
        return base64.b64decode(body)
    else:
        return body
