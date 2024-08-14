from logging import warning
from os import walk
from pkgutil import walk_packages
from itertools import chain
from pathlib import Path, PurePath
from types import ModuleType
from typing import Set, Any, Generator
from importlib import import_module


import_module


def import_package_modules(
    package: ModuleType,
    shallow: bool = True
) -> Generator[ModuleType, None, None]:
    for module in find_all_importables(package, shallow):
        yield import_module(module)


def find_all_importables(
    package: ModuleType,
    shallow: bool = True
) -> Set[str]:
    """Find all importables in the project and return them in order.

    This solution is based on a solution by Sviatoslav Sydorenko (webknjaz)
    * https://github.com/sanitizers/octomachinery/blob/2428877/tests/circular_imports_test.py
    """
    return set(
        chain.from_iterable(
            _discover_path_importables(Path(p), package.__name__, shallow)
            for p in package.__path__
        )
    )


# TODO : Add proper types
def _discover_path_importables(
    pkg_pth,
    pkg_name,
    shallow
) -> Generator[Any, Any, Any]:
    """Yield all importables under a given path and package.

    This solution is based on a solution by Sviatoslav Sydorenko (webknjaz)
    * https://github.com/sanitizers/octomachinery/blob/2428877/tests/circular_imports_test.py
    """
    for dir_path, _d, file_names in walk(pkg_pth):
        pkg_dir_path: Path = Path(dir_path)

        if pkg_dir_path.parts[-1] == '__pycache__':
            continue

        if all(Path(_).suffix != '.py' for _ in file_names):
            continue

        rel_pt: PurePath = pkg_dir_path.relative_to(pkg_pth)
        pkg_pref: str = '.'.join((pkg_name, ) + rel_pt.parts)

        if '__init__.py' not in file_names:
            warning(f"'{pkg_dir_path}' seems to be missing an '__init__.py'. This might cause issues.")

        yield from (
            pkg_path
            for _, pkg_path, _ in walk_packages(
                (str(pkg_dir_path), ), prefix=f'{pkg_pref}.',
            )
        )

        if not shallow:
            break
