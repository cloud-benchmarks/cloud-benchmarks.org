import argparse

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from sqlalchemy import engine_from_config

from cloudbenchmarksorg.models import (
    Base,
    DBSession,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ini_file')
    parser.add_argument(
        '-f', '--force',
        help='If tables exist, drop and recreate'
    )
    args = parser.parse_args()

    setup_logging(args.ini_file)
    settings = get_appsettings(args.ini_file)
    engine = engine_from_config(settings, 'sqlalchemy.')

    DBSession.configure(bind=engine)
    if args.force:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
