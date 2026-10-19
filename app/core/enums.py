from enum import Enum


class FieldType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    COLOR = "color"
    SELECT = "select"


class FormStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"


class RoleType(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
