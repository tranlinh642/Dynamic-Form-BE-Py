import re
from typing import Any, Optional

from app.core.validation.field_validator import BaseFieldValidator
from app.db.models.field import Field

HEX_COLOR_REGEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


class ColorValidator(BaseFieldValidator):
    def validate(self, value: Any, field: Field) -> Optional[str]:
        if not isinstance(value, str):
            return f"Trường {field.label} phải là định dạng mã màu HEX."

        if not HEX_COLOR_REGEX.match(value):
            return f"Trường {field.label} không đúng định dạng mã màu HEX (VD: #FFFFFF)."

        return None
