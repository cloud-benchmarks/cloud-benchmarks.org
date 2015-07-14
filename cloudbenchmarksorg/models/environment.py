from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.orm import relationship

from .base import Base


class Environment(Base):
    uuid = Column(String)
    provider_type = Column(String)
    region = Column(String)
    cloud = Column(String)
    name = Column(String, index=True)

    submissions = relationship(
        'Submission', order_by="desc(Submission.created_at)")

    def __init__(self, **kw):
        super(Environment, self).__init__(**kw)
        self.name = self._parse_name()

    def _parse_name(self):
        if self.cloud:
            return self.cloud.lower()
        if self.region:
            return '{}-{}'.format(
                self.provider_type, self.region)
        return self.provider_type

    def to_json(self):
        return {
            'uuid': self.uuid,
            'provider_type': self.provider_type,
            'region': self.region,
            'cloud': self.cloud,
            'name': self.name,
        }
