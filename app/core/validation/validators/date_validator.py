from datetime import datetime, timezone
from typing import Any, Optional

from app.core.validation.field_validator import BaseFieldValidator
from app.db.models.field import Field


class DateValidator(BaseFieldValidator):
    def validate(self, value: Any, field: Field) -> Optional[str]:
        if not isinstance(value, str):
            return f"Trường {field.label} phải là một ngày tháng hợp lệ (ISO format)."

        try:
            parsed_date = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed_date.tzinfo is None:
                parsed_date = parsed_date.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            return f"Trường {field.label} phải là một ngày tháng hợp lệ (ISO format)."

        if field.validation and isinstance(field.validation, dict):
            today = datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

            if "minDate" in field.validation and field.validation["minDate"]:
                raw_min = field.validation["minDate"]
                min_label = (
                    "ngày hiện tại" if raw_min == "today" else str(raw_min)
                )
                try:
                    min_d = (
                        today
                        if raw_min == "today"
                        else datetime.fromisoformat(str(raw_min).replace("Z", "+00:00"))
                    )
                    if min_d.tzinfo is None:
                        min_d = min_d.replace(tzinfo=timezone.utc)
                    if parsed_date < min_d:
                        return f"Trường {field.label} không được nhỏ hơn {min_label}."
                except Exception:
                    pass

            if "maxDate" in field.validation and field.validation["maxDate"]:
                raw_max = field.validation["maxDate"]
                max_label = (
                    "ngày hiện tại" if raw_max == "today" else str(raw_max)
                )
                try:
                    max_d = (
                        today
                        if raw_max == "today"
                        else datetime.fromisoformat(str(raw_max).replace("Z", "+00:00"))
                    )
                    if max_d.tzinfo is None:
                        max_d = max_d.replace(tzinfo=timezone.utc)
                    if parsed_date > max_d:
                        return f"Trường {field.label} không được lớn hơn {max_label}."
                except Exception:
                    pass

        return None
