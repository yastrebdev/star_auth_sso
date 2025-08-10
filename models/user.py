import uuid
from sqlalchemy import Column, String, Boolean

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String)
    last_name = Column(String)

    is_active = Column(Boolean, default=True, index=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()