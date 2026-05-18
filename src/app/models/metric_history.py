from sqlalchemy import Column, String, Double, ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class MetricHistory(BaseModel):
    __tablename__ = 'metric_histories'

    metric = Column(String(100), nullable=False)
    value = Column(Double, nullable=False)
    unit = Column(String(150), nullable=False)

    server_id = Column(String(36), ForeignKey('servers.id'), nullable=False)
    server = relationship('Server', lazy='joined')

    def __repr__(self):
        return self.metric
