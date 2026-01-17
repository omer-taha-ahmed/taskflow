# TaskFlow: Complete Implementation Guide

Step-by-step AWS deployment with zero spending.

## Prerequisites

- AWS Account (free tier eligible)
- Your computer with PowerShell/Terminal
- Internet connection
- ~1 hour for setup

**Have ready:**
- Notepad for saving important values
- AWS Console access
- Key file location for EC2

---

## PHASE 1: Create VPC & Network Infrastructure

### Step 1.1: Create VPC

**AWS Console:**
1. Services → VPC
2. Click "Create VPC"

**Configuration:**
Name: taskflow-vpc
IPv4 CIDR: 10.0.0.0/16
IPv6: (leave empty)

**Verify:** Green banner "VPC created successfully"

---

### Step 1.2: Create Public Subnet 1

**AWS Console:**
1. VPC → Subnets
2. Click "Create subnet"

**Configuration:**
VPC: taskflow-vpc
Subnet name: taskflow-public-subnet-1
Availability Zone: us-east-1a
IPv4 CIDR: 10.0.1.0/24

**Verify:** Green banner

**CRITICAL:** This is in us-east-1a

---

### Step 1.3: Create Public Subnet 2

**AWS Console:**
1. VPC → Subnets
2. Click "Create subnet"

**Configuration:**
VPC: taskflow-vpc
Subnet name: taskflow-public-subnet-2
Availability Zone: us-east-1b (DIFFERENT!)
IPv4 CIDR: 10.0.4.0/24 (DIFFERENT CIDR!)

**Verify:** Green banner

**CRITICAL:**
- Must be us-east-1b, NOT us-east-1a
- Must be 10.0.4.0/24, NOT 10.0.1.0/24
- ALB requires 2 subnets in different AZs

---

### Step 1.4: Create Private Subnet

**AWS Console:**
1. VPC → Subnets
2. Click "Create subnet"

**Configuration:**
VPC: taskflow-vpc
Subnet name: taskflow-private-subnet
Availability Zone: us-east-1c (DIFFERENT from both!)
IPv4 CIDR: 10.0.2.0/24

**Verify:** Green banner

**Note:** This won't have internet access (intentional for database security)

---

### Step 1.5: Create Internet Gateway

**AWS Console:**
1. VPC → Internet Gateways
2. Click "Create internet gateway"

**Configuration:**
Name: taskflow-igw

**Attach to VPC:**
1. Click "Attach to VPC"
2. Select VPC: taskflow-vpc
3. Click "Attach"

**Verify:** Status changes from "Detached" to "Attached"

---

### Step 1.6: Configure Route Table (CRITICAL!)

**AWS Console:**
1. VPC → Route Tables
2. Find route table associated with taskflow-vpc
3. Click on it

**Check current routes:**
10.0.0.0/16 → local (should already exist)

**Add internet route:**
1. Click "Routes" tab
2. Click "Edit routes"
3. Click "Add route"

**Settings:**
Destination: 0.0.0.0/0
Target: Internet Gateway → taskflow-igw

4. Click "Save routes"

**Verify routes:**
10.0.0.0/16 → local (internal traffic)
0.0.0.0/0 → taskflow-igw (external traffic)

**Associate with public subnets:**
1. Click "Subnet associations" tab
2. Click "Edit subnet associations"
3. CHECK BOTH:
   - taskflow-public-subnet-1
   - taskflow-public-subnet-2
4. Click "Save associations"

**IMPORTANT:** Do NOT associate taskflow-private-subnet

---

## PHASE 2: Create Security Groups

### Step 2.1: Create ALB Security Group

**AWS Console:**
1. EC2 → Security Groups
2. Click "Create security group"

**Basic Details:**
Name: taskflow-alb-sg
Description: ALB security group
VPC: taskflow-vpc

**Inbound Rules:**

**Rule 1 - HTTP:**
Type: HTTP
Port: 80
Source: 0.0.0.0/0
Description: Allow HTTP from internet

**Rule 2 - HTTPS:**
Type: HTTPS
Port: 443
Source: 0.0.0.0/0
Description: Allow HTTPS from internet

**Outbound:** Leave default (allow all)

**Create security group**

**Verify:** Green banner

---

### Step 2.2: Create EC2 Security Group

**AWS Console:**
1. EC2 → Security Groups
2. Click "Create security group"

**Basic Details:**
Name: taskflow-ec2-sg
Description: EC2 security group
VPC: taskflow-vpc

**Inbound Rules:**

**Rule 1 - From ALB:**
Type: Custom TCP
Port: 5000
Source Type: Security group
Source: taskflow-alb-sg (SELECT FROM DROPDOWN!)
Description: Allow from ALB

**Rule 2 - SSH:**
Type: SSH
Port: 22
Source: 0.0.0.0/0
Description: SSH admin access

**Outbound:** Leave default

**Create security group**

---

### Step 2.3: Create RDS Security Group

**AWS Console:**
1. EC2 → Security Groups
2. Click "Create security group"

**Basic Details:**
Name: taskflow-rds-sg
Description: RDS security group
VPC: taskflow-vpc

**Inbound Rules:**

**Rule 1 - From EC2:**
Type: PostgreSQL
Port: 5432
Source Type: Security group
Source: taskflow-ec2-sg
Description: Allow from EC2

**Outbound:** Leave default

**Create security group**

---

## PHASE 3: Launch EC2 Instance

### Step 3.1: Launch EC2

**AWS Console:**
1. EC2 → Instances
2. Click "Launch instances"

**Name:**
taskflow-server

**Application and OS Images:**
Ubuntu Server 24.04 LTS (Free tier eligible)

**Instance Type:**
t3.micro

**Key Pair:**
Click "Create new key pair"
Name: taskflow-key
Type: RSA
Format: .pem
(File downloads - SAVE IT!)

**Network Settings:**
VPC: taskflow-vpc
Subnet: taskflow-public-subnet-1 (PUBLIC!)
Auto-assign public IP: Enable
Security group: taskflow-ec2-sg

**Storage:**
Type: gp3
Size: 30 GB
Delete on termination: ✓
Encrypted: ✓

**Click "Launch instances"**

**Verify:**
- Green banner
- Wait 2-3 minutes for "Running" state
- **SAVE:** Copy Public IPv4 address (for SSH)

---

## PHASE 4: Create Application Load Balancer

### Step 4.1: Create Target Group First

**AWS Console:**
1. EC2 → Target Groups
2. Click "Create target group"

**Configuration:**
Target type: Instances
Name: taskflow-targets
Protocol: HTTP
Port: 5000
VPC: taskflow-vpc

**Health Check:**
Protocol: HTTP
Path: /health
Healthy threshold: 2
Unhealthy threshold: 2
Timeout: 5 seconds
Interval: 30 seconds
Success codes: 200

**Register Targets:**
1. Select taskflow-server instance
2. Click "Include as pending below"
3. Click "Create target group"

**Verify:** Green banner

---

### Step 4.2: Create ALB

**AWS Console:**
1. EC2 → Load Balancers
2. Click "Create load balancer"
3. Select "Application Load Balancer"

**Configuration:**
Name: taskflow-alb
Scheme: Internet-facing
IP address type: IPv4

**Network Mapping:**
VPC: taskflow-vpc
Subnets: CHECK BOTH:
☑ us-east-1a (taskflow-public-subnet-1)
☑ us-east-1b (taskflow-public-subnet-2)

**Security Groups:**
Remove: default
Add: taskflow-alb-sg

**Listeners:**
HTTP:80 → Forward to: taskflow-targets

**Click "Create load balancer"**

**Wait:** 1-2 minutes for "Active" state

**SAVE:** Copy ALB DNS name (like: taskflow-alb-123456.us-east-1.elb.amazonaws.com)

---

## PHASE 5: Deploy Backend

### Step 5.1: Connect to EC2

**PowerShell:**
```powershell
cd C:\Users\omar4\Downloads\taskflow
ssh -i taskflow-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

**Expected:**
Welcome to Ubuntu 24.04 LTS
ubuntu@ip-10-0-1-xxx:~$

---

### Step 5.2: Create Application Directory

**In SSH terminal:**
```bash
sudo mkdir -p /opt/taskflow
sudo chown ubuntu:ubuntu /opt/taskflow
cd /opt/taskflow
pwd
```

**Expected:** `/opt/taskflow`

---

### Step 5.3: Create Backend Server

**In SSH terminal:**
```bash
cat > server.py << 'EOF'
#!/usr/bin/env python3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

class TaskFlowHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/health':
            response = {'status': 'ok', 'message': 'Backend running!', 'service': 'taskflow-backend'}
        elif self.path == '/api/test':
            response = {'status': 'success', 'message': 'API is working!', 'version': '1.0.0'}
        else:
            self.send_response(404)
            response = {'error': 'Endpoint not found'}
        
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    PORT = 5000
    server = HTTPServer(('0.0.0.0', PORT), TaskFlowHandler)
    print(f'[TaskFlow] Server running on port {PORT}')
    print(f'[TaskFlow] Health: GET http://localhost:{PORT}/health')
    server.serve_forever()
EOF
```

**Verify:**
```bash
head -10 server.py
```

---

### Step 5.4: Start Backend

**In SSH:**
```bash
python3 server.py &
```

**Expected:**
[TaskFlow] Server running on port 5000
[TaskFlow] Health: GET http://localhost:5000/health

---

### Step 5.5: Test Backend

**Open NEW SSH terminal:**
```bash
ssh -i taskflow-key.pem ubuntu@YOUR_EC2_IP
curl http://localhost:5000/health
```

**Expected:**
```json
{"status": "ok", "message": "Backend running!", "service": "taskflow-backend"}
```

✅ Backend works!

---

## PHASE 6: Deploy Frontend

### Step 6.1: Create S3 Bucket

**AWS Console:**
1. S3 → Create bucket

**Configuration:**
Name: taskflow-frontend-YOUR-UNIQUE-NAME
(Example: taskflow-frontend-omar-2026)
Region: us-east-1
Block all public access: UNCHECK

**Create bucket**

---

### Step 6.2: Enable Static Website Hosting

**AWS Console:**
1. S3 → Click bucket
2. Properties tab
3. Scroll to "Static website hosting"
4. Click "Edit"

**Settings:**
Enable: ✓
Index document: index.html
Error document: index.html

### Step 6.3: Make Bucket Public

**Bucket Policy:**
1. S3 → Bucket → Permissions tab
2. Scroll to "Bucket policy"
3. Click "Edit"

**Paste this (replace YOUR_BUCKET_NAME):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    }
  ]
}
```

**Save changes**

---

### Step 6.4: Upload Frontend

Create `index.html` on your computer with the complete frontend code (see frontend/index.html in this repo).

**Upload to S3:**
1. S3 → Bucket → Upload
2. Drag index.html
3. Upload

---

### Step 6.5: Create CloudFront Distribution

**AWS Console:**
1. CloudFront → Create distribution

**Configuration:**
Origin domain: YOUR_BUCKET_NAME.s3.us-east-1.amazonaws.com
(Use bucket domain, NOT website endpoint!)
Viewer protocol: Redirect HTTP to HTTPS
Cache policy: CachingOptimized

**Create distribution**

**Wait:** 5-10 minutes for "Deployed"

**SAVE:** Copy CloudFront domain name

---

## PHASE 7: Test Everything

### Test 1: Backend (Local)
```bash
# In EC2 SSH
curl http://localhost:5000/health
```

**Expected:** `{"status": "ok", ...}`

✅ Backend works locally

---

### Test 2: Backend via ALB
```powershell
# From your computer
curl http://YOUR_ALB_DNS/health
```

**Expected:** Same JSON

✅ ALB routing works

---

### Test 3: Frontend via S3
Open browser:
http://YOUR_BUCKET_NAME.s3-website-us-east-1.amazonaws.com

✅ Frontend loads

---

### Test 4: Frontend via CloudFront
Open browser:
https://YOUR_CLOUDFRONT_DOMAIN

✅ Everything works!

---

## PHASE 8: Cleanup (Zero Spending)

### Step 8.1: Terminate EC2
1. EC2 → Instances
2. Right-click taskflow-server
3. Terminate instance

### Step 8.2: Delete ALB
1. EC2 → Load Balancers
2. Select taskflow-alb
3. Actions → Delete

### Step 8.3: Delete Target Group
1. EC2 → Target Groups
2. Select taskflow-targets
3. Actions → Delete

### Step 8.4: Empty & Delete S3
1. S3 → Select bucket
2. Empty
3. Delete bucket

### Step 8.5: Delete CloudFront
1. CloudFront → Select distribution
2. Disable
3. Wait → Delete

### Step 8.6: Delete VPC
1. VPC → Your VPCs
2. Select taskflow-vpc
3. Delete VPC (auto-deletes associated resources)

**Verify all deleted = $0 spending!**

---

## Summary

✅ VPC with proper networking  
✅ Security groups (layered firewall)  
✅ EC2 instance (Python backend)  
✅ ALB (load balancer)  
✅ S3 + CloudFront (frontend)  
✅ Production architecture  

**You built a production-ready AWS application!** 🎉