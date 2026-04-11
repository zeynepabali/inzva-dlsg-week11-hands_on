# Dockerfile
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# Copy project files
COPY api.py .
COPY requirements.txt .

# Install dependencies using uv
RUN uv pip install --system -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
