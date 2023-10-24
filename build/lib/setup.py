from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="hiram",
    version="0.0.1",
    description="An Option Pricing Library",
    package_dir={"":"hiram"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="paulbqnt",
    license="MIT",
    python_requires=">=3.10"
)