import pathlib
from setuptools import setup, find_namespace_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# This call to setup() does all the work
setup(
    name="ml-idm",
    version="0.0.2",
    description="A tool that provides a direct interface to a model you want "
    "to interact with. Get predictions, build graphs, analyse models "
    "with external tools.",
    long_description_content_type="text/markdown",
    url="https://github.com/ityutin/ml-idm",
    author="Ilya Tyutin",
    author_email="emmarrgghh@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_namespace_packages(
        exclude=(
            "*.tests",
            "*.tests.*",
            "tests.*",
            "tests",
            "*.examples",
            "*.examples.*",
            "examples.*",
            "examples",
            "*.downloads",
            "downloads",
        )
    ),
    include_package_data=True,
    install_requires=["pandas", "numpy", "joblib", "pyyaml", "streamlit", "pydantic"],
)
