"""
Setup configuration for BizLens
Integrated Analytics Platform - Descriptive, Diagnostic & Predictive Analytics
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README_FINAL.md").read_text(encoding="utf-8")

setup(
    name="bizlens",
    version="2.2.0",
    author="Sudhanshu Singh",
    author_email="cc9n8y8tqc@privaterelay.appleid.com",
    description="Integrated Analytics Platform — Descriptive, Diagnostic, Predictive, Prescriptive & Simulation Analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/solutiongate-learn/bizlens",
    project_urls={
        "Bug Tracker": "https://github.com/solutiongate-learn/bizlens/issues",
        "Documentation": "https://github.com/solutiongate-learn/bizlens#readme",
        "Source Code": "https://github.com/solutiongate-learn/bizlens",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "polars>=0.14.0",
        "narwhals>=0.1.0",
        "matplotlib>=3.3.0",
        "seaborn>=0.11.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12.0",
            "flake8>=3.9.0",
            "black>=21.5b0",
            "mypy>=0.910",
        ],
        "viz": [
            "plotly>=5.0.0",  # Optional for interactive plots
            "altair>=4.0.0",  # Optional for Altair plots
        ],
    },
    include_package_data=True,
    keywords=[
        "statistics",
        "analytics",
        "education",
        "visualization",
        "data-science",
        "descriptive-statistics",
        "central-tendency",
    ],
    zip_safe=False,
)
