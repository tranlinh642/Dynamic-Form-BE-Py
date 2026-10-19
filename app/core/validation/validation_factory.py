from typing import Dict

from app.core.enums import FieldType
from app.core.validation.field_validator import BaseFieldValidator
from app.core.validation.validators import (
    ColorValidator,
    DateValidator,
    NumberValidator,
    SelectValidator,
    TextValidator,
)


class ValidationFactory:
    _validators: Dict[str, BaseFieldValidator] = {
        FieldType.TEXT.value: TextValidator(),
        FieldType.NUMBER.value: NumberValidator(),
        FieldType.DATE.value: DateValidator(),
        FieldType.COLOR.value: ColorValidator(),
        FieldType.SELECT.value: SelectValidator(),
    }

    @classmethod
    def get_validator(cls, field_type: str) -> BaseFieldValidator:
        validator = cls._validators.get(field_type)
        if not validator:
            raise ValueError(f"Không tìm thấy Validator cho loại trường: {field_type}")
        return validator
