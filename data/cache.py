from __future__ import annotations

import functools
import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

VERSION_DATE = datetime(2022, 12, 28, tzinfo=timezone.utc)
CACHE_ROOT = Path(os.getcwd()).joinpath('data_cache')
VERSION_FILE = '.version'


def _verify_cache_dir(path: Path, versions: tuple[datetime, ...]):
    version_text = '\n'.join(version.isoformat() for version in versions)
    version_file = path.joinpath(VERSION_FILE)
    if version_file.exists():
        existing_version_text = version_file.read_text().strip()
        if version_text == existing_version_text:
            return

    if path.exists():
        shutil.rmtree(path)
    path.mkdir()
    version_file.write_text(version_text + '\n')


@functools.cache
def _get_root_dir() -> Path:
    _verify_cache_dir(CACHE_ROOT, (VERSION_DATE,))
    return CACHE_ROOT


@dataclass(frozen=True)
class Cache:
    id: str
    version: datetime = VERSION_DATE
    dependencies: tuple[Cache, ...] = ()

    @property
    def all_dependencies(self) -> tuple[Cache, ...]:
        return tuple(set().union(
            dep.all_dependencies
            for dep in self.dependencies
        ))

    def dir(self) -> Path:
        cache_dir = _get_root_dir().joinpath(self.id)
        versions = (self.version,) + tuple(dep.version for dep in self.all_dependencies)
        _verify_cache_dir(cache_dir, versions)
        return cache_dir


POPULATION_CACHE = Cache('population', version=datetime(2024, 2, 4))
