"""API routes."""

from .agents import create_agents_router
from .posts import create_posts_router
from .search import create_search_router

__all__ = ["create_posts_router", "create_agents_router", "create_search_router"]
