# AWS Manual Setup Steps

For automated setup (future), see Terraform code (coming soon).

For manual setup, see complete guide:
[../docs/IMPLEMENTATION.md](../docs/IMPLEMENTATION.md)

## Quick Reference

### VPC
- CIDR: 10.0.0.0/16
- Name: taskflow-vpc

### Subnets
- Public 1: 10.0.1.0/24 (us-east-1a)
- Public 2: 10.0.4.0/24 (us-east-1b)
- Private: 10.0.2.0/24 (us-east-1c)

### Security Groups
- ALB: 80, 443 from 0.0.0.0/0
- EC2: 5000 from ALB-SG, 22 from 0.0.0.0/0
- RDS: 5432 from EC2-SG

### EC2
- Instance: t3.micro
- OS: Ubuntu 24.04 LTS
- Subnet: Public 1
- Auto-assign IP: Yes

### ALB
- Name: taskflow-alb
- Subnets: Both public subnets
- Target: EC2 port 5000

See full guide for step-by-step instructions.