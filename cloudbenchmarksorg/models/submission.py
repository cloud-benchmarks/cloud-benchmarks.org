from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)

from .base import Base


CHARM_BLACKLIST = (
    'collectd', 'cabs', 'cabs-collector',
    'benchmark-gui', 'siege',
)


class Submission(Base):
    environment_id = Column(Integer, ForeignKey('environment.id'))

    data = Column(JSON)
    environment = relationship('Environment')

    @property
    def services_dict(self):
        """Return the 'services' dict from this submission's bundle.

        """
        return self.data['bundle']['services']

    def services(self, filtered=False):
        for s in self.services_dict.values():
            c = Service(s)
            if filtered and c.charm_name in CHARM_BLACKLIST:
                continue
            yield Service(s)

    @property
    def result(self):
        return self.data['action']['output']['meta']['composite']


class Service(object):
    def __init__(self, data):
        self.data = data
        self.charm_name = self._parse_name()
        self.unit_count = self._parse_count()

    def _parse_name(self):
        charm = self.data['charm']
        _, charm = charm.rsplit('/', 1)
        charm, _ = charm.rsplit('-', 1)
        return charm

    def _parse_count(self):
        num_units = self.data['num_units']
        return int(num_units)
