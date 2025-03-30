FROM python:3.8-slim
WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY client.py .
CMD ["python3", "client.py"]