from setuptools import setup
import pathlib
HERE = pathlib.Path(__file__).parent
README_PATH = "Readme.md"  #Path to the Readme file
README = (HERE / "Readme.md").read_text()
SHORT_DESCRIPTION = "Python Wrapper around the Huskoll API."
setup(
    name="huskoll",
    packages=["huskoll"],
    version="0.1.3",
    license="MIT",
    description=SHORT_DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sotpotatis/Huskoll-Python",
    author="Albin Seijmer",
    author_email="albin@albins.website",
    #download_url="https://github.com/sotpotatis/Huskoll-Python/archive/huskoll-0.1.1.tar.gz",
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
