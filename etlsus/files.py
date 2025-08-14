import os
from typing import List


def check_file_exists (path: str) -> bool:
    """
    Returns True if a file exists. False if otherwise.

    param:
        path (str): Path leading to the file
    return:
        bool: State of the file
    """
    return os.path.isfile(path)


def load_files (folder_url: str, endswith: str) -> List[str]:
    return [os.path.join(folder_url, f)
            for f in os.listdir(folder_url)
            if f.endswith(endswith)]
