FROM python:3.12.2-alpine3.19

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install deps - Fixed: uv sync is the right command
RUN uv sync --frozen --no-dev

# Copy app
COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]