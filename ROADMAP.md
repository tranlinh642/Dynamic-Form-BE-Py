# 🗺️ Kế Hoạch Chuyển Đổi: NestJS sang Python FastAPI (Clean Architecture)

> **Mục tiêu**: Chuyển đổi toàn diện dự án Dynamic Form từ NestJS sang FastAPI, áp dụng kiến trúc Clean Architecture, tuân thủ chặt chẽ các Design Patterns và nguyên lý SOLID. Toàn bộ mã nguồn do học viên tự tay triển khai dưới sự hướng dẫn phương pháp và giải thích chi tiết.

---

## 📌 GIAI ĐOẠN 1: Database Foundation & ORM (Async SQLAlchemy 2.0 + Alembic)
- [x] **Task 1.1: Quản lý cấu hình tập trung (`app/core/config.py`)**
- [x] **Task 1.2: Base Model & Async Database Session (`app/db/base.py`, `app/db/session.py`)**
- [x] **Task 1.3: Khai báo Entity Models (`app/db/models/`)**
- [x] **Task 1.4: Cấu hình Alembic Async & Chạy Migration đầu tiên**
- [x] **Task 1.5: Seed Data Script (`scripts/seed.py`)**

---

## 📌 GIAI ĐOẠN 2: Data Access Layer (Repository Pattern)
- [x] **Task 2.1: Generic Base Repository (`app/db/repositories/base.py`)**
- [x] **Task 2.2: Specialized Repositories (`app/db/repositories/`)**

---

## 📌 GIAI ĐOẠN 3: Authentication, Authorization & Security (RBAC)
- [x] **Task 3.1: Security Core (`app/core/security.py`)**
- [x] **Task 3.2: Auth DTOs & Service (`app/schemas/auth.py`, `app/services/auth_service.py`)**
- [x] **Task 3.3: FastAPI Security Dependencies (`app/api/dependencies/auth.py`)**

---

## 📌 GIAI ĐOẠN 4: Dynamic Validation Engine (Strategy & Factory Pattern)
- [x] **Task 4.1: Strategy Pattern cho Field Validators (`app/core/validation/validators/`)**
- [x] **Task 4.2: Factory Pattern (`app/core/validation/validation_factory.py`)**
- [x] **Task 4.3: Validation Runner trong Submission Service**

---

## 📌 GIAI ĐOẠN 5: Use Cases & Business Logic (Service Layer)
- [x] **Task 5.1: Form Service (`app/services/form_service.py`)**
- [x] **Task 5.2: Field Service (`app/services/field_service.py`)**
- [x] **Task 5.3: Submission Service (`app/services/submission_service.py`)**

---

## 📌 GIAI ĐOẠN 6: Presentation Layer (API Routers & OpenAPI Docs)
- [x] **Task 6.1: Auth Router (`app/api/v1/auth.py`)**
- [x] **Task 6.2: Form Router (`app/api/v1/forms.py`)**
- [x] **Task 6.3: Field Router (`app/api/v1/fields.py`)**
- [x] **Task 6.4: Submission Router (`app/api/v1/submissions.py`)**
- [x] **Task 6.5: Router Integration & Docs Optimization (`app/main.py`)**

---

## 📌 GIAI ĐOẠN 7: Testing & Production Readiness
- [ ] **Task 7.1: Async Testing Setup (`pytest`, `httpx.AsyncClient`)**
- [ ] **Task 7.2: E2E Integration Tests (Luồng nghiệp vụ trọn vẹn)**
- [ ] **Task 7.3: Review kiến trúc, kiểm tra N+1 query và rà soát bảo mật**
