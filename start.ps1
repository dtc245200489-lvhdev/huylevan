$ErrorActionPreference = "Stop"
Write-Host "Kiem tra Docker Compose..."
docker compose config
Write-Host "Khoi dong cac dich vu..."
docker compose up -d --build
Write-Host "Trang thai dich vu:"
docker compose ps
Write-Host "Website: http://localhost:8080"
Write-Host "Grafana: http://localhost:3000"
Write-Host "Prometheus: http://localhost:9090"
Write-Host "pgAdmin: http://localhost:5050"
