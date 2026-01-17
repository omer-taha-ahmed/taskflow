# TaskFlow Backend

Python HTTP server - zero external dependencies.

## Run Locally
```bash
python3 server.py
```

## API Endpoints

### Health Check
```http
GET /health

Response:
{
  "status": "ok",
  "message": "Backend running!",
  "service": "taskflow-backend"
}
```

### API Test
```http
GET /api/test

Response:
{
  "status": "success",
  "message": "API is working!",
  "version": "1.0.0"
}
```

## Deploy to EC2
```bash
# SSH to EC2
ssh -i key.pem ubuntu@EC2_IP

# Create directory
sudo mkdir -p /opt/taskflow
sudo chown ubuntu:ubuntu /opt/taskflow
cd /opt/taskflow

# Copy server.py
# Run server
python3 server.py &
```

## Testing
```bash
curl http://localhost:5000/health
curl http://localhost:5000/api/test
```

See [../docs/IMPLEMENTATION.md](../docs/IMPLEMENTATION.md) for full deployment guide.