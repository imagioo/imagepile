import os
import logging
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from functools import partial
from typing import Union

logger = logging.getLogger(__name__)

EXTENSIONS=['.jpg', '.jpeg', '.png']


def _validate_image(
    filepath: Union[str, Path],
    remove: bool=False
):
    try:
        with Image.open(filepath) as img:
            img.convert("RGB").verify()
    
        return True
    except Exception as e:
        print(f"[{e.__class__.__name__}] {e}: {str(filepath)}")
        if remove:
            os.remove(filepath)
        return False


def validate(
    folderpath: Union[str, Path],
    remove: bool=False
):
    root = Path(folderpath)
    n = len(root.parts)
    filepaths = np.array([
        str(Path(*f.parts[n:])) for f in root.rglob("*")
        if f.is_file() and f.suffix in EXTENSIONS
    ])
    logger.info(f"Number of images {len(filepaths)}")

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        mask = np.array(list(executor.map(
            partial(_validate_image, remove=remove),
            (root / Path(f) for f in filepaths))))

    filepaths = list(filepaths[mask])
    logger.info(f"Number of filtered images: {len(filepaths)}")
