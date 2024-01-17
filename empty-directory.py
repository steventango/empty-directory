import argparse
from datetime import datetime, timedelta
import glob
import logging
import os
import subprocess


def main():
    parser = argparse.ArgumentParser(description='Empty directory')
    parser.add_argument('path', metavar='path', type=str, nargs='+',
                        help='path to empty')
    parser.add_argument('--trash', action='store_true',
                        help='move files to trash')
    parser.add_argument('--remove', action='store_true',
                        help='remove files')
    parser.add_argument('--days', type=int, default=30,
                        help='days to keep files')
    parser.add_argument('--start-date', type=str, default=None,
                        help='start date')
    parser.add_argument('--dry-run', action='store_true',
                        help='dry run')
    args = parser.parse_args()

    logging.basicConfig(filename='empty-directory.log', level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())

    paths = glob.glob(args.path[0] + '/**')

    start_date = datetime.strptime(args.start_date, '%Y-%m-%d') if args.start_date else None

    for path in paths:
        date_time = datetime.fromtimestamp(os.path.getmtime(path))

        if start_date and date_time < start_date or datetime.now() - date_time < timedelta(days=args.days):
            continue

        logging.info(path)
        if args.dry_run:
            continue
        elif args.trash:
            subprocess.run(['trash', path])
        elif args.remove:
            os.remove(path)
        else:
            raise ValueError('No action specified')


if __name__ == "__main__":
    main()
