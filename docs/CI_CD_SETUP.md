# CI/CD Pipeline Setup

Two options: **GitHub Actions** (recommended, free) or **Jenkins** (as in `Jenkinsfile`).

## Pipeline flow

```
git push → main
    → Run pytest (backend)
    → Build Docker images (API + Web)
    → Push to Docker Hub
    → (optional) Deploy on EC2
```

---

## Option A — GitHub Actions (easiest)

### 1. Docker Hub

1. Create account: https://hub.docker.com
2. Create repositories:
   - `YOUR_USERNAME/smart-farming-api`
   - `YOUR_USERNAME/smart-farming-web`
3. Account Settings → **Security** → **New Access Token** → copy token

### 2. GitHub secrets

Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Name | Value |
|------|--------|
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Access token (not account password) |

### 3. Push workflow file

The workflow is in `.github/workflows/ci-cd.yml`. Push to `main`:

```bash
git add .github/workflows/ci-cd.yml
git commit -m "Add GitHub Actions CI/CD"
git push
```

### 4. View pipeline

GitHub repo → **Actions** tab → see **Smart Farming CI/CD** runs.

### 5. Pull images on EC2

```bash
docker login
docker pull YOUR_USERNAME/smart-farming-api:latest
docker pull YOUR_USERNAME/smart-farming-web:latest
```

---

## Option B — Jenkins

### 1. Install Jenkins (Ubuntu EC2)

```bash
sudo apt update
sudo apt install -y openjdk-17-jdk git
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list
sudo apt update && sudo apt install -y jenkins
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

Open: `http://EC2_IP:8080` (open port 8080 in security group).

### 2. Jenkins credentials

**Manage Jenkins → Credentials → Add**

- ID: `docker-hub-credentials`
- Username + Docker Hub token

### 3. Create Pipeline job

- **New Item** → `smart-farming` → **Pipeline**
- **Pipeline script from SCM** → Git
- URL: `https://github.com/02fe23bcs060-commits/smart-farming.git`
- Branch: `main`
- Script Path: `Jenkinsfile`

### 4. Environment variable

In job **Configure** → add:

- `IMAGE_PREFIX` = `YOUR_DOCKERHUB_USERNAME/smart-farming`

### 5. Trigger

- **Poll SCM**: `H/5 * * * *`  
  or GitHub webhook → `http://JENKINS_IP:8080/github-webhook/`

---

## For viva

> "CI/CD automates testing and deployment. On every push to `main`, we run **pytest**, build **Docker images**, and push to **Docker Hub**. Production runs on **AWS EC2** with `docker compose`."

---

## Files in this project

| File | Purpose |
|------|---------|
| `.github/workflows/ci-cd.yml` | GitHub Actions pipeline |
| `Jenkinsfile` | Jenkins pipeline |
| `ansible/playbook.yml` | Optional EC2 deploy |
