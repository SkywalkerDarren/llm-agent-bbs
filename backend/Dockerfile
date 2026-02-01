FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ ./src/

# Create data directory
RUN mkdir -p /app/data/posts /app/data/agents /app/data/index

# Initialize index files
RUN echo '{"posts": []}' > /app/data/index/posts_index.json && \
    echo '{"agents": []}' > /app/data/index/agents_index.json

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.interfaces.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
