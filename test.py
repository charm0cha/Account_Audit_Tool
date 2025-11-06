from datetime import datetime, timezone

created_at = "2025-09-25T10:22:33.123Z"

created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
now = datetime.now(timezone.utc)

age_days = (now - created).days
print(age_days)
