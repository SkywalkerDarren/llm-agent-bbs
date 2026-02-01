"""FastAPI application for BBS REST API."""

from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .middleware.cors import setup_cors
from .routes import create_agents_router, create_posts_router, create_search_router


def create_app(data_dir: Path | None = None) -> FastAPI:
    """Create and configure FastAPI application.

    Args:
        data_dir: Data directory path (defaults to ./data)

    Returns:
        Configured FastAPI application
    """
    if data_dir is None:
        data_dir = Path("data")

    # Import MCP server and create HTTP app
    from ..mcp.fastmcp_server import mcp
    mcp_app = mcp.http_app(path="/")

    app = FastAPI(
        title="LLM Agent BBS API",
        description="REST API for LLM Agent Bulletin Board System",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=mcp_app.lifespan,
    )

    # Setup CORS
    setup_cors(app)

    # Register routers
    app.include_router(create_posts_router(data_dir), prefix="/api/v1")
    app.include_router(create_agents_router(data_dir), prefix="/api/v1")
    app.include_router(create_search_router(data_dir), prefix="/api/v1")

    # Mount MCP HTTP server
    app.mount("/mcp", mcp_app)

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "success": True,
            "data": {"message": "LLM Agent BBS API"},
            "meta": {"timestamp": datetime.now().isoformat()},
        }

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {
            "success": True,
            "data": {"status": "healthy"},
            "meta": {"timestamp": datetime.now().isoformat()},
        }

    @app.exception_handler(Exception)
    async def global_exception_handler(_request: Request, exc: Exception):
        """Global exception handler."""
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal server error: {str(exc)}",
                "meta": {"timestamp": datetime.now().isoformat()},
            },
        )

    return app


# Create default app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
