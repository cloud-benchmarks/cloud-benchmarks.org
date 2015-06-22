import argparse

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from sqlalchemy import engine_from_config
from sqlalchemy_utils import (
    create_database,
    database_exists,
)

from cloudbenchmarksorg.models import (
    Base,
    DBSession,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ini_file')
    parser.add_argument(
        '-f', '--force', action='store_true',
        help='If tables exist, drop and recreate'
    )
    args = parser.parse_args()

    setup_logging(args.ini_file)
    settings = get_appsettings(args.ini_file)
    engine = engine_from_config(settings, 'sqlalchemy.')

    if not database_exists(engine.url):
        create_database(engine.url)

    DBSession.configure(bind=engine)
    if args.force:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
