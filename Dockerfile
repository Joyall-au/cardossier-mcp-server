FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN pip install --no-cache-dir .

# stdio MCP server; runs keyless (demo tier) unless CARDOSSIER_API_KEY is set
ENTRYPOINT ["cardossier-mcp"]
