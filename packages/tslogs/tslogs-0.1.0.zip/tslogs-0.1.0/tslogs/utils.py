import re
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Iterable, Tuple, Union

RE_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def get_files_in_date_range(
    paths: Iterable[Union[str, PathLike]], date_range: Tuple[datetime, datetime] = None
):
    """
    Get the all the files from dirs that matched yyyy-mm-dd pattern.
    If file path is also given it will be included without matching.
    """
    files = []
    if isinstance(paths, (str, Path)):
        paths = [paths]
    for path in paths:
        p = Path(path)
        dir_fs = []
        if p.is_dir():
            dir_fs = [f for f in p.iterdir() if f.is_file()]
        elif p.is_file():
            files.append(p)

        if date_range:
            for f in dir_fs:
                if match := RE_ISO_DATE.match(f.name):
                    try:
                        fdate = datetime.fromisoformat(match.group()).date()
                    except ValueError:
                        pass
                    else:
                        if date_range[0].date() <= fdate < date_range[1].date():
                            files.append(f)
        else:
            files += dir_fs
    return files
