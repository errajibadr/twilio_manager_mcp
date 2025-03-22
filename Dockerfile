FROM python:3.12-slim

WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh 

COPY --from=ghcr.io/astral-sh/uv:0.6.9 /uv /uvx /bin/

# Copy project files first
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv sync --frozen

# Copy the rest of the application
COPY . .

# Add virtual environment to PATH
# ENV VIRTUAL_ENV=/app/.venv
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
ENTRYPOINT ["uv", "run", "twilio_manager_mcp_sse.py"]
CMD ["--host", "0.0.0.0", "--port", "8000"]