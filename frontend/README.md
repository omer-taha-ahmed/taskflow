# TaskFlow Frontend

Single-page HTML/CSS/JavaScript application.

## Features

- Real-time backend health monitoring
- Task management (create, complete, delete)
- Responsive design
- Zero dependencies (vanilla JS)
- Beautiful gradient UI

## Configuration

Edit `index.html` line 119:
```javascript
const API_BASE_URL = 'http://YOUR_ALB_DNS';
```

Replace with your actual ALB DNS after deployment.

## Local Testing
```bash
# Open in browser
open index.html

# Or use Python server
python3 -m http.server 8000
```

## Deploy to S3

1. Create S3 bucket
2. Upload index.html
3. Enable static website hosting
4. Create CloudFront distribution

See [../docs/IMPLEMENTATION.md](../docs/IMPLEMENTATION.md) for complete guide.