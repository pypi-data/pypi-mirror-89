from setuptools import setup
import os
README_PATH = os.path.join(os.path.dirname(__file__), "Readme.md") #Path to the Readme file
README = open(README_PATH, "r").read()
SHORT_DESCRIPTION = "Python Wrapper around the Huskoll API."
setup(
    name="huskoll",
    packages=["huskoll"],
    version="0.1.1",
    license="MIT",
    description=SHORT_DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    author="sotpotatis",
    url="https://github.com/sotpotatis/Huskoll-Python",
    download_url="https://github.com/sotpotatis/Huskoll-Python/archive/v_011.tar.gz",
    keywords=["api", "huskoll"],
    install_requires=[
        "dateutil",
        "requests"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
