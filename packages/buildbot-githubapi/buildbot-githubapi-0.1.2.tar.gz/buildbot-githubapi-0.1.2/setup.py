#!/usr/bin/env python

from setuptools import setup

VERSION = '0.1.2'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="buildbot-githubapi",
    version=VERSION,
    description="GitHub API plugin for BuildBot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Henrik Hautakoski",
    author_email="henrik@eossweden.org",
    url="https://github.com/eosswedenorg/buildbot-GitHubAPI",
    packages=[
        "src",
    ],
    requires=["Buildbot (>=2.8.0)"],
    entry_points={
        "buildbot.changes": [
            "GitHubAPI = src.githubapi:GitHubAPI"
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Build Tools",
    ]
)
