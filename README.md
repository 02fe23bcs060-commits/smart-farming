# AgriSmart — Smart Farming Web Application

AI-powered agricultural decision support for farmers: crop selection, fertilizer plans, irrigation scheduling, and weather-based alerts. Built for sustainable farming, water conservation, and data-driven productivity.

## Features

| Feature | Description |
|---------|-------------|
| **Farm input form** | Soil type, season, temperature, water availability, land size |
| **Crop AI engine** | Weighted multi-factor scoring across 15+ crops |
| **Fertilizer advisor** | NPK ratios, organic options, soil amendments per crop |
| **Irrigation planner** | Weekly schedule, daily water estimates, conservation tips |
| **Weather insights** | Rainfall alerts, heat/frost warnings via Open-Meteo |
| **History DB** | PostgreSQL stores farmers, inputs, and recommendation history |
| **Roadmap** | Disease detection, market prices, i18n, IoT sensors (extensible API) |

## Tech stack

- **Frontend:** Next.js 15, React 19, Tailwind CSS
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **DevOps:** Docker Compose, Jenkins, Ansible, AWS EC2, GitHub

## Quick start (Docker)

```bash
cd smart-farming
cp .env.example .env
docker compose up --build
```

- Web UI: http://localhost:3000
- API: http://localhost:8000
- API docs: http://localhost:8000/docs

## Local development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
# Start PostgreSQL or use docker compose up db -d
set DATABASE_URL=postgresql://agri_user:agri_pass@localhost:5432/smart_farming
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
set NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

### Tests

```bash
cd backend && pytest -q
```

## API examples

```bash
curl -X POST http://localhost:8000/api/recommendations/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "farmer_name": "Demo Farmer",
    "soil_type": "loam",
    "season": "kharif",
    "temperature_c": 28,
    "water_availability": "medium",
    "land_size_acres": 2.5
  }'
```

## Project structure

```
smart-farming/
├── backend/          # FastAPI + AI engines + PostgreSQL models
├── frontend/         # Next.js farmer UI
├── ansible/          # EC2 provisioning and deploy
├── docs/             # AWS deployment guide
├── docker-compose.yml
├── Jenkinsfile
└── README.md
```

## GitHub collaboration

1. Create a GitHub organization or repo
2. Push this project: `git push -u origin main`
3. Use branch protection and pull requests for team workflow
4. Connect Jenkins to the repo webhook for CI/CD

## CI/CD (Jenkins)

The `Jenkinsfile` runs:

1. Backend unit tests (`pytest`)
2. Frontend production build
3. Docker image build (on `main`)
4. Optional registry push
5. Ansible deploy to EC2

Configure Jenkins credentials: `docker-hub-credentials`, and set `IMAGE_PREFIX` / `GIT_REPO_URL` environment variables.

## AWS + Ansible

See [docs/AWS_DEPLOYMENT.md](docs/AWS_DEPLOYMENT.md) for EC2 setup, security groups, and Ansible playbook usage.

## Future enhancements

The `/api/features/roadmap` endpoint documents planned modules:

- Crop disease detection (image ML)
- Market price prediction
- Multilingual UI
- IoT sensor integration (MQTT)

Architecture uses separate service modules so each can be upgraded independently.

## License

MIT — use freely for education and agricultural extension projects.
