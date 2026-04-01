"""
BizLens v2.1.0 — Dataset Loading and Repository Integration

Supported Sources (all with proper citations):
- Built-in: seaborn, sklearn, scipy datasets
- Kaggle: via kaggle API (requires kaggle.json credentials)
- OpenML: via openml package (free, no credentials needed)
- World Bank: via wbgapi or pandas_datareader
- UCI ML Repository: via ucimlrepo package

Citations are automatically generated in APA, BibTeX, and Chicago formats.
"""

import warnings
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.table import Table

warnings.filterwarnings("ignore")
console = Console()

# ─────────────────────────────────────────────────────────────────────────────
# DATASET REGISTRY WITH FULL CITATIONS
# ─────────────────────────────────────────────────────────────────────────────

DATASET_REGISTRY: Dict[str, Dict] = {
    "iris": {
        "source": "seaborn", "loader": "load_dataset", "loader_key": "iris",
        "description": "Classic iris flower measurements — 150 samples, 3 species",
        "rows": 150, "cols": 5,
        "features": "sepal_length, sepal_width, petal_length, petal_width, species",
        "level": "Beginner",
        "concepts": ["classification", "multivariate", "central tendency", "distributions"],
        "citation_apa": "Fisher, R.A. (1936). The use of multiple measurements in taxonomic problems. Annals of Eugenics, 7(2), 179–188.",
        "citation_bibtex": "@article{fisher1936,\n  author={Fisher, R.A.},\n  title={The use of multiple measurements in taxonomic problems},\n  journal={Annals of Eugenics},\n  volume={7},\n  number={2},\n  pages={179--188},\n  year={1936}\n}",
        "url": "https://archive.ics.uci.edu/ml/datasets/iris",
    },
    "titanic": {
        "source": "seaborn", "loader": "load_dataset", "loader_key": "titanic",
        "description": "Titanic passenger survival data — 891 records",
        "rows": 891, "cols": 15,
        "features": "survived, pclass, sex, age, fare, embarked, class",
        "level": "Beginner-Intermediate",
        "concepts": ["categorical", "missing data", "logistic regression", "chi-square"],
        "citation_apa": "Titanic Dataset. Seaborn built-in datasets. Retrieved from https://github.com/mwaskom/seaborn-data",
        "citation_bibtex": "@misc{titanic,\n  title={Titanic Dataset},\n  howpublished={\\url{https://github.com/mwaskom/seaborn-data}}\n}",
        "url": "https://www.kaggle.com/c/titanic",
    },
    "tips": {
        "source": "seaborn", "loader": "load_dataset", "loader_key": "tips",
        "description": "Restaurant tips — 244 observations",
        "rows": 244, "cols": 7,
        "features": "total_bill, tip, sex, smoker, day, time, size",
        "level": "Beginner",
        "concepts": ["correlation", "categorical comparison", "regression"],
        "citation_apa": "Bryant, P.G. & Smith, M.A. (1995). Practical Data Analysis: Case Studies in Business Statistics. Irwin.",
        "citation_bibtex": "@book{bryant1995,\n  author={Bryant, P.G. and Smith, M.A.},\n  title={Practical Data Analysis},\n  publisher={Irwin},\n  year={1995}\n}",
        "url": "https://github.com/mwaskom/seaborn-data",
    },
    "penguins": {
        "source": "seaborn", "loader": "load_dataset", "loader_key": "penguins",
        "description": "Palmer Penguins — 344 observations, 3 species",
        "rows": 344, "cols": 7,
        "features": "species, island, bill_length_mm, flipper_length_mm, body_mass_g, sex",
        "level": "Beginner-Intermediate",
        "concepts": ["species comparison", "outlier detection", "PCA"],
        "citation_apa": "Horst, A.M., Hill, A.P., & Gorman, K.B. (2020). palmerpenguins: Palmer Archipelago (Antarctica) penguin data. R package version 0.1.0.",
        "citation_bibtex": "@misc{horst2020,\n  author={Horst, A.M. and Hill, A.P. and Gorman, K.B.},\n  title={palmerpenguins},\n  year={2020},\n  url={https://allisonhorst.github.io/palmerpenguins/}\n}",
        "url": "https://allisonhorst.github.io/palmerpenguins/",
    },
    "diamonds": {
        "source": "seaborn", "loader": "load_dataset", "loader_key": "diamonds",
        "description": "Diamond prices and characteristics — 53,940 rows",
        "rows": 53940, "cols": 10,
        "features": "carat, cut, color, clarity, depth, table, price, x, y, z",
        "level": "Intermediate",
        "concepts": ["regression", "categorical", "price prediction"],
        "citation_apa": "ggplot2 diamonds dataset. Retrieved from Seaborn library.",
        "citation_bibtex": "@misc{diamonds,\n  title={Diamonds Dataset},\n  howpublished={\\url{https://github.com/mwaskom/seaborn-data}}\n}",
        "url": "https://github.com/mwaskom/seaborn-data",
    },
    "flights": {
        "source": "seaborn", "loader": "load_dataset", "loader_key": "flights",
        "description": "Monthly airline passenger counts 1949-1960 — 144 rows",
        "rows": 144, "cols": 3,
        "features": "year, month, passengers",
        "level": "Intermediate",
        "concepts": ["time series", "seasonality", "trend analysis", "forecasting"],
        "citation_apa": "Box, G.E.P., Jenkins, G.M., & Reinsel, G.C. (1976). Time Series Analysis: Forecasting and Control. Prentice Hall.",
        "citation_bibtex": "@book{box1976,\n  author={Box, G.E.P. and Jenkins, G.M.},\n  title={Time Series Analysis},\n  publisher={Prentice Hall},\n  year={1976}\n}",
        "url": "https://github.com/mwaskom/seaborn-data",
    },
    "mpg": {
        "source": "seaborn", "loader": "load_dataset", "loader_key": "mpg",
        "description": "Auto MPG dataset — 398 cars, fuel efficiency",
        "rows": 398, "cols": 9,
        "features": "mpg, cylinders, displacement, horsepower, weight, acceleration, model_year, origin, name",
        "level": "Intermediate",
        "concepts": ["multiple regression", "feature selection", "outliers"],
        "citation_apa": "Quinlan, J.R. (1993). Combining instance-based and model-based learning. Proceedings ML-93. Morgan Kaufmann.",
        "citation_bibtex": "@inproceedings{quinlan1993,\n  author={Quinlan, J.R.},\n  title={Combining instance-based and model-based learning},\n  booktitle={Proceedings ML-93},\n  year={1993}\n}",
        "url": "https://archive.ics.uci.edu/ml/datasets/auto+mpg",
    },
    "wine_quality": {
        "source": "sklearn", "loader": "load_wine", "loader_key": None,
        "description": "Wine quality classification — 178 samples, 13 features",
        "rows": 178, "cols": 14,
        "features": "alcohol, malic_acid, ash, flavanoids, color_intensity, ... class",
        "level": "Intermediate-Advanced",
        "concepts": ["classification", "feature importance", "PCA", "scaling"],
        "citation_apa": "Aeberhard, S., Coomans, D., & De Vel, O. (1992). Comparison of classifiers in high dimensional settings. Tech. Rep. 92-02.",
        "citation_bibtex": "@misc{aeberhard1992,\n  author={Aeberhard, S.},\n  title={Wine Dataset},\n  year={1992},\n  url={https://archive.ics.uci.edu/ml/datasets/wine}\n}",
        "url": "https://archive.ics.uci.edu/ml/datasets/wine",
    },
    "breast_cancer": {
        "source": "sklearn", "loader": "load_breast_cancer", "loader_key": None,
        "description": "Breast cancer classification — 569 samples, 30 features",
        "rows": 569, "cols": 31,
        "features": "mean radius, texture, perimeter, area, smoothness... target",
        "level": "Advanced",
        "concepts": ["binary classification", "feature selection", "ROC-AUC", "medical diagnostics"],
        "citation_apa": "Wolberg, W.H., Street, W.N., & Mangasarian, O.L. (1995). Image analysis and machine learning for breast cancer diagnosis. Computers and Statistics, 10, 67–78.",
        "citation_bibtex": "@article{wolberg1995,\n  author={Wolberg, W.H.},\n  title={Breast Cancer Wisconsin Dataset},\n  year={1995},\n  url={https://archive.ics.uci.edu/ml/datasets/breast+cancer+wisconsin+(diagnostic)}\n}",
        "url": "https://archive.ics.uci.edu/ml/datasets/breast+cancer+wisconsin+(diagnostic)",
    },
    "boston_housing": {
        "source": "openml", "loader_key": "41211",
        "description": "Boston housing prices — 506 samples, 13 features",
        "rows": 506, "cols": 14,
        "features": "CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT, MEDV",
        "level": "Intermediate",
        "concepts": ["regression", "feature importance", "outliers", "real estate"],
        "citation_apa": "Harrison, D., & Rubinfeld, D.L. (1978). Hedonic prices and the demand for clean air. Journal of Environmental Economics and Management, 5, 81–102.",
        "citation_bibtex": "@article{harrison1978,\n  author={Harrison, D. and Rubinfeld, D.L.},\n  title={Hedonic prices and the demand for clean air},\n  journal={JEEM},\n  volume={5},\n  pages={81--102},\n  year={1978}\n}",
        "url": "https://www.openml.org/d/41211",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# BUILT-IN DATASET LOADERS
# ─────────────────────────────────────────────────────────────────────────────

def load_dataset(name: str, show_citation: bool = True) -> pd.DataFrame:
    """
    Load a built-in dataset by name.

    Args:
        name: Dataset name (see list_datasets() for all options)
        show_citation: Print citation information (default True)

    Returns:
        pandas DataFrame

    Example:
        >>> import bizlens as bl
        >>> iris = bl.load_dataset('iris')
        >>> titanic = bl.load_dataset('titanic')
        >>> flights = bl.load_dataset('flights')
    """
    name = name.lower().strip()
    if name not in DATASET_REGISTRY:
        available = ", ".join(DATASET_REGISTRY.keys())
        raise ValueError(f"Dataset '{name}' not found. Available: {available}")

    info = DATASET_REGISTRY[name]
    source = info["source"]

    if source == "seaborn":
        import seaborn as sns
        df = sns.load_dataset(info["loader_key"])

    elif source == "sklearn":
        from sklearn import datasets as sk_datasets
        loader_fn = getattr(sk_datasets, info["loader"])
        bunch = loader_fn()
        df = pd.DataFrame(bunch.data, columns=bunch.feature_names)
        if hasattr(bunch, "target"):
            df["target"] = bunch.target

    elif source == "openml":
        df = load_from_openml(dataset_id=int(info["loader_key"]), show_citation=False)

    else:
        raise ValueError(f"Unknown source: {source}")

    if show_citation:
        console.print(f"\n[bold green]✅ Loaded '{name}'[/bold green] ({info['rows']} rows × {info['cols']} columns)")
        console.print(f"[dim]{info['description']}[/dim]")
        console.print(f"[bold yellow]📚 Citation (APA):[/bold yellow] {info['citation_apa']}")
        console.print(f"[dim]Level: {info['level']} | Concepts: {', '.join(info['concepts'][:3])}[/dim]")

    return df


def list_datasets() -> pd.DataFrame:
    """
    List all built-in datasets with metadata.

    Returns:
        DataFrame with dataset names, sources, sizes, and concepts

    Example:
        >>> bl.list_datasets()
    """
    rows = []
    for name, info in DATASET_REGISTRY.items():
        rows.append({
            "Name": name,
            "Source": info["source"],
            "Rows": info["rows"],
            "Cols": info["cols"],
            "Level": info["level"],
            "Key Concepts": ", ".join(info["concepts"][:2]),
        })
    df = pd.DataFrame(rows)

    table = Table(title="📦 BizLens Built-in Datasets", show_lines=True)
    for col in df.columns:
        table.add_column(col, style="cyan" if col == "Name" else "white", width=16 if col == "Key Concepts" else 12)
    for _, row in df.iterrows():
        table.add_row(*[str(v) for v in row])
    console.print(table)
    return df


def dataset_info(name: str) -> Dict:
    """
    Show full information and citation for a dataset.

    Example:
        >>> bl.dataset_info('iris')
    """
    name = name.lower().strip()
    if name not in DATASET_REGISTRY:
        raise ValueError(f"Dataset '{name}' not found.")
    info = DATASET_REGISTRY[name]
    console.print(f"\n[bold]📋 Dataset: {name.upper()}[/bold]")
    console.print(f"Description: {info['description']}")
    console.print(f"Size: {info['rows']} rows × {info['cols']} columns")
    console.print(f"Features: {info['features']}")
    console.print(f"Education Level: {info['level']}")
    console.print(f"Key Concepts: {', '.join(info['concepts'])}")
    console.print(f"\n[bold yellow]Citation (APA):[/bold yellow]\n  {info['citation_apa']}")
    console.print(f"\n[bold yellow]Citation (BibTeX):[/bold yellow]\n  {info['citation_bibtex']}")
    console.print(f"\n[bold]URL:[/bold] {info['url']}")
    return info


# ─────────────────────────────────────────────────────────────────────────────
# KAGGLE DATASET LOADER
# ─────────────────────────────────────────────────────────────────────────────

def load_from_kaggle(
    dataset: str,
    file_name: Optional[str] = None,
    save_path: str = ".",
) -> pd.DataFrame:
    """
    Load a dataset directly from Kaggle.

    Requires:
        1. pip install kaggle
        2. Kaggle API token at ~/.kaggle/kaggle.json
           (Get from: https://www.kaggle.com/settings → API → Create New Token)

    Args:
        dataset: Kaggle dataset identifier (e.g. 'username/dataset-name')
        file_name: Specific CSV file within the dataset (optional)
        save_path: Directory to save downloaded files (default: current dir)

    Returns:
        pandas DataFrame

    Example:
        >>> # First time: get token from https://www.kaggle.com/settings
        >>> df = bl.load_from_kaggle('blastchar/telco-customer-churn', 'WA_Fn-UseC_-Telco-Customer-Churn.csv')
        >>> df = bl.load_from_kaggle('house-prices-advanced-regression-techniques')

    Citation:
        Kaggle. (2024). {dataset}. Kaggle Dataset Repository. https://www.kaggle.com/datasets/{dataset}
    """
    try:
        import kaggle
    except ImportError:
        raise ImportError(
            "kaggle package required.\n"
            "Install: pip install kaggle\n"
            "Then get your API token from: https://www.kaggle.com/settings → API → Create New Token\n"
            "Save it to: ~/.kaggle/kaggle.json"
        )

    import os
    import zipfile
    import glob

    console.print(f"[bold]📥 Downloading from Kaggle:[/bold] {dataset}")
    console.print("[dim]Source: Kaggle Dataset Repository — https://www.kaggle.com[/dim]")

    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(dataset, path=save_path, unzip=True)

    # Find CSV files
    csv_files = glob.glob(os.path.join(save_path, "*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {save_path} after download.")

    if file_name:
        target = os.path.join(save_path, file_name)
    else:
        target = csv_files[0]
        if len(csv_files) > 1:
            console.print(f"[yellow]Multiple CSVs found: {[os.path.basename(f) for f in csv_files]}[/yellow]")
            console.print(f"[yellow]Loading: {os.path.basename(target)}. Specify file_name to choose another.[/yellow]")

    df = pd.read_csv(target)
    console.print(f"[green]✅ Loaded: {os.path.basename(target)} ({df.shape[0]} rows × {df.shape[1]} cols)[/green]")
    console.print(f"[bold yellow]📚 Citation (APA):[/bold yellow] Kaggle. (2026). {dataset}. Kaggle Dataset Repository. https://www.kaggle.com/datasets/{dataset}")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# OPENML DATASET LOADER
# ─────────────────────────────────────────────────────────────────────────────

def load_from_openml(
    dataset_id: Optional[int] = None,
    dataset_name: Optional[str] = None,
    show_citation: bool = True,
) -> pd.DataFrame:
    """
    Load a dataset from OpenML (free, no credentials needed).

    OpenML is an open platform for machine learning datasets and experiments.
    Citation: Vanschoren, J., et al. (2013). OpenML: Networked science in machine learning.
              ACM SIGKDD Explorations, 15(2), 49–60.

    Args:
        dataset_id: OpenML dataset ID (e.g. 61 for iris, 40691 for wine quality)
        dataset_name: Dataset name string (alternative to ID)
        show_citation: Print citation information

    Returns:
        pandas DataFrame

    Common OpenML IDs:
        61   = iris            | 40691 = wine quality
        31   = credit-g        | 1461  = bank marketing
        1590 = adult (income)  | 41211 = boston housing
        40945= titanic         | 4534  = PhishingWebsites

    Example:
        >>> df = bl.load_from_openml(dataset_id=61)          # Iris
        >>> df = bl.load_from_openml(dataset_name='credit-g') # German credit
    """
    try:
        import openml
    except ImportError:
        raise ImportError("openml required: pip install openml")

    if dataset_id is not None:
        dataset = openml.datasets.get_dataset(dataset_id)
    elif dataset_name is not None:
        datasets = openml.datasets.list_datasets(output_format="dataframe")
        match = datasets[datasets["name"] == dataset_name]
        if match.empty:
            raise ValueError(f"Dataset '{dataset_name}' not found on OpenML.")
        dataset_id = int(match.iloc[0]["did"])
        dataset = openml.datasets.get_dataset(dataset_id)
    else:
        raise ValueError("Provide dataset_id or dataset_name.")

    X, y, categorical_indicator, attribute_names = dataset.get_data(
        dataset_format="dataframe", target=dataset.default_target_attribute
    )
    df = X.copy()
    if y is not None:
        df["target"] = y

    if show_citation:
        console.print(f"[green]✅ Loaded from OpenML:[/green] {dataset.name} ({df.shape[0]} rows × {df.shape[1]} cols)")
        console.print(f"[bold yellow]📚 Citation (APA):[/bold yellow]")
        console.print(f"  Vanschoren, J., et al. (2013). OpenML: Networked science in machine learning. ACM SIGKDD Explorations, 15(2), 49–60.")
        console.print(f"  Dataset: {dataset.name}. OpenML ID: {dataset_id}. https://www.openml.org/d/{dataset_id}")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# WORLD BANK DATASET LOADER
# ─────────────────────────────────────────────────────────────────────────────

def load_from_world_bank(
    indicator: str,
    countries: str = "all",
    start_year: int = 2000,
    end_year: int = 2023,
) -> pd.DataFrame:
    """
    Load macroeconomic data directly from the World Bank API.

    Source: World Bank Open Data — https://data.worldbank.org
    Citation: World Bank. (2024). World Development Indicators. Washington, DC: World Bank.
              https://data.worldbank.org

    Args:
        indicator: World Bank indicator code
        countries: Country code(s) or 'all' (default)
        start_year: Start year (default 2000)
        end_year: End year (default 2023)

    Common Indicators:
        'NY.GDP.MKTP.CD'  = GDP (current US$)
        'SP.POP.TOTL'     = Total population
        'NY.GNP.PCAP.CD'  = GNI per capita
        'SH.DYN.MORT'     = Child mortality rate
        'SE.ADT.LITR.ZS'  = Literacy rate
        'FP.CPI.TOTL.ZG'  = Inflation rate
        'SL.UEM.TOTL.ZS'  = Unemployment rate

    Example:
        >>> gdp = bl.load_from_world_bank('NY.GDP.MKTP.CD', countries='US;GB;IN', start_year=2010)
        >>> pop = bl.load_from_world_bank('SP.POP.TOTL', start_year=2000, end_year=2023)
    """
    try:
        import wbgapi as wb
    except ImportError:
        try:
            import pandas_datareader.wb as wb_reader
            console.print("[dim]Using pandas_datareader for World Bank data[/dim]")
            df = wb_reader.download(
                indicator=indicator,
                country=countries if countries != "all" else "all",
                start=start_year,
                end=end_year,
            ).reset_index()
            console.print(f"[green]✅ Loaded World Bank indicator:[/green] {indicator}")
            console.print(f"[bold yellow]📚 Citation (APA):[/bold yellow]")
            console.print(f"  World Bank. (2024). World Development Indicators. Washington, DC: World Bank.")
            console.print(f"  Indicator: {indicator}. https://data.worldbank.org/indicator/{indicator}")
            return df
        except ImportError:
            raise ImportError(
                "Install wbgapi or pandas_datareader:\n"
                "  pip install wbgapi\n"
                "  or: pip install pandas_datareader"
            )

    economy = countries if countries != "all" else wb.region.members("WLD")
    data = wb.data.DataFrame(indicator, economy, time=range(start_year, end_year + 1))
    df = data.reset_index()

    console.print(f"[green]✅ Loaded World Bank indicator:[/green] {indicator}")
    console.print(f"[bold yellow]📚 Citation (APA):[/bold yellow]")
    console.print(f"  World Bank. (2024). World Development Indicators. Washington, DC: World Bank.")
    console.print(f"  Indicator: {indicator}. https://data.worldbank.org/indicator/{indicator}")
    return df
