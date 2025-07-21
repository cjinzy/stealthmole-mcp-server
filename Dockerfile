FROM ghcr.io/astral-sh/uv:0.8-python3.12-alpine

# Set working directory
WORKDIR /app

COPY . .

RUN uv sync

RUN pip install -e .

CMD ["python", "-m", "stealthmole_mcp.server"]
