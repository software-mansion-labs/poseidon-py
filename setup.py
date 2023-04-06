import subprocess
import setuptools
from setuptools.command import build_py
from setuptools.command import build_ext

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

        subprocess.run("chmod a+x ./build.sh && ./build.sh", shell=True, check=True)
        self.already_built = True


if __name__ == "__main__":
    with open("README.rst", encoding="utf-8") as f:
        long_description = f.read()

    setuptools.setup(
        name="poseidon_py",
        version="0.1.0",
        description="Python implementation of Poseidon hash",
        long_description=long_description,
        author="drknzz",
        author_email="kamil.jankowski.x@gmail.com",
        url="https://github.com/drknzz/poseidon-py.git",
        extras_require={"build": ["make"]},
        ext_modules=[PoseidonExtension()],
        cmdclass={
            "build_py": BuildPy,
            "build_ext": BuildPoseidon,
        },
        python_requires=">=3.9",
        packages=["poseidon_py"],
        package_data={"poseidon_py": ["lib_pos.*"]},
    )
