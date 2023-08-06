from pathlib import Path

from v3_0.shared.filesystem import fs
from v3_0.shared.filesystem.movable import Movable


class PathBased(Movable):
    def __init__(self, path: Path) -> None:
        super().__init__()

        self.__path = path

    @property
    def path(self) -> Path:
        return self.__path

    def move(self, path: Path) -> None:
        # files and folders are copied differently. Also having same drive matters
        fs.move(self.path, path)

        self.__path = path / self.path.name

    def copy(self, path: Path) -> None:
        fs.copy(self.path, path)

    def move_down(self, subfolder: str) -> None:
        self.move(self.path.parent / subfolder)

    def move_up(self) -> None:
        self.move(self.path.parent.parent)
