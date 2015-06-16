from sqlalchemy.dialects.postgresql import JSON

from sqlalchemy import (
    Column,
)

from .base import Base


class Submission(Base):
    data = Column(JSON)
