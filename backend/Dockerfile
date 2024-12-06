FROM python:3.10-slim

WORKDIR /backend

COPY requirements.txt .

RUN apt-get update && apt-get install -y curl
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /

CMD ["python", "-m", "backend.app.main"]