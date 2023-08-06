from setuptools import find_packages, setup

with open("README.md", "r") as file:
    readme_description = file.read()

with open("requirements.txt", "r") as file:
    requirements = file.read()

setup(
    name="dop_python_pip_package",
    version="0.0.4",
    author="Ryan",
    author_email="ryanang.jy@gmail.com",
    description="Python utils library",
    long_description=readme_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RyanAngJY/dop_python_pip_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    install_requires=[
        requirements
    ],
    dependency_links=[]
)
