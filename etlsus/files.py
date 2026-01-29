from __future__ import annotations

from pathlib import Path
from typing import List


def get_files_from_dir(
        folder_dir: str,
        extension: str,
        infix: str = None
) -> List[Path]:
    """
    Retrieves all files from a directory with matching extension.

    param:
        folder_dir (str): Directory path to search
        extension (str): Expected file extension (e.g., 'csv', '.yaml')
        infix (str): Optional string used to filter files
    returns:
        List[Path]: Full file paths matching the criteria
    """
    path = Path(folder_dir).resolve()

    if infix:
        files = [file for file in path.glob(f'**/*{extension}')
                 if infix in str(file)]
    else:
        files = [file for file in path.glob(f'**/*{extension}')]

    return files


def get_file_name(file_path: Path, excluding_path: Path) -> str:
    """
    Get the folder/file name directly after excluding_path.
    """
    if file_path.parent.name != excluding_path.name:
        return file_path.parent.name
    else:
        return file_path.stem
