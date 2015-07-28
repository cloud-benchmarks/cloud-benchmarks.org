import argparse
import logging

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

import transaction
from sqlalchemy import engine_from_config

from cloudbenchmarksorg import models as M

log = logging.getLogger('cloudbenchmarksorg')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ini_file')
    args = parser.parse_args()

    setup_logging(args.ini_file)
    settings = get_appsettings(args.ini_file)
    engine = engine_from_config(settings, 'sqlalchemy.')
    M.DBSession.configure(bind=engine)

    session = M.DBSession()
    for s in session.query(M.Submission):
        d = {}
        d.update(s.data)
        updated = False
        for svc in d.get('bundle', {}).get('services', {}):
            constraints = d['bundle']['services'][svc].get('constraints')
            if constraints and isinstance(constraints, dict):
                constraints = ' '.join([
                    '{}={}'.format(k, v) for k, v in constraints.items()
                ])
                d['bundle']['services'][svc]['constraints'] = constraints
                updated = True
        if updated:
            log.debug(
                'Updating constraints on Submission %s: %s', s.id, constraints)
            session.query(M.Submission) \
                .filter_by(id=s.id) \
                .update(dict(data=d))
    transaction.commit()


if __name__ == '__main__':
    main()
