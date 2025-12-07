from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="json_therule0",
    version="0.1.0",
    author="json_therule0 contributors",
    author_email="",
    description="A library for loading, cleaning, and reading JSON data with OOP principles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/charlesnaces/OOP-FINAL-PROJECT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[],
    include_package_data=True,
)
