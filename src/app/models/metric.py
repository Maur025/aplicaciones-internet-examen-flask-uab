from sqlalchemy import Column, String

from .base_model import BaseModel


class Metric(BaseModel):
    __tablename__ = 'metrics'

    name = Column(String(150), nullable=False)
    code = Column(String(150), nullable=False)
    unit = Column(String(150), nullable=False)

    def __repr__(self):
        return self.name
