# TaskFlow 🚀

**Production-Ready AWS Task Management Application**

[![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

## 📋 Overview

TaskFlow demonstrates **AWS Well-Architected Framework** principles with a production-grade task management application. Zero external dependencies, fully documented, completely free-tier eligible.

## 🏗️ Architecture
Users → CloudFront CDN → ALB → EC2 → RDS PostgreSQL
↓
S3 (Frontend)
↓
CloudWatch + CloudTrail

### AWS Services

| Service | Purpose | Cost |
|---------|---------|------|
| VPC | Network isolation | $0 |
| EC2 (t3.micro) | Application server | $0 (Free tier) |
| ALB | Load balancing | $16/month |
| S3 | Frontend hosting | $0 (Free tier) |
| CloudFront | Global CDN | $0 (Free tier) |
| RDS PostgreSQL | Database | $0 (Free tier) |
| CloudWatch | Monitoring | $0 (Free tier) |

**Total Cost:** $0 (first 12 months), ~$25/month after

## 🚀 Quick Start

### Prerequisites
- AWS Account (free tier)
- Python 3.12+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/omer-taha-ahmed/taskflow.git
cd taskflow
```

### 2. Run Backend Locally
```bash
cd backend
python3 server.py
```

### 3. Test Backend
```bash
curl http://localhost:5000/health
```

### 4. Open Frontend
```bash
cd ../frontend
# Open index.html in browser
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | AWS services & design decisions |
| [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) | Complete deployment guide |
| [backend/README.md](backend/README.md) | Backend documentation |
| [frontend/README.md](frontend/README.md) | Frontend documentation |

## 📂 Project Structure
taskflow/
├── backend/              # Python HTTP server
│   ├── server.py        # Main application
│   └── README.md        # Backend docs
├── frontend/             # HTML/CSS/JS app
│   ├── index.html       # Complete frontend
│   └── README.md        # Frontend docs
├── docs/                 # Documentation
│   ├── ARCHITECTURE.md   # Design explanation
│   └── IMPLEMENTATION.md # Deployment guide
├── infrastructure/       # AWS setup
│   └── aws-setup.md     # Manual setup steps
├── README.md             # This file
├── CONTRIBUTING.md       # Contribution guide
├── LICENSE               # MIT License
└── .gitignore            # Git ignore

## 🔗 API Endpoints
```http
GET /health
GET /api/test
```

## 💰 Cost Analysis

**Free Tier (12 months):** $0  
**After Free Tier:** ~$25/month  
**Cleanup:** Delete all resources = $0

## 🏆 What You'll Learn

✅ AWS Infrastructure Architecture  
✅ VPC with public/private subnets  
✅ Security groups (layered defense)  
✅ Load balancing & high availability  
✅ S3 + CloudFront CDN  
✅ Production deployment  
✅ Monitoring & logging  

## 🛠️ Deploy to AWS

See complete guide: [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md)

**Time:** ~1 hour  
**Result:** Production-ready app on AWS

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 License

MIT License - See [LICENSE](LICENSE)

## 👤 Author

**Omer Taha Ahmed**  
Cloud Solutions Architect  
🔗 [LinedIn](https://www.linkedin.com/in/omar-taha-ah/)

---

**Made with ❤️ for the AWS community**