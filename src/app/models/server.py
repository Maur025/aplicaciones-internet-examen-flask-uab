from sqlalchemy import Column, String, Integer

from .base_model import BaseModel


class Server(BaseModel):
    __tablename__ = "servers"

    name = Column(String(100), nullable=False)
    host = Column(String(255))
    port = Column(Integer)

    def __repr__(self):
        return self.name
