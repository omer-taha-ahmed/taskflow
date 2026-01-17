# TaskFlow: Complete Architecture Explanation

## The Problem TaskFlow Solves

Teams need real-time task management without expensive solutions like Jira or Asana. TaskFlow demonstrates professional AWS architecture while remaining completely free-tier eligible.

## Core Features

- Create/assign/complete tasks
- Real-time collaboration (future: WebSocket)
- Activity logging
- Team management
- Zero external dependencies
- Production-ready AWS infrastructure

---

## Architecture Diagram
┌─────────────┐
│    Users    │
└──────┬──────┘
│
▼
┌──────────────────┐
│  CloudFront CDN  │ (200+ edge locations globally)
└────────┬─────────┘
│
┌────┴─────┐
│          │
▼          ▼
┌─────┐   ┌─────────┐
│ S3  │   │   ALB   │ (Port 80/443)
│HTML │   │         │
└─────┘   └────┬────┘
│
┌──────┴──────┐
│             │
▼             ▼
┌──────────────┐ ┌──────────────┐
│PUBLIC SUBNET1│ │PUBLIC SUBNET2│
│ us-east-1a   │ │ us-east-1b   │
│              │ │              │
│ ┌──────────┐ │ │              │
│ │   EC2    │ │ │  (ALB spans  │
│ │ Python   │ │ │   both AZs)  │
│ │ Port 5000│ │ │              │
│ └────┬─────┘ │ │              │
└──────┼───────┘ └──────────────┘
│
▼
┌──────────────┐
│PRIVATE SUBNET│
│ us-east-1c   │
│              │
│ ┌──────────┐ │
│ │   RDS    │ │
│ │PostgreSQL│ │
│ │ Port 5432│ │
│ └──────────┘ │
└──────────────┘
Monitoring (Always Active):
├─ CloudWatch (Logs, Metrics, Alarms)
└─ CloudTrail (API Audit Trail)

---

## AWS Services: Why Each One?

### 1. VPC (Virtual Private Cloud) - $0

**What:** Isolated network inside AWS (like your own private internet)

**Why:**
- Security isolation from other AWS users
- Complete control over network traffic
- Required foundation for all other services
- Industry best practice

**Configuration:**
- CIDR: 10.0.0.0/16
- Provides 65,536 IP addresses
- Isolated from internet by default

---

### 2. Subnets - $0

**What:** Smaller networks inside VPC

**Why 2 PUBLIC Subnets:**
- ALB requires minimum 2 subnets in different Availability Zones
- High availability: if us-east-1a fails, us-east-1b continues
- Professional redundancy
- Load balancing across zones

**Public Subnet 1:**
- CIDR: 10.0.1.0/24 (256 IPs)
- AZ: us-east-1a
- Hosts: EC2, part of ALB

**Public Subnet 2:**
- CIDR: 10.0.4.0/24 (256 IPs)
- AZ: us-east-1b
- Hosts: Part of ALB

**Why 1 PRIVATE Subnet:**
- Database security
- No direct internet access
- Only EC2 can connect
- Best practice for sensitive data

**Private Subnet:**
- CIDR: 10.0.2.0/24
- AZ: us-east-1c
- Hosts: RDS PostgreSQL

---

### 3. Internet Gateway (IGW) - $0

**What:** Gateway between VPC and internet

**Why:**
- Without it: VPC is completely isolated (island with no bridge)
- With it: Public subnets can reach internet
- ALB receives traffic from users
- EC2 can download updates

**Critical:** Must be attached to VPC AND route table must point to it

---

### 4. Route Tables - $0

**What:** Traffic routing rules

**Public Route Table:**
10.0.0.0/16 → local (internal VPC traffic)
0.0.0.0/0 → IGW (all other traffic to internet)

**Private Route Table:**
10.0.0.0/16 → local (internal VPC traffic only)
(No internet route = secure)

**Why Critical:**
- Without 0.0.0.0/0 → IGW route, public subnet isn't truly public
- This mistake causes "EC2 can't reach internet" errors

---

### 5. Security Groups - $0

**What:** Virtual firewalls controlling traffic

**ALB Security Group:**
- Inbound: 80 (HTTP) from 0.0.0.0/0 (internet)
- Inbound: 443 (HTTPS) from 0.0.0.0/0 (internet)
- Outbound: All traffic (default)
- Purpose: Let users access application

**EC2 Security Group:**
- Inbound: 5000 from ALB-SG ONLY (not internet!)
- Inbound: 22 (SSH) from 0.0.0.0/0 (admin access)
- Outbound: All traffic
- Purpose: Hidden from internet, only ALB connects

**RDS Security Group:**
- Inbound: 5432 from EC2-SG ONLY
- Outbound: All traffic
- Purpose: Database completely hidden, only EC2 connects

**Why Layered:**
- Defense in depth
- If ALB breached → EC2 still protected
- If EC2 breached → RDS still protected
- Industry security standard

---

### 6. Application Load Balancer (ALB) - $16.20/month

**What:** Smart traffic distributor

**Why ALB:**
- Distributes traffic across multiple EC2 instances
- Health checks every 30 seconds
- Automatic failover if EC2 unhealthy
- Terminates HTTPS/SSL (encryption)
- Enables auto-scaling
- Professional production setup

**Why NOT Network Load Balancer:**
- NLB: For extreme performance (millions requests/sec)
- ALB: For web apps (HTTP/HTTPS) - our use case
- ALB: Cheaper for this workload

**Why NOT Direct EC2:**
- No redundancy (single point of failure)
- Can't scale easily
- No health checks
- Not professional

**Configuration:**
- Scheme: Internet-facing
- Listeners: HTTP:80
- Spans: 2 public subnets (us-east-1a, us-east-1b)
- Target: EC2 port 5000
- Health check: /health endpoint

**Cost:**
- $16.20/month (unavoidable for production)
- Only unavoidable cost in architecture
- Worth it for reliability

---

### 7. EC2 Instance (t3.micro) - $0

**What:** Virtual server in the cloud

**Instance Type: t3.micro**
- 2 vCPUs
- 1 GB RAM
- Burstable (handles traffic spikes)
- Free tier: 750 hours/month = 24/7 = $0
- After free tier: ~$8/month

**Why EC2 NOT Lambda:**
- Lambda: Stateless, spins up/down
- Lambda: Can't maintain WebSocket connections
- Lambda: Cold starts (latency)
- EC2: Always running = instant response
- EC2: Full control over environment

**Why EC2 NOT Heroku/Managed:**
- Learning: Understand infrastructure
- Cost: EC2 cheaper for this workload
- Control: Full customization
- Portfolio: Shows cloud skills

**Configuration:**
- OS: Ubuntu 24.04 LTS
- Subnet: Public Subnet 1 (CRITICAL!)
- Auto-assign public IP: Enabled
- Security Group: EC2-SG

---

### 8. S3 Bucket - $0

**What:** Infinitely scalable object storage

**Why S3:**
- Static files (HTML, CSS, JS) stored here
- No server needed to serve files
- Infinitely scalable
- Extremely cheap ($0 for 5GB free tier)
- CloudFront origin

**Why NOT Serve from EC2:**
- EC2 wastes compute on static files
- Can't scale globally
- More expensive
- EC2 should focus on API logic only

**Configuration:**
- Static website hosting: Enabled
- Public access: Enabled
- Bucket policy: Allow GetObject from *

---

### 9. CloudFront (CDN) - $0

**What:** Global Content Delivery Network (200+ edge locations)

**Why CloudFront:**
- Caches files at edge locations worldwide
- User in Tokyo → gets files from Japan (fast)
- User in London → gets files from UK (fast)
- Reduces load on S3
- DDoS protection included
- Free tier: 1TB data transfer/month

**Without CloudFront:**
- All users fetch from single S3 region (slow for distant users)
- Higher latency globally

**With CloudFront:**
- Files cached worldwide
- Fast for everyone
- Professional setup

