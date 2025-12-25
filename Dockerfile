FROM --platform=linux/arm64 ghcr.io/astral-sh/uv:python3.11-bookworm-slim

LABEL maintainer="Triumph"

WORKDIR /app

COPY . /app

RUN uv sync --frozen --no-cache

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
