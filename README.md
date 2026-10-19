# Dynamic Form Management - Backend API (Python)

Hệ thống Backend quản lý biểu mẫu động (Dynamic Form Management) được xây dựng bằng **Python 3.12** và **FastAPI**, chuyển đổi và tối ưu hóa từ phiên bản NestJS theo kiến trúc **Clean Architecture (Hexagonal)** và các **Design Patterns** chuẩn mực.

---

## 🏗️ Kiến Trúc Hệ Thống (Clean Architecture)

Dự án áp dụng mô hình phân tách tầng nghiêm ngặt (Separation of Concerns):

```text
dynamic-form-py/
├── alembic/                       # Quản lý Database Migrations (tương đương Prisma Migrate)
│   ├── versions/                  # Các file revision migration tự động
│   └── env.py                     # Cấu hình async database migration
├── app/
│   ├── main.py                    # Khởi tạo FastAPI App, CORS, Exception Handlers, Routers
│   ├── core/                      # Domain Core & Nền tảng dùng chung
│   │   ├── config.py              # Centralized Settings (Pydantic-Settings)
│   │   ├── constants.py           # Định nghĩa mã quyền hạn hệ thống (Permissions)
│   │   ├── enums.py               # FieldType, FormStatus, RoleType
│   │   ├── exceptions.py          # Custom Domain Exception Hierarchy
│   │   ├── error_handlers.py      # Bộ xử lý lỗi tập trung (Global Exception Filter)
│   │   ├── security.py            # Bcrypt hashing & PyJWT token utilities
│   │   └── validation/            # Dynamic Validation Engine
│   │       ├── field_validator.py # Abstract Strategy Interface
│   │       ├── validation_factory.py # Factory Pattern tạo Validator theo FieldType
│   │       └── validators/        # Text, Number, Date, Color, Select Validators
│   ├── db/                        # Data Layer
│   │   ├── base.py                # DeclarativeBase (SQLAlchemy 2.0)
│   │   ├── session.py             # Async Engine & Session (Unit of Work + DI)
│   │   ├── models/                # ORM Entities (User, Role, Form, Field, Submission)
│   │   └── repositories/          # Data Access Layer (Repository Pattern)
│   ├── schemas/                   # Data Transfer Objects (Pydantic v2 Schemas)
│   │   ├── auth.py                # Login, Register, Token, User schemas
│   │   ├── form.py                # Form request/response schemas
│   │   ├── field.py               # Field request/response schemas
│   │   ├── submission.py          # Submission schemas
│   │   └── response.py            # Generic Responses (SuccessResponse[T], PaginatedResponse[T])
│   ├── services/                  # Application Use Cases & Business Logic
│   │   ├── auth_service.py        # Đăng ký, đăng nhập, thông tin profile
│   │   ├── form_service.py        # Quản lý vòng đời biểu mẫu, cập nhật thứ tự
│   │   ├── field_service.py       # Quản lý trường dữ liệu và thứ tự trong form
│   │   └── submission_service.py  # Kiểm tra answers qua Validation Engine & lưu bài nộp
│   └── api/                       # Presentation Layer
│       ├── dependencies/          # Security & Auth Dependencies (JWT & RBAC Guards)
│       └── v1/                    # API Routers (Auth, Forms, Fields, Submissions)
├── scripts/
│   └── seed.py                    # Seed dữ liệu mẫu (Permissions, Roles, Admin user)
├── main.py                        # Root entrypoint
├── requirements.txt               # Danh sách thư viện phụ thuộc
└── ROADMAP.md                     # Lộ trình và tiến độ chuyển đổi
```

---

## 🧩 Các Design Patterns Áp Dụng

1. **Repository Pattern**: Tách biệt hoàn toàn tầng truy vấn cơ sở dữ liệu (`app/db/repositories/`) khỏi nghiệp vụ.
2. **Strategy Pattern**: Mỗi loại trường biểu mẫu (`text`, `number`, `date`, `color`, `select`) sở hữu một chiến lược kiểm tra tính hợp lệ độc lập trong `app/core/validation/validators/`.
3. **Factory Pattern**: `ValidationFactory` ánh xạ và cung cấp đúng validator tại runtime mà không dùng chuỗi `if-else` phức tạp.
4. **Unit of Work & Dependency Injection**: Quản lý vòng đời `AsyncSession` qua generator `get_db()`, tự động commit khi thành công và rollback khi phát sinh ngoại lệ.
5. **Centralized Error Handling**: Bắt và chuẩn hóa toàn bộ lỗi nghiệp vụ (`AppException`), lỗi xác thực (`RequestValidationError`) và lỗi hệ thống về định dạng JSON thống nhất.

---

## 🌐 Danh Sách API Endpoints

Tất cả phản hồi từ API đều tuân thủ cấu trúc chuẩn:
```json
{
  "success": true,
  "statusCode": 200,
  "timestamp": "2026-10-19T15:00:00.000Z",
  "message": "Thành công",
  "data": { ... },
  "meta": { "total": 10, "page": 1, "limit": 10, "totalPages": 1 }
}
```

### 1. Xác thực (Auth)
* `POST /api/auth/register`: Đăng ký tài khoản mới (mặc định gán vai trò `employee`).
* `POST /api/auth/login`: Đăng nhập bằng `username` / `password`, nhận về JWT Access Token.
* `GET /api/auth/me`: Lấy thông tin tài khoản hiện tại kèm danh sách `roles` và `permissions` (Yêu cầu Bearer Token).

### 2. Quản lý Biểu Mẫu (Forms)
* `POST /api/forms`: Tạo biểu mẫu mới (Yêu cầu quyền `CREATE_FORM`).
* `GET /api/forms`: Lấy danh sách biểu mẫu có phân trang và lọc theo trạng thái `draft` / `active`.
* `PUT /api/forms/order`: Cập nhật thứ tự sắp xếp của nhiều biểu mẫu (Yêu cầu quyền `UPDATE_FORM`).
* `GET /api/forms/{id}`: Xem chi tiết biểu mẫu kèm danh sách các trường dữ liệu.
* `PUT /api/forms/{id}`: Cập nhật tiêu đề, mô tả, trạng thái, thứ tự (Yêu cầu quyền `UPDATE_FORM`).
* `DELETE /api/forms/{id}`: Xóa biểu mẫu (Yêu cầu quyền `DELETE_FORM`).

### 3. Quản lý Trường Dữ Liệu (Fields)
* `POST /api/forms/{form_id}/fields`: Thêm trường mới vào biểu mẫu (Yêu cầu quyền `CREATE_FIELD`).
* `PUT /api/forms/{form_id}/fields/order`: Sắp xếp lại thứ tự các trường trong form (Yêu cầu quyền `UPDATE_FIELD`).
* `PUT /api/forms/{form_id}/fields/{field_id}`: Cập nhật cấu hình, options, validation rules của trường (Yêu cầu quyền `UPDATE_FIELD`).
* `DELETE /api/forms/{form_id}/fields/{field_id}`: Xóa trường khỏi biểu mẫu (Yêu cầu quyền `DELETE_FIELD`).

### 4. Nộp Biểu Mẫu & Kết Quả (Submissions)
* `GET /api/forms/active`: Lấy danh sách các biểu mẫu đang ở trạng thái kích hoạt (`active`).
* `POST /api/forms/{id}/submit`: Người dùng nộp câu trả lời, hệ thống tự động kiểm tra tính hợp lệ qua Validation Engine (Yêu cầu quyền `SUBMIT_FORM`).
* `GET /api/submissions`: Xem lịch sử nộp biểu mẫu (Người dùng thông thường xem bài nộp của chính mình; người dùng có quyền `VIEW_ALL_SUBMISSIONS` có thể xem tất cả với query param `?all=true`).

### 5. Hệ thống
* `GET /api/health`: Kiểm tra tình trạng hoạt động của API.

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Dự Án

### 1. Yêu cầu hệ thống
* **Python**: 3.11 hoặc 3.12
* **PostgreSQL**: Phiên bản 14 trở lên

### 2. Thiết lập môi trường ảo
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường
Tạo file `.env` tại thư mục gốc của dự án:
```env
ENVIRONMENT="development"
PORT=8000

# PostgreSQL Async Connection URL
DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/dynamic-form"

# JWT Authentication
AUTH_SECRET="your-super-secret-jwt-key-change-this-in-production"
AUTH_ALGORITHM="HS256"
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
CORS_ALLOWED_ORIGINS="http://localhost:5173,http://localhost:3000"
CORS_CREDENTIALS=true
```

### 4. Áp dụng Database Migration
```powershell
.\.venv\Scripts\alembic.exe upgrade head
```

### 5. Nạp dữ liệu khởi tạo (Seed Data)
```powershell
.\.venv\Scripts\python.exe -m scripts.seed
```
Dữ liệu mặc định tạo ra:
* Danh sách toàn bộ quyền hạn (`CREATE_FORM`, `SUBMIT_FORM`, `VIEW_SUBMISSIONS`,...)
* Vai trò `admin` (toàn quyền) và `employee` (các quyền cơ bản)
* Tài khoản quản trị viên:
  * **Email**: `admin@gmail.com`
  * **Mật khẩu**: `123456`

### 6. Khởi chạy Server
```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

* Swagger UI Documentation: **`http://localhost:8000/api/docs`**
* OpenAPI Schema: **`http://localhost:8000/api/openapi.json`**
