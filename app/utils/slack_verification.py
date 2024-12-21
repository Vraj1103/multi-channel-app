import hashlib
import hmac
import time
from fastapi import HTTPException

from app.config import settings

def verify_slack_request(headers, body):
    timestamp = headers.get("X-Slack-Request-Timestamp")
    if abs(time.time() - int(timestamp)) > 60 * 5:
        raise HTTPException(status_code=400, detail="Request timestamp expired")

    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"

    computed_signature = (
        "v0=" + hmac.new(
            key=settings.slack_signing_secret.encode('utf-8'),  # Ensure the signing secret is encoded to bytes
            msg=sig_basestring.encode('utf-8'),  # Ensure the base string is encoded to bytes
            digestmod=hashlib.sha256  # Use SHA256 hashing
        ).hexdigest()
    )

    print(computed_signature,"computed_signature")
    slack_signature = headers.get("X-Slack-Signature")
    if not slack_signature:
        raise HTTPException(status_code=400, detail="Missing Slack signature")
    print(slack_signature,"slack_signature")

    if not hmac.compare_digest(computed_signature, slack_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
