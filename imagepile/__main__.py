import logging
import argparse
from imagepile.validate import validate

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Remove invalid images from a folder")
    parser.add_argument("folderpath")
    parser.add_argument("--remove", action="store_true", help="Remove faulty images")
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)

    validate(args.folderpath, args.remove)