**Configuration:**
- Origin: S3 bucket domain (NOT static website endpoint)
- Viewer protocol: Redirect HTTP → HTTPS
- Caching: Optimized

---

### 10. RDS PostgreSQL - $0

**What:** Managed relational database

**Why PostgreSQL:**
- Relational data (users, tasks, teams, relationships)
- ACID transactions (data consistency guaranteed)
- Mature, reliable, widely used
- Free tier available

**Why NOT SQLite:**
- Lives on EC2 disk
- If EC2 dies → data lost
- Can't scale
- No automated backups

**Why NOT DynamoDB:**
- DynamoDB: NoSQL (key-value)
- Our data: Relational (users → tasks → teams)
- DynamoDB: Overkill for this use case
- PostgreSQL: Better fit

**Why Managed RDS:**
- AWS handles backups automatically
- AWS handles patches/updates
- Multi-AZ failover available
- Read replicas for scaling
- Zero admin overhead

**Configuration:**
- Instance: t3.micro (free tier)
- Storage: 20GB (free tier)
- Subnet: Private (hidden from internet)
- Security Group: Only EC2 can connect

---

### 11. CloudWatch - $0

**What:** Monitoring and logging service

**Why CloudWatch:**
- See what's happening (metrics: CPU, memory, disk, network)
- Debug problems (logs from EC2, ALB)
- Alerts if something fails (email/SMS)
- Dashboards for visualization
- Required for production

**Metrics Tracked:**
- EC2: CPU, memory, disk, network
- ALB: Request count, latency, errors
- RDS: Connections, CPU, storage

