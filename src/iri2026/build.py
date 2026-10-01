from __future__ import annotations

import importlib.resources as resources
import os
import shutil
import subprocess
import sys


def build() -> None:
    """Build the bundled Fortran driver with CMake."""
    cmake = shutil.which("cmake")
    if not cmake:
        raise FileNotFoundError("CMake not available")

    with resources.as_file(resources.files(__package__).joinpath("CMakeLists.txt")) as cmake_file:
        source = cmake_file.parent
        build_dir = source / "build"
        generator = []
        if sys.platform == "win32" and not os.environ.get("CMAKE_GENERATOR"):
            generator = ["-G", "MinGW Makefiles"]
        subprocess.check_call([cmake, f"-S{source}", f"-B{build_dir}", *generator])
        subprocess.check_call([cmake, "--build", str(build_dir), "--parallel"])
