from sqlalchemy.dialects.postgresql import JSON

from sqlalchemy import (
    Column,
)

from .base import Base


CHARM_BLACKLIST = (
    'collectd', 'cabs', 'cabs-collector',
    'benchmark-gui', 'siege',
)


class Submission(Base):
    data = Column(JSON)

    @property
    def cloud_name(self):
        env = self.data['environment']
        if env['cloud']:
            return env['cloud'].lower()
        if env['region']:
            return '{}:{}'.format(
                env['provider_type'], env['region'])
        return env['provider_type']

    @property
    def services(self):
        return self.data['bundle']['services']

    def charms(self, filtered=False):
        for s in self.services.values():
            c = Charm(s)
            if filtered and c.name in CHARM_BLACKLIST:
                continue
            yield Charm(s)

    @property
    def result(self):
        return self.data['action']['output']['meta']['composite']


class Charm(object):
    def __init__(self, service_dict):
        self.service_dict = service_dict
        self.name = self._parse_name()
        self.count = self._parse_count()

    def _parse_name(self):
        charm = self.service_dict['charm']
        _, charm = charm.rsplit('/', 1)
        charm, _ = charm.rsplit('-', 1)
        return charm

    def _parse_count(self):
        num_units = self.service_dict['num_units']
        return int(num_units)
