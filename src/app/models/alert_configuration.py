from sqlalchemy import Column, Double, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class AlertConfiguration(BaseModel):
    __tablename__ = 'alert_configurations'

    max_value = Column(Double, nullable=False)
    min_value = Column(Double, nullable=False)
    remain_value_min = Column(Integer, nullable=False, default=0)

    metric_id = Column(String(36), ForeignKey('metrics.id'), nullable=False)
    metric = relationship('Metric', lazy='joined')

    server_id = Column(String(36), ForeignKey('servers.id'), nullable=False)
    server = relationship('Server', lazy='joined')

    def __repr__(self):
        return ''
