from typing import Any, Optional

from app.core.validation.field_validator import BaseFieldValidator
from app.db.models.field import Field


class NumberValidator(BaseFieldValidator):
    def validate(self, value: Any, field: Field) -> Optional[str]:
        try:
            num = float(value)
        except (ValueError, TypeError):
            return f"Trường {field.label} phải là một số hợp lệ."

        if field.validation and isinstance(field.validation, dict):
            if "min" in field.validation and field.validation["min"] is not None:
                min_val = float(field.validation["min"])
                if num < min_val:
                    return f"Trường {field.label} tối thiểu phải là {field.validation['min']}."

            if "max" in field.validation and field.validation["max"] is not None:
                max_val = float(field.validation["max"])
                if num > max_val:
                    return f"Trường {field.label} tối đa là {field.validation['max']}."

        return None
