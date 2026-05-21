# Docker troubleshooting (Windows)

## Error: `500 Internal Server Error` on `dockerDesktopLinuxEngine`

This means **Docker Desktop is not running correctly** — not a bug in this project.

### Fix (try in order)

1. **Quit Docker Desktop fully**  
   System tray → Docker icon → **Quit Docker Desktop**

2. **Start Docker Desktop again**  
   Wait until the whale icon shows **"Docker Desktop is running"** (can take 1–2 minutes).

3. **Verify the engine**

   ```powershell
   docker version
   ```

   You must see both **Client** and **Server** sections. If Server is missing or you get 500 again, the engine is still broken.

4. **Restart WSL** (if you use WSL2 backend)

   ```powershell
   wsl --shutdown
   ```

   Then start Docker Desktop again.

5. **Clean and rebuild this project**

   ```powershell
   cd C:\Users\Keerti\Projects\smart-farming
   docker compose down
   docker builder prune -f
   docker compose build --no-cache
   docker compose up
   ```

6. **Still failing?**
   - Restart Windows
   - Docker Desktop → **Settings → Troubleshoot → Restart** or **Reset to factory defaults**
   - Update Docker Desktop to the latest version

## Run without Docker (while Docker is broken)

### Terminal 1 — API (no database history unless Postgres is up)

```powershell
cd C:\Users\Keerti\Projects\smart-farming\backend
.\.venv\Scripts\activate
$env:DATABASE_URL="postgresql://agri_user:agri_pass@localhost:5432/smart_farming"
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Web UI

```powershell
cd C:\Users\Keerti\Projects\smart-farming\frontend
npm install
$env:NEXT_PUBLIC_API_URL="http://localhost:8000"
npm run dev
```

Open http://localhost:3000. For full DB features, start only Postgres after Docker works:

```powershell
docker compose up db -d
```
