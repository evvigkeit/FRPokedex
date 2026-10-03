from datetime import datetime, timezone

def check_session_valid(expires: datetime) -> bool:
    expires = expires.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires:
        return False
    return True