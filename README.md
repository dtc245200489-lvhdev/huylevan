# Đề 29 – Website công thức nấu ăn / Recipe

**Sinh viên:** Lê Văn Huy – DTC245200489  
**Lớp:** CNTT K23A – Trường Đại học Công nghệ Thông tin và Truyền thông, Đại học Thái Nguyên  
**Giảng viên:** Nguyễn Chuyên Anh

## 1. Mục tiêu

Triển khai website công thức nấu ăn cùng PostgreSQL, Nginx reverse proxy, Prometheus, Grafana, Loki và Promtail bằng Docker Compose. Có pgAdmin để quản trị cơ sở dữ liệu.

## 2. Yêu cầu

- Docker Desktop hoặc Docker Engine + Docker Compose v2
- Máy tính có RAM khuyến nghị 8 GB, còn trống khoảng 4 GB
- Các cổng 8080, 5050, 3000, 9090, 3100 chưa bị ứng dụng khác chiếm

## 3. Khởi chạy trên Windows

Mở PowerShell tại thư mục có `docker-compose.yml`:

```powershell
docker compose config
docker compose up -d --build
docker compose ps
```

Truy cập:

- Website: http://localhost:8080
- pgAdmin: http://localhost:5050 (email `admin@example.com`, mật khẩu `Admin123!ChangeMe`)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (user `admin`, mật khẩu `Admin123!ChangeMe`)

**Đổi các mật khẩu mẫu trước khi dùng trên mạng thật.** Các thông tin đăng nhập trong bài chỉ dùng cho môi trường thực hành cục bộ.

## 4. Kiểm tra nhanh

Kiểm tra trạng thái các dịch vụ:

```powershell
docker compose ps
```

Xem log của từng dịch vụ:

```powershell
docker compose logs --tail=100 web
docker compose logs --tail=100 nginx
docker compose logs --tail=100 prometheus
docker compose logs --tail=100 loki
```

Kiểm tra endpoint metrics: http://localhost:8080/metrics  
Kiểm tra health: http://localhost:808
