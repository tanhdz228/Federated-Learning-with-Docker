
# Federated Learning Simulation with Docker and Flask

A Dockerized simulation of Federated Learning (FL) with a central server and multiple clients communicating via Flask APIs. Designed to handle updates across distributed nodes while addressing real-world challenges like network latency, compliance, and thread safety.

---

## Features
- **Dockerized Environment**: Isolated containers for the central server and clients.
- **Flask API Communication**: REST endpoints for model updates and aggregation.
- **Thread-Safe Aggregation**: Uses `Lock()` to handle concurrent client updates.
- **Multi-Region Simulation**: Clients and server can be customized for region-specific logic (GDPR, etc.).
- **Error Handling**: Robust validation and logging for debugging.

---

## Prerequisites
- Docker Engine and Docker Compose
- Python 3.8+
- `curl` (for testing)

---

## Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd fl-framework
```

### 2. Folder Structure
```
fl-framework/
├── central_server/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py
│   └── model.py
├── client/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── client.py
└── docker-compose.yml
```

---

## Usage

### 1. Build and Start Containers
```bash
docker-compose up --build -d
```

### 2. Trigger Training on Clients
```bash
# Trigger client1
docker exec -it fl-framework-client1-1 curl http://localhost:5000/train

# Trigger client2
docker exec -it fl-framework-client2-1 curl http://localhost:5000/train
```

### 3. Monitor Logs
```bash
# Central server logs
docker logs -f fl-framework-central-server-1

# Client logs (optional)
docker logs -f fl-framework-client1-1
```

---

## Customization

### Modify the Model
1. Update `central_server/model.py`:
   ```python
   def initialize_model():
       return np.random.rand(10)  # Example: 10-element model

   def aggregate_updates(updates):
       return np.median(updates, axis=0)  # Custom aggregation logic
   ```

2. Rebuild:
   ```bash
   docker-compose down && docker-compose up --build -d
   ```

### Add Region-Specific Logic
1. Create region-specific client folders (e.g., `eu-client/`, `asia-client/`).
2. Extend Docker Compose to include region-specific services.

