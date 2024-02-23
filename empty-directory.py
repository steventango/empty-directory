import argparse
import glob
import logging
import os
from datetime import datetime, timedelta

from send2trash import send2trash


def main():
    parser = argparse.ArgumentParser(description="Empty directory")
    parser.add_argument("path", type=str, help="path to empty")
    parser.add_argument("--trash", action="store_true", help="move files to trash")
    parser.add_argument("--remove", action="store_true", help="remove files")
    parser.add_argument("--days", type=int, default=30, help="days to keep files")
    parser.add_argument("--start-date", type=str, default=None, help="start date")
    parser.add_argument("--dry-run", action="store_true", help="dry run")
    args = parser.parse_args()

    logging.basicConfig(
        filename="empty-directory.log",
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    logging.getLogger().addHandler(console)

    logging.info(args)

    pathname = args.path + "/**"
    logging.info(f"Searching {pathname}")
    paths = glob.glob(pathname, recursive=True)
    paths = sorted(paths, key=len, reverse=True)
    if len(paths):
        paths.pop()
    logging.info(f"Found {len(paths)} files")

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d") if args.start_date else None

    for path in paths:
        date_time = datetime.fromtimestamp(os.path.getmtime(path))

        logging.info(f"{path} [{date_time}]")

        if start_date and date_time < start_date or datetime.now() - date_time < timedelta(minutes=args.days):
            continue

        logging.info(f"Removing {path}")

        if args.dry_run:
            continue
        elif args.trash:
            send2trash(path)
        elif args.remove:
            os.remove(path)
        else:
            raise ValueError("No action specified")


if __name__ == "__main__":
    main()
