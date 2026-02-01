"""ID generator utility."""

import uuid
from datetime import datetime


class IdGenerator:
    """Utility for generating unique IDs."""

    @staticmethod
    def generate_post_id() -> str:
        """Generate a unique post ID.

        Returns:
            Post ID string in format: post_{timestamp}_{uuid}
        """
        timestamp = int(datetime.utcnow().timestamp())
        unique_id = uuid.uuid4().hex[:8]
        return f"post_{timestamp}_{unique_id}"

    @staticmethod
    def generate_reply_id() -> str:
        """Generate a unique reply ID.

        Returns:
            Reply ID string in format: reply_{timestamp}_{uuid}
        """
        timestamp = int(datetime.utcnow().timestamp())
        unique_id = uuid.uuid4().hex[:8]
        return f"reply_{timestamp}_{unique_id}"
