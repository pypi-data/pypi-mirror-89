from pathlib import Path
from typing import List

from v3_0.shared.filesystem.file import File
from v3_0.shared.filesystem.folder_tree import FolderTree
from v3_0.shared.filesystem.path_based import PathBased


class PathsParser:
    @staticmethod
    def parse(paths: List[Path]) -> List[PathBased]:
        result = []

        for path in paths:
            if path.is_file():
                result.append(File(path))
            elif path.is_dir():
                result.append(FolderTree(path))
            else:
                assert False

        return result
