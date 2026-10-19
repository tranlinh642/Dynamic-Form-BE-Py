from typing import Any, Optional

from app.core.validation.field_validator import BaseFieldValidator
from app.db.models.field import Field


class SelectValidator(BaseFieldValidator):
    def validate(self, value: Any, field: Field) -> Optional[str]:
        if not field.options or not isinstance(field.options, list):
            return f"Trường {field.label} bị lỗi cấu hình (thiếu danh sách lựa chọn)."

        if value not in field.options:
            return f"Giá trị của trường {field.label} không nằm trong danh sách lựa chọn hợp lệ."

        return None
