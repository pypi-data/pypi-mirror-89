import setuptools
import shutil
import os

from _parser.parser import parsed


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


copytree(parsed / "core", "chameleongram/raw/core")
copytree(parsed / "functions", "chameleongram/raw/functions")
copytree(parsed / "types", "chameleongram/raw/types")
shutil.copyfile(parsed / "_all.py", "chameleongram/raw/_all.py")

shutil.rmtree(parsed)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chameleongram",
    license="LGPLv3+",
    version="0.0.1",
    author="Davide Galilei",
    author_email="davidegalilei2018@gmail.com",
    description="An async (trio) MTProto Client written in Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/DavideGalilei/chameleongram",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        x.strip() for x in open("chameleongram/requirements.txt").read().splitlines() if x
    ]
)
