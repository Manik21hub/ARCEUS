# setup.py
from setuptools import setup, find_packages

setup(
    name="arceus",
    version="1.0.0",
    description="ARCEUS - Headless Windows Voice Assistant",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "requests",
        "tabulate",
        "pywebview"
    ],
    entry_points={
        "console_scripts": [
            "arceus=core.cli:main", 
        ]
    }
)