@echo off
setlocal

docker compose up --build -d
if errorlevel 1 (
  echo.
  echo Failed to start WeCareForYou with Docker.
  exit /b 1
)

echo.
echo WeCareForYou is running.
echo Frontend: http://localhost:4200
echo Backend:  http://localhost:5000/api/health
