FROM python:3.11

WORKDIR /app

# --> install system deps + chromium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# --> install python deps
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --> copy project
COPY .. .

CMD ["python", "main.py"]