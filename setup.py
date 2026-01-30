""" Setup script for the nt_users_tool package"""
from setuptools import setup, find_packages

setup(
    name="gestion_bancaire",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        # Add dependencies from requirements.txt or pyproject.toml
        # Example: "pandas>=1.3.0", "openpyxl>=3.0.0"
    ],
    entry_points={
        "console_scripts": [
            # Add CLI entry points if applicable
            # Example: "nt-users-tool=nt_users_tool.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    extras_require={
        "dev": ["pylint"],
    },
)
