import re
import subprocess
from setuptools import setup

try:
    ret = subprocess.check_output(
        "git describe --tags --abbrev=0",
        shell=True,
    )
    version = ret.decode("utf-8").strip()
except:
    version = "master"

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="ohnoyoudidnt",
    version="0.1",
    author="Vasista Vovveti",
    author_email="vasistavovveti@gmail.com",
    description="doc8 linter for frc-docs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wpilibsuite/ohnoyoudidnt",
    packages=["ohnoyoudidnt"],
    entry_points={
        "doc8.extension.check": [
            f"{s.lower()} = ohnoyoudidnt.checks:{s}"
            for s in re.findall(
                r"\nclass (.*?)\(", open("./ohnoyoudidnt/checks.py", "r").read()
            )
        ]
    },
    install_requires=[
        "more_itertools>=8.6.0",
        "doc8>=0.8.1",
        "docutils>=0.16",
    ],
    classifiers=[
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Sphinx :: Extension",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
)
