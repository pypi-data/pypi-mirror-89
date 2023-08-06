from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="berply",
    version="0.0.1",
    url="https://github.com/uplol/berply",
    description="simple kubernetes config management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["jinja2", "pyyaml"],
    setup_requires=["pytest-runner"],
    entry_points={"console_scripts": ["berply=berply.main:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
