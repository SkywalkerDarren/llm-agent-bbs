"""Domain exceptions for posts."""


class PostException(Exception):
    """Base exception for post-related errors."""

    pass


class PostNotFoundException(PostException):
    """Raised when a post is not found."""

    def __init__(self, post_id: str) -> None:
        """Initialize exception.

        Args:
            post_id: ID of the post that was not found
        """
        super().__init__(f"Post '{post_id}' not found")
        self.post_id = post_id


class PostAlreadyDeletedException(PostException):
    """Raised when trying to delete an already deleted post."""

    def __init__(self, post_id: str) -> None:
        """Initialize exception.

        Args:
            post_id: ID of the post that is already deleted
        """
        super().__init__(f"Post '{post_id}' is already deleted")
        self.post_id = post_id


class UnauthorizedPostDeletionException(PostException):
    """Raised when an agent tries to delete a post they don't own."""

    def __init__(self, post_id: str, agent_name: str) -> None:
        """Initialize exception.

        Args:
            post_id: ID of the post
            agent_name: Name of the agent attempting deletion
        """
        super().__init__(f"Agent '{agent_name}' cannot delete post '{post_id}'")
        self.post_id = post_id
        self.agent_name = agent_name


class ReplyNotFoundException(PostException):
    """Raised when a reply is not found."""

    def __init__(self, reply_id: str) -> None:
        """Initialize exception.

        Args:
            reply_id: ID of the reply that was not found
        """
        super().__init__(f"Reply '{reply_id}' not found")
        self.reply_id = reply_id


class UnauthorizedReplyDeletionException(PostException):
    """Raised when an agent tries to delete a reply they don't own."""

    def __init__(self, reply_id: str, agent_name: str) -> None:
        """Initialize exception.

        Args:
            reply_id: ID of the reply
            agent_name: Name of the agent attempting deletion
        """
        super().__init__(f"Agent '{agent_name}' cannot delete reply '{reply_id}'")
        self.reply_id = reply_id
        self.agent_name = agent_name
