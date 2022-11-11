import os
import logging
from PIL import Image, ImageOps
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from functools import partial
from typing import Union
from tqdm.auto import tqdm
from enum import Enum

logger = logging.getLogger(__name__)

EXTENSIONS=['.jpg', '.jpeg', '.png']
class Mode(Enum):
    CONTAIN = "contain"
    FIT = "fit"


def _thumbnail_image(
    src_filepath: Union[str, Path],
    dst_filepath: Union[str, Path],
    size,
    mode: Mode=Mode.CONTAIN,
    overwrite: bool=False
):
    try:
        if overwrite or not os.path.exists(dst_filepath):
            # Create the directory and all parent directories if they don't exist
            folderpath = os.path.dirname(dst_filepath)
            os.makedirs(folderpath, exist_ok=True)

            with Image.open(src_filepath) as img:
                img = img.convert("RGB")
                img.verify()
                if mode == Mode.CONTAIN:
                    img = ImageOps.contain(img, size)
                elif mode == Mode.FIT:
                    img = ImageOps.fit(img, size)
                else:
                    raise NotImplementedError(f"Mode {mode} not implemented")
                if "exif" in img.info:
                    img.save(dst_filepath, exif=img.info["exif"])
                else:
                    img.save(dst_filepath)
    
        return True
    except Exception as e:
        print(f"[{e.__class__.__name__}] {e}: {str(src_filepath)}")
        return False
    

def thumbnail(
    src_folderpath: Union[str, Path],
    dst_folderpath: Union[str, Path],
    size,
    mode: Mode=Mode.CONTAIN,
    overwrite: bool=False
):
    root = Path(src_folderpath)
    n = len(root.parts)
    src_filepaths = [
        str(Path(*f.parts[n:])) for f in root.rglob("*")
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    ]
    dst_filepaths = [os.path.join(dst_folderpath, f) for f in src_filepaths]
    src_filepaths = [os.path.join(src_folderpath, f) for f in src_filepaths]

    logger.info(f"Number of images {len(src_filepaths)}")

    if len(src_filepaths) > 0:
        if not os.path.exists(dst_folderpath):
            os.makedirs(dst_folderpath)

        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            num_images = sum(tqdm(executor.map(
                partial(_thumbnail_image, size=size, mode=mode, overwrite=overwrite),
                src_filepaths, dst_filepaths), total=len(src_filepaths)))
            
        logger.info(f"Number of resized images: {num_images}")
