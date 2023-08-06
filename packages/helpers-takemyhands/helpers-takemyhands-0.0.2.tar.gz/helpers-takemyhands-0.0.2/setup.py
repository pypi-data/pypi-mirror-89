from setuptools import setup, find_packages
from version import version

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="helpers-takemyhands",
    version=version,
    description="This help for python or django development easily.",
    long_description=long_description,
    author="TakeMyHands",
    author_email="wy0353@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keyword=[
        "helper",
        "helpers",
        "python",
        "django",
        "takemyhands",
    ],
    packages=find_packages(),
    install_requires=[""],
)