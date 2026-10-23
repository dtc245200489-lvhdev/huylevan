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
```powershell
docker compose ps
docker compose logs --tail=100 web
docker compose logs --tail=100 nginx
docker compose logs --tail=100 prometheus
docker compose logs --tail=100 loki
```
Kiểm tra endpoint metrics: http://localhost:8080/metrics  
Kiểm tra health: http://localhost:8080/health

Trong Prometheus, thử query `up`, `http_requests_total`, `process_resident_memory_bytes`.  
Trong Grafana, vào Explore, chọn nguồn Loki và chạy `{container="recipe-web"}` hoặc `{job="docker"}` tùy nhãn được thu thập.

## 5. Dừng và xóa
```powershell
docker compose down
```
Xóa cả dữ liệu PostgreSQL:
```powershell
docker compose down -v
```
Lệnh thứ hai xóa dữ liệu DB trong volume, hãy dùng cẩn thận.

## 6. Cấu trúc
- `app/`: Flask web, mô hình dữ liệu và templates
- `nginx/`: cấu hình reverse proxy và security headers
- `prometheus/`: cấu hình scrape metrics
- `grafana/`: datasource và dashboard provision
- `loki/`, `promtail/`: tập trung log
- `report/`: báo cáo DOCX và PDF nếu đã xuất

## 7. Ghi chú học thuật
Đây là bộ mã nguồn thực hành mẫu có thể chạy và kiểm thử. Trong báo cáo, chỉ điền kết quả thực nghiệm và ảnh chụp sau khi thực sự chạy trên máy của sinh viên; không sử dụng ảnh minh họa giả làm bằng chứng đã triển khai.
