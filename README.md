# Ứng Dụng Quản Lý Công Việc

## Thông Tin Cá Nhân
- Tên: Nguyễn Quang Mạnh
- MSSV: 22645001

## Mô Tả Dự Án
Dự án này là một ứng dụng quản lý công việc cho phép người dùng quản lý công việc của họ, theo dõi tình trạng hoàn thành và xem thời gian tạo và hoàn thành.

## Hướng Dẫn Cài Đặt
1. **Clone repository**:
   ```bash
   git clone https://github.com/QuangManh160304/ptud-gk-de-2.git
   cd ptud-gk-de-2
   ```
2. **Tạo môi trường ảo**
   - Trên Windows:

      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

    - Trên macOS/Linux:

      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
3. **Cài đặt các thư viện phụ thuộc**:

    ```bash
    pip install -r requirements.txt
    ```

    Nếu bạn chưa có `requirements.txt`, bạn có thể tạo file này bằng cách chạy:

    ```bash
    pip freeze > requirements.txt
    ```

### 3. Chạy ứng dụng
Hướng dẫn chạy ứng dụng Flask.

```markdown
## Chạy ứng dụng

Sau khi cài đặt xong, bạn có thể chạy ứng dụng bằng cách:

```bash
flask run
======
