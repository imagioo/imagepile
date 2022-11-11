import logging
import argparse
from imagepile.validate import validate
from imagepile.thumbnail import thumbnail, Mode

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Remove invalid images from a folder")
    subparsers = parser.add_subparsers(dest="method", help="Method")

    # Validate
    parser_validate = subparsers.add_parser("validate", help="Validate")
    parser_validate.add_argument("folderpath")
    parser_validate.add_argument(
        "--remove", action="store_true", help="Remove faulty images")
    
    # Thumbnail
    parser_thumbnail = subparsers.add_parser("thumbnail", help="Thumbnail")
    parser_thumbnail.add_argument("src_folderpath")
    parser_thumbnail.add_argument("dst_folderpath")
    parser_thumbnail.add_argument("width", type=int)
    parser_thumbnail.add_argument("height", type=int)
    parser_thumbnail.add_argument(
        "mode", type=str, 
        choices=[m.value for m in Mode],
        default=Mode.CONTAIN.value)
    parser_thumbnail.add_argument("overwrite", action="store_true")
    
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)

    if args.method == "validate":
        validate(args.folderpath, args.remove)
    elif args.method == "thumbnail":
        thumbnail(
            args.src_folderpath,
            args.dst_folderpath,
            (args.width, args.height),
            args.overwrite)