**Without CloudWatch:**
- Blind (don't know if things work)
- Can't debug issues
- Find out from users when down

**Cost:**
- Free tier: Basic monitoring
- After: Minimal ($1-2/month)

---

### 12. CloudTrail - $0

**What:** API audit log (who did what, when)

**Why CloudTrail:**
- Records every AWS API call
- Security investigation
- Compliance requirement
- "Who deleted that database?"
- "Who changed security group?"

**Free Tier:**
- 90 days of history
- Enough for learning/small production

**Cost After:**
- $2 per 100,000 events

---

## Design Decisions Explained

### Why Public Subnets for EC2?

**Decision:** EC2 in PUBLIC subnet (not private)

**Reasoning:**
1. Needs internet access for updates
2. Needs to receive traffic from ALB
3. ALB targets must be reachable
4. Simpler architecture for this use case

**Alternative:** EC2 in private + NAT Gateway
- More secure
- But costs $32/month (NAT Gateway)
- Overkill for learning project

---

### Why 2 Availability Zones?

**Decision:** Subnets in us-east-1a AND us-east-1b

**Reasoning:**
1. ALB requires minimum 2 AZs
2. High availability (redundancy)
3. If one datacenter fails, other continues
4. Industry best practice
5. Enables auto-scaling across zones

---

### Why ALB Not Direct EC2?

**Decision:** ALB in front of EC2

**Reasoning:**
1. Single point of failure eliminated
2. Health checks (auto-recovery)
3. Ready for scaling (add more EC2s)
4. Professional architecture
5. HTTPS termination
6. Future-proof

---

## Cost Breakdown

### Free Tier (12 months)

| Service | Free Tier | Value |
|---------|-----------|-------|
| EC2 t3.micro | 750 hours/month | 24/7 = $0 |
| RDS t3.micro | 750 hours/month | 24/7 = $0 |
| RDS Storage | 20GB | $0 |
| S3 | 5GB storage | $0 |
| CloudFront | 1TB transfer | $0 |
| CloudWatch | Basic monitoring | $0 |
| **Total** | | **$0** |

**Only Cost:** ALB at $16.20/month (unavoidable)

### After Free Tier

| Service | Monthly Cost |
|---------|--------------|
| EC2 t3.micro | ~$8 |
| RDS t3.micro | ~$15 |
| ALB | ~$16 |
| S3 + CloudFront | ~$1 |
| **Total** | **~$25** |

### Cleanup = $0

Delete all resources → Zero spending guaranteed

---

## Security Architecture

### Network Security (Layers)

**Layer 1: VPC Isolation**
- Isolated network (10.0.0.0/16)
- No access from other AWS accounts

**Layer 2: Subnet Segmentation**
- Public: Internet-accessible (ALB, EC2)
- Private: Hidden (RDS)

**Layer 3: Security Groups**
- ALB: Only 80, 443 from internet
- EC2: Only 5000 from ALB, 22 for admin
- RDS: Only 5432 from EC2

**Layer 4: IAM Roles**
- No hardcoded credentials
- Temporary credentials only
- Least privilege access

**Layer 5: Encryption**
- HTTPS at ALB (in transit)
- RDS encryption (at rest) - ready
- S3 encryption (at rest) - ready

---

## Scalability Architecture

### Current (Single Instance)
Users → ALB → 1 EC2 → RDS

### Future (Auto-Scaling)
Users → ALB → ┌─ EC2-1 ┐
├─ EC2-2 ├─→ RDS (Primary)
├─ EC2-3 ┘      ↓
└─ EC2-4      RDS (Read Replica)

**Easy to add:**
1. Create Auto Scaling Group
2. ALB automatically distributes traffic
3. Add RDS read replicas for database scaling

---

## Monitoring Strategy

### Metrics to Watch

**EC2:**
- CPU > 80% → Need larger instance or more instances
- Memory > 80% → Need more RAM
- Disk > 80% → Add storage

**ALB:**
- Request count → Traffic patterns
- Latency > 1s → Performance issue
- 5xx errors → Backend problems

**RDS:**
- CPU > 80% → Need larger instance
- Connections → Max connections approaching
- Storage → Disk filling up

### Alerts

**Critical:**
- EC2 down → Email + SMS
- RDS down → Email + SMS
- 5xx errors > 10/min → Email

**Warning:**
- CPU > 80% → Email
- Disk > 80% → Email

---

## Well-Architected Framework

### 1. Operational Excellence
✅ Infrastructure as Code ready (Terraform)
✅ CloudWatch monitoring
✅ CloudTrail auditing
✅ Automated health checks
✅ Runbooks documented

### 2. Security
✅ VPC network isolation
✅ Layered security groups
✅ HTTPS ready
✅ Encryption ready
✅ CloudTrail audit logging
✅ No hardcoded credentials

### 3. Reliability
✅ Multi-AZ deployment (ALB)
✅ Health checks every 30 seconds
✅ Auto-recovery on failure
✅ RDS backups configured
✅ No single point of failure

### 4. Performance Efficiency
✅ CloudFront CDN for caching
✅ Right-sized instances (t3.micro)
✅ Ready for auto-scaling
✅ Async operations ready

### 5. Cost Optimization
✅ Free tier maximized
✅ Right-sizing (not over-provisioned)
✅ Auto-scaling ready (pay for what you use)
✅ No unnecessary services

### 6. Sustainability
✅ Efficient resource usage
✅ No idle resources
✅ Proper monitoring
✅ Reproducible (IaC ready)

---

## Future Enhancements

### Phase 1: Database Integration
- Connect EC2 to RDS
- User authentication (JWT)
- Task persistence
- Real user management

### Phase 2: Real-Time Features
- WebSocket support (Socket.io)
- Real-time task updates
- Live collaboration
- Notifications

### Phase 3: Scaling
- Auto Scaling Group (multiple EC2s)
- RDS read replicas
- ElastiCache (Redis) for caching
- SQS for async tasks

### Phase 4: Advanced Features
- File uploads (S3)
- Email notifications (SES)
- Search (Elasticsearch)
- Analytics (Athena)

---

## Conclusion

This architecture demonstrates:
- Professional AWS design
- Well-Architected principles
- Production-ready infrastructure
- Cost optimization
- Security best practices
- Scalability planning

**Perfect for:**
- Learning AWS
- Portfolio projects
- Production applications
- Understanding cloud architecture

**Total Investment:**
- Time: ~1 hour setup
- Cost: $0 (free tier), ~$25/month after
- Learning: Priceless