from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Lớp cơ sở chung cho toàn bộ ORM Models.
    Base.metadata sẽ chứa thông tin toàn bộ schema để Alembic đọc."""
    pass
