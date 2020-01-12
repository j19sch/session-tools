import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="session-noter",
    version="v0.2.0",
    packages=["session_noter"],
    entry_points={
        "console_scripts": [
            "session-notetaker = session_noter.session_notetaker:main",
            "session-printer = session_noter.session_printer:main",
            "session-analyzer = session_noter.session_analyzer:main",
        ]
    },
    url="https://github.com/j19sch/session-noter",
    license="MIT",
    author="Joep Schuurkes",
    author_email="j19sch@gmail.com",
    description="note-taking tools for session-based test management",
    long_description=read("README.md"),
    python_requires=">=3.6",
    install_requires=["pyyaml", "mss"],
    tests_require=["pytest", "flake8", "black", "mypy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console" "Topic :: Software Development :: Testing",
    ],
)
