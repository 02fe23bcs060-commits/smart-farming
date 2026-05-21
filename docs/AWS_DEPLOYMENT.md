# AWS EC2 Deployment Guide

## 1. Launch EC2 instance

- AMI: Ubuntu 22.04 LTS
- Instance type: `t3.small` (minimum) or `t3.medium` for production
- Security group inbound: 22 (SSH), 80, 443, 3000, 8000 (restrict to your IP where possible)
- Attach an Elastic IP for stable DNS

## 2. Push code to GitHub

```bash
git remote add origin https://github.com/YOUR_ORG/smart-farming.git
git add .
git commit -m "Initial smart farming application"
git push -u origin main
```

## 3. Configure Ansible inventory

Edit `ansible/inventory/production`:

- Set `ansible_host` to your EC2 public IP
- Set `ansible_ssh_private_key_file` to your `.pem` key path

## 4. Deploy with Ansible

```bash
export GIT_REPO_URL=https://github.com/YOUR_ORG/smart-farming.git
ansible-playbook -i ansible/inventory/production ansible/playbook.yml
```

## 5. Access the application

- Frontend: `http://<EC2_IP>:3000`
- API docs: `http://<EC2_IP>:8000/docs`

## 6. Jenkins CI/CD (optional)

1. Install Jenkins on a build server or EC2
2. Add credentials: `docker-hub-credentials`, GitHub SSH key
3. Create a Pipeline job pointing to this repo's `Jenkinsfile`
4. On `main` branch merges, Jenkins runs tests, builds images, and triggers Ansible deploy

## 7. Production hardening

- Put Nginx reverse proxy in front with TLS (Let's Encrypt)
- Use RDS PostgreSQL instead of container DB for scale
- Store secrets in AWS Secrets Manager
- Enable CloudWatch logs for containers
