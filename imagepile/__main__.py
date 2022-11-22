import os
import logging
import argparse
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

logger = logging.getLogger(__name__)

EXTENSIONS=['.jpg', '.jpeg', '.png']


def _validate_image(filepath):
    try:
        with Image.open(filepath) as img:
            img.convert("RGB").verify()
    
        return True
    except Exception as e:
        print(f"[{e.__class__.__name__}] {e}: {str(filepath)}")
        os.remove(filepath)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Remove invalid images from a folder")
    parser.add_argument("folderpath")
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)

    root = Path(args.folderpath)
    n = len(root.parts)
    filepaths = np.array([
        str(Path(*f.parts[n:])) for f in root.rglob("*")
        if f.is_file() and f.suffix in EXTENSIONS
    ])

    logger.info("Num filepaths", len(filepaths))

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        mask = np.array(list(executor.map(
            _validate_image, (root / Path(f) for f in filepaths))))

    filepaths = list(filepaths[mask])
    logger.info("Num filepaths", len(filepaths))
