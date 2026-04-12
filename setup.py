"""
Setup configuration for BizLens v2.3.2
Integrated Analytics Platform — Descriptive · Diagnostic · Predictive ·
Prescriptive · Simulation · Quality · Project · Text Analytics
"""

from setuptools import setup, find_packages
from pathlib import Path

# Long description shown on PyPI project page
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="bizlens",
    version="2.3.1",
    author="Sudhanshu Singh",
    author_email="cc9n8y8tqc@privaterelay.appleid.com",
    description="Comprehensive analytics and ML platform with 13 interactive Jupyter notebooks covering statistics, regression, machine learning, clustering, process mining, time series analysis, and anomaly detection. Dual Pandas/Polars framework support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/solutiongate-learn/bizlens",
    project_urls={
        "Bug Tracker":    "https://github.com/solutiongate-learn/bizlens/issues",
        "Documentation":  "https://github.com/solutiongate-learn/bizlens#readme",
        "Source Code":    "https://github.com/solutiongate-learn/bizlens",
        "PyPI":           "https://pypi.org/project/bizlens/",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},

    # ── Classifiers ────────────────────────────────────────────────────────
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Manufacturing",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Office/Business :: Financial",
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

    # ── Core dependencies (pyproject.toml takes precedence; kept in sync) ─
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "polars>=0.14.0",
        "narwhals>=0.1.0",
        "scipy>=1.7.0",
        "matplotlib>=3.3.0",
        "seaborn>=0.11.0",
        "scikit-learn>=1.0.0",
        "statsmodels>=0.14.2",
        "PuLP>=2.7.0",
        "networkx>=2.6.0",
        "rich>=12.0.0",
    ],

    # ── Optional extras ────────────────────────────────────────────────────
    extras_require={
        # Text analytics
        "text": [
            "wordcloud>=1.8.0",
            "vaderSentiment>=3.3.0",
            "textblob>=0.17.0",
        ],
        # Advanced optimisation solvers
        "optimization": [
            "pyomo>=6.0.0",
            "cvxpy>=1.2.0",
            "gekko>=1.0.0",
            "pymoo>=0.6.0",
        ],
        # Discrete-event simulation
        "simulation": [
            "simpy>=4.0.0",
        ],
        # Dataset sources
        "kaggle": [
            "kaggle>=1.5.0",
        ],
        "openml": [
            "openml>=0.14.0",
        ],
        "worldbank": [
            "wbgapi>=1.0.0",
        ],
        # Interactive visualisation
        "interactive": [
            "plotly>=5.0.0",
            "altair>=4.0.0",
            "ipywidgets>=7.0.0",
        ],
        # Development / testing
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12.0",
            "flake8>=3.9.0",
            "black>=21.5b0",
            "mypy>=0.910",
        ],
        # Full install — everything
        "full": [
            "wordcloud>=1.8.0",
            "vaderSentiment>=3.3.0",
            "textblob>=0.17.0",
            "pyomo>=6.0.0",
            "cvxpy>=1.2.0",
            "pymoo>=0.6.0",
            "simpy>=4.0.0",
            "kaggle>=1.5.0",
            "openml>=0.14.0",
            "wbgapi>=1.0.0",
            "plotly>=5.0.0",
            "altair>=4.0.0",
        ],
    },

    # ── Keywords (shown on PyPI sidebar) ──────────────────────────────────
    keywords=[
        # Analytics pyramid
        "analytics", "descriptive-analytics", "diagnostic-analytics",
        "predictive-analytics", "prescriptive-analytics",
        # Statistics
        "statistics", "sample-vs-population", "hypothesis-testing",
        "confidence-intervals", "regression", "anova", "chi-square",
        # Machine learning
        "machine-learning", "scikit-learn", "decision-tree",
        "logistic-regression", "confusion-matrix",
        # Optimisation / OR
        "optimization", "linear-programming", "operations-research",
        "transportation-problem", "assignment-problem", "pulp", "milp",
        # Simulation
        "monte-carlo", "simulation", "npv", "risk-analysis", "bootstrap",
        # Quality / Six Sigma
        "six-sigma", "process-capability", "control-chart", "pareto",
        "fishbone", "cpk", "dpmo",
        # Project management
        "gantt-chart", "critical-path", "cpm", "pert", "project-management",
        # Text analytics
        "text-analytics", "wordcloud", "sentiment-analysis", "tfidf", "nlp",
        # Data & visualisation
        "data-science", "visualization", "pandas", "polars", "narwhals",
        "education", "business-intelligence",
    ],

    include_package_data=True,
    zip_safe=False,
)
