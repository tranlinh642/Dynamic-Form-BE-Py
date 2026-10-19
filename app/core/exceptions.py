from typing import Any, List, Optional


class AppException(Exception):
    def __init__(
        self,
        message: str = "Lỗi hệ thống không mong muốn",
        status_code: int = 500,
        error_code: str = "INTERNAL_SERVER_ERROR",
        errors: Optional[List[Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.errors = errors


class BadRequestException(AppException):
    def __init__(
        self, message: str = "Yêu cầu không hợp lệ", errors: Optional[List[Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=400,
            error_code="BAD_REQUEST",
            errors=errors,
        )


class UnauthorizedException(AppException):
    def __init__(
        self, message: str = "Chưa xác thực danh tính", errors: Optional[List[Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=401,
            error_code="UNAUTHORIZED",
            errors=errors,
        )


class ForbiddenException(AppException):
    def __init__(
        self, message: str = "Không có quyền truy cập", errors: Optional[List[Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=403,
            error_code="FORBIDDEN",
            errors=errors,
        )


class NotFoundException(AppException):
    def __init__(self, message: str = "Không tìm thấy dữ liệu yêu cầu"):
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
        )


class ValidationException(AppException):
    def __init__(
        self,
        message: str = "Dữ liệu xác thực không hợp lệ",
        errors: Optional[List[Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
            errors=errors or [],
        )
