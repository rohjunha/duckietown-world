import os
from functools import lru_cache
from pathlib import Path
from typing import List

from zuper_commons.fs import locate_files

RESOURCES_PATTERNS = ["*.png", "*.jpg", "*.yaml", "*.gltf", "*.obj", "*.mtl", "*.json", "*.tga", "*.bmp"]


def list_maps() -> List[str]:
    maps_dir = get_maps_dir()

    def f():
        for map_file in os.listdir(maps_dir):
            map_name = map_file.split(".")[0]
            yield map_name

    return list(f())


def list_maps2():
    maps_dir = get_maps_dir()

    def f():
        for map_file in os.listdir(maps_dir):
            map_name = map_file.split(".")[0]
            yield map_name, os.path.join(maps_dir, map_file)

    return dict(f())


def get_maps_dir():
    dd = get_data_dir()
    d = os.path.join(dd, "gd1/maps")
    assert os.path.exists(d), d
    return d


def get_data_dir():
    """ location of data dir """
    abs_path_module = os.path.realpath(__file__)
    module_dir = Path(os.path.dirname(abs_path_module))
    return str(module_dir / "data")
    # return cast(DirPath, str(module_dir / "data"))


@lru_cache(maxsize=None)
def get_data_resources():
    data = get_data_dir()
    # logger.info(data=data)
    files = locate_files(data, pattern=RESOURCES_PATTERNS)
    res2 = []
    res1 = {}
    for f in files:
        basename = os.path.basename(f)
        if basename in res1:
            msg = "Double basename."
            # logger.warning(msg, basename=basename, f1=f, f2=res1[basename])
        else:
            res1[basename] = f
        res2.append(f)

    # logger.info(resources=res2, res1=list(res1))
    return res1, res2


def get_resource_path(basename: str):
    res1, res2 = get_data_resources()
    if "/" in basename:
        for v in res2:
            if v.endswith(basename):
                return v

    else:
        if basename in res1:
            return res1[basename]
    msg = f"Could not find resource {basename!r}."
    raise KeyError(msg)  #, known=sorted(res2), res1=sorted(res1))
