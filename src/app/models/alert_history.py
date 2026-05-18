from sqlalchemy import Column, String, Double, UUID, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class AlertHistory(BaseModel):
    __tablename__ = 'alert_histories'

    metric = Column(String(100), nullable=False)
    value = Column(Double, nullable=False)
    unit = Column(String(150), nullable=False)
    state = Column(String(150), nullable=False)
    max_value = Column(Double, nullable=False)
    min_value = Column(Double, nullable=False)
    remain_value_min = Column(Integer, nullable=False, default=0)

    server_id = Column(UUID(as_uuid=True), ForeignKey('servers.id'), nullable=False)
    server = relationship('Server', lazy="joined")

    def __repr__(self):
        return self.metric
