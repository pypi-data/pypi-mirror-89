#!/usr/bin/env python3

# https://packaging.python.org/tutorials/packaging-projects/
# https://packaging.python.org/guides/distributing-packages-using-setuptools/

import setuptools
import os
import shutil

import agunua

shutil.rmtree("./scripts")
os.mkdir("scripts")
os.symlink("../agunua.py", "scripts/agunua")
os.symlink("../sample-client.py", "scripts/agunua-sample-client.py")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agunua", # Replace with your own username
    version=agunua.VERSION,
    author="Stéphane Bortzmeyer",
    author_email="stephane+framagit@bortzmeyer.org",
    description="A library for the development of Gemini clients",
    keywords="Gemini",
    license="GPL",
    install_requires=['pyopenssl'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://framagit.org/bortzmeyer/agunua/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    package_data={
        "agunua": ["../scripts/agunua-sample-client.py"]
    },
    scripts=["scripts/agunua"]
)
