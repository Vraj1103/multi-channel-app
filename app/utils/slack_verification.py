import hashlib
import hmac
import time
from fastapi import HTTPException

from app.config import settings

def verify_slack_request(headers, body):
    timestamp = headers.get("X-Slack-Request-Timestamp")
    if abs(time.time() - int(timestamp)) > 60 * 5:
        raise HTTPException(status_code=400, detail="Request timestamp expired")

    sig_basestring = f"v0:{timestamp}:{body}".encode("utf-8")
    computed_signature = (
        "v0=" + hmac.new(
            settings.slack_signing_secret.encode(),
            sig_basestring,
            hashlib.sha256
        ).hexdigest()
    )

    slack_signature = headers.get("X-Slack-Signature")
    if not hmac.compare_digest(computed_signature, slack_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
