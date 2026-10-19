from typing import Any, Optional

from app.core.validation.field_validator import BaseFieldValidator
from app.db.models.field import Field


class TextValidator(BaseFieldValidator):
    def validate(self, value: Any, field: Field) -> Optional[str]:
        if not isinstance(value, str):
            return f"Trường {field.label} phải là định dạng chuỗi."

        max_length = 200
        min_length = 0

        if field.validation and isinstance(field.validation, dict):
            if "maxLength" in field.validation and field.validation["maxLength"] is not None:
                max_length = int(field.validation["maxLength"])
            if "minLength" in field.validation and field.validation["minLength"] is not None:
                min_length = int(field.validation["minLength"])

        if len(value) > max_length:
            return f"Trường {field.label} không được vượt quá {max_length} ký tự (hiện tại: {len(value)})."

        if len(value) < min_length:
            return f"Trường {field.label} tối thiểu phải có {min_length} ký tự (hiện tại: {len(value)})."

        return None
