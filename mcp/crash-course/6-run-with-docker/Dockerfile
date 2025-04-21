FROM python:3.11-slim

WORKDIR /app

# install uv 
RUN pip install uv

COPY requirements.txt .

RUN uv venv
RUN uv pip install -r requirements.txt

COPY server.py .
COPY client.py .

# Expose the port the server runs on
EXPOSE 8050

# Run the server
CMD ["uv", "run", "server.py"]
