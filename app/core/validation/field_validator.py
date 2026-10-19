from abc import ABC, abstractmethod
from typing import Any, Optional

from app.db.models.field import Field


class BaseFieldValidator(ABC):
    @abstractmethod
    def validate(self, value: Any, field: Field) -> Optional[str]:
        pass
