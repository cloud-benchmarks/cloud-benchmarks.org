from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)

from .base import Base


FILTERED_CHARMS = (
    'collectd', 'cabs', 'cabs-collector',
    'benchmark-gui', 'siege',
)


class Submission(Base):
    environment_id = Column(Integer, ForeignKey('environment.id'))

    data = Column(JSONB)
    _service_names = Column(JSONB)
    environment = relationship('Environment')

    def __init__(self, *args, **kw):
        super(Submission, self).__init__(*args, **kw)
        # Store parsed service names in a json column
        # so we can query against it later
        self._service_names = [s.charm_name for s in self.services()]

    @property
    def services_dict(self):
        """Return the 'services' dict from this submission's bundle.

        """
        return self.data['bundle']['services']

    def services(self, filtered=False):
        for s in self.services_dict.values():
            c = Service(s)
            if filtered and c.charm_name in FILTERED_CHARMS:
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
