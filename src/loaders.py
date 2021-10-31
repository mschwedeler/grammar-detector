from logging import getLogger
from os.path import join
from typing import Any, TextIO
from yaml import FullLoader, load as load_yaml
from .utils import singleton


logger = getLogger(__name__)


# @singleton  # the parent inherits the child's singleton decorator
class FileLoader:
    def __init__(self, file_ext: str, dir_path: str) -> None:
        logger.info(f"Constructing the FileLoader")
        if not file_ext:
            msg = f"argument 'file_ext' is missing"
            logger.error(msg)
            raise ValueError(msg)
        if not dir_path:
            msg = f"argument 'dir_path' is missing"
            logger.error(msg)
            raise ValueError(msg)

        self.file_ext: str = file_ext
        self.dir_path: str = dir_path

    def __call__(self, filename_base: str) -> dict[str, Any]:
        path: str = self.generate_path(filename_base)
        with open(path, "r") as file:
            return self.load(file)

    def generate_path(self, filename_base: str) -> str:
        return join(self.dir_path, f"{filename_base}.{self.file_ext}")

    def load(self, file: TextIO) -> dict[str, Any]:
        msg = f"load(file) was not implemented"
        logger.error(msg)
        raise NotImplementedError(msg)


@singleton
class YamlLoader(FileLoader):
    def __init__(self, *args: str, **kwargs: str) -> None:
        logger.info(f"Constructing the YamlLoader")
        super().__init__("yaml", *args, **kwargs)

    def load(self, file: TextIO) -> Any:
        logger.debug(f"Loading the YAML file: {file}")
        return load_yaml(file, Loader=FullLoader)
