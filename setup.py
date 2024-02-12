import platform
import subprocess
import setuptools
from setuptools.command.build_py import build_py
from setuptools.command.build_ext import build_ext

class PoseidonExtension(setuptools.Extension):
    def __init__(self):
        self.name = "poseidon"
        setuptools.Extension.__init__(self, self.name, sources=[])


class BuildPy(build_py):
    def run(self):
        self.run_command("build_ext")
        return super().run()


class BuildPoseidon(build_ext):
    already_built = False

    def build_extension(self, ext):
        if self.already_built:
            return

        if platform.system() == "Windows":
            self._build_extension_windows()
        else:
            self._build_extension_mac_linux()

        self.already_built = True
    
    def _build_extension_windows(self):
        with subprocess.Popen(["powershell.exe", ".\\build.ps1"]) as process:
            process.wait()
            if process.returncode != 0:
                raise Exception("Build returned a non-zero code")
            
    def _build_extension_mac_linux(self):
        subprocess.run("chmod a+x ./build.sh && ./build.sh", shell=True, check=True)


if __name__ == "__main__":
    with open("README.rst", encoding="utf-8") as f:
        long_description = f.read()

    setuptools.setup(
        name="poseidon_py",
        version="0.1.4",
        description="Python implementation of Poseidon hash",
        long_description=long_description,
        author="drknzz",
        author_email="kamil.jankowski.x@gmail.com",
        url="https://github.com/drknzz/poseidon-py.git",
        ext_modules=[PoseidonExtension()],
        cmdclass={
            "build_py": BuildPy,
            "build_ext": BuildPoseidon,
        },
        python_requires=">=3.8",
        packages=["poseidon_py"],
        package_data={"poseidon_py": ["../lib_pos.*"]},
    )
