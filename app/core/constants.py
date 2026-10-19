from typing import Final


class Permissions:
    CREATE_FORM: Final[str] = "CREATE_FORM"
    SUBMIT_FORM: Final[str] = "SUBMIT_FORM"
    VIEW_FORM: Final[str] = "VIEW_FORM"
    UPDATE_FORM: Final[str] = "UPDATE_FORM"
    DELETE_FORM: Final[str] = "DELETE_FORM"

    CREATE_FIELD: Final[str] = "CREATE_FIELD"
    UPDATE_FIELD: Final[str] = "UPDATE_FIELD"
    DELETE_FIELD: Final[str] = "DELETE_FIELD"

    VIEW_SUBMISSIONS: Final[str] = "VIEW_SUBMISSIONS"
    VIEW_ALL_SUBMISSIONS: Final[str] = "VIEW_ALL_SUBMISSIONS"

    @classmethod
    def get_all(cls) -> list[str]:
        return [
            v for k, v in cls.__dict__.items()
            if not k.startswith("__") and isinstance(v, str)
        ]
