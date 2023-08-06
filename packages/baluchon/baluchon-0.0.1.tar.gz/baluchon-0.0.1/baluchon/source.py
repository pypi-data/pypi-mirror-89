import os
from abc import ABC, abstractmethod
from pathlib import Path

from jinja2 import Template

from .constants import EMPTY_VERSION
from .exceptions import (
    InvalidMigrationSource,
    SourceAlreadyOpenedException,
    NoMigrationException,
)
from .migration import Migration
from .validator import RaisingValidator
from .validator.schemas import SQL_FOLDER_SOURCE_SCHEMA


class Source(ABC):
    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def first(self, direction="up") -> Migration:
        pass

    @abstractmethod
    def prev(self, version: int) -> Migration:
        pass

    @abstractmethod
    def next(self, version: int) -> Migration:
        pass

    @abstractmethod
    def read_query_up(self, version: int) -> str:
        pass

    @abstractmethod
    def read_query_down(self, version: int) -> str:
        pass


class SQLFolderSource(Source):
    def __init__(self, config):
        validator = RaisingValidator()
        validator.validate(config, SQL_FOLDER_SOURCE_SCHEMA)
        self.folder = validator.document["folder"]
        self.context = validator.document["context"] or {}
        self.files = {}
        self.versions = None

    def open(self) -> None:
        if self.files:
            raise SourceAlreadyOpenedException
        path = Path(self.folder)
        for elem in path.iterdir():
            if elem.is_file() and elem.name.endswith(".sql"):
                # Extract migration number
                try:
                    parsed_name = elem.name.split("_", 1)
                    version = int(parsed_name[0])
                    direction = os.path.splitext(elem.name)[0].split(".")[-1]
                    name = ".".join(parsed_name[1].split(".")[:-2])
                    if direction not in ["up", "down"]:
                        raise InvalidMigrationSource(
                            f"{direction} is not a valid direction from {elem.name}"
                        )
                    if version not in self.files:
                        self.files[version] = {}
                    with elem.open() as file:
                        self.files[version][direction] = {
                            "identifier": name,
                            "query": Template(file.read()).render(**self.context),
                        }

                except TypeError:
                    raise InvalidMigrationSource(
                        f"Can't extract version from {elem.name}"
                    )
        if not self.files:
            raise NoMigrationException(f"No migrations has been found in {self.folder}")
        self.versions = list(sorted(list(self.files.keys())))

    def first_version(self):
        return self.versions[0]

    def next_version(self, version):
        if version == EMPTY_VERSION:
            return self.first_version()
        return self.versions[self.versions.index(version) + 1]

    def prev_version(self, version):
        index = self.versions.index(version)
        if index == 0:
            return EMPTY_VERSION
        return self.versions[self.versions.index(version) - 1]

    def first(self, direction="up") -> Migration:
        if direction not in ["up", "down"]:
            raise TypeError(f"{direction} is not a valid direction")
        version = self.first_version()
        if direction == "up":
            versions = {"version": EMPTY_VERSION, "target_version": version}
        else:
            versions = {
                "version": version,
                "target_version": EMPTY_VERSION,
            }
        try:
            file_info = self.files[version][direction]
        except (ValueError, IndexError):
            raise NoMigrationException

        return Migration(**file_info, **versions)

    def prev(self, version: int) -> Migration:
        assert type(version) is int, "Version must be an integer"
        try:
            file_info = self.files[version]["down"]
        except (ValueError, IndexError, KeyError):
            raise NoMigrationException
        return Migration(
            **file_info, version=version, target_version=self.prev_version(version)
        )

    def next(self, version: int) -> Migration:
        assert type(version) is int, "Version must be an integer"
        try:
            file_info = self.files[self.next_version(version)]["up"]
        except (ValueError, IndexError):
            raise NoMigrationException
        return Migration(
            **file_info, version=version, target_version=self.next_version(version)
        )

    def read_query_up(self, version: int) -> str:
        assert type(version) is int, "Version must be an integer"
        try:
            file_info = self.files[version]["up"]
        except (ValueError, IndexError):
            raise NoMigrationException
        return file_info["query"]

    def read_query_down(self, version: int) -> str:
        assert type(version) is int, "Version must be an integer"
        try:
            file_info = self.files[version]["down"]
        except (ValueError, IndexError):
            raise NoMigrationException
        return file_info["query"]

    def close(self) -> None:
        pass


class PythonModuleSource(Source):
    pass


class S3FolderSource(Source):
    pass
