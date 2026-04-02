"""
BizLens v2.2.8 — Built-in Sample Datasets with Citations
"""

import warnings
import polars as pl
from rich.console import Console
from rich.table import Table

warnings.filterwarnings("ignore")
console = Console()

# Complete Registry of Classic Teaching Datasets
DATASET_REGISTRY = {
    "tips": {
        "source": "seaborn",
        "loader_key": "tips",
        "description": "Restaurant tips dataset — 244 observations",
        "rows": 244,
        "cols": 7,
        "level": "Beginner",
        "concepts": ["correlation", "categorical analysis", "regression"],
        "citation_apa": "Bryant, P.G. & Smith, M.A. (1995). Practical Data Analysis: Case Studies in Business Statistics. Irwin.",
    },
    "iris": {
        "source": "seaborn",
        "loader_key": "iris",
        "description": "Iris flower dataset — 150 samples, 3 species",
        "rows": 150,
        "cols": 5,
        "level": "Beginner",
        "concepts": ["classification", "multivariate analysis", "clustering"],
        "citation_apa": "Fisher, R.A. (1936). The use of multiple measurements in taxonomic problems. Annals of Eugenics, 7(2), 179–188.",
    },
    "titanic": {
        "source": "seaborn",
        "loader_key": "titanic",
        "description": "Titanic survival data — 891 passengers",
        "rows": 891,
        "cols": 15,
        "level": "Beginner-Intermediate",
        "concepts": ["missing values", "categorical analysis", "survival prediction"],
        "citation_apa": "Titanic Dataset from Seaborn library.",
    },
    "penguins": {
        "source": "seaborn",
        "loader_key": "penguins",
        "description": "Palmer Penguins dataset — 344 observations",
        "rows": 344,
        "cols": 7,
        "level": "Beginner-Intermediate",
        "concepts": ["species comparison", "outlier detection"],
        "citation_apa": "Horst, A.M., Hill, A.P., & Gorman, K.B. (2020). palmerpenguins R package.",
    },
    "diamonds": {
        "source": "seaborn",
        "loader_key": "diamonds",
        "description": "Diamonds price and attributes — 53,940 records",
        "rows": 53940,
        "cols": 10,
        "level": "Intermediate",
        "concepts": ["regression", "price prediction", "large dataset"],
        "citation_apa": "ggplot2 diamonds dataset.",
    },
    "mpg": {
        "source": "seaborn",
        "loader_key": "mpg",
        "description": "Auto MPG dataset — fuel efficiency of cars",
        "rows": 398,
        "cols": 9,
        "level": "Intermediate",
        "concepts": ["multiple regression", "feature selection", "outliers"],
        "citation_apa": "Quinlan, J.R. (1993). Combining instance-based and model-based learning.",
    },
    "flights": {
        "source": "seaborn",
        "loader_key": "flights",
        "description": "NYC flights data — time series example",
        "rows": 336776,
        "cols": 4,
        "level": "Intermediate",
        "concepts": ["time series", "grouping", "trend analysis"],
        "citation_apa": "Seaborn flights dataset.",
    },
    "wine_quality": {
        "source": "sklearn",
        "loader_key": "wine",
        "description": "Wine quality classification dataset",
        "rows": 178,
        "cols": 14,
        "level": "Intermediate-Advanced",
        "concepts": ["classification", "feature importance"],
        "citation_apa": "Aeberhard, S., Coomans, D., & De Vel, O. (1992). Comparison of classifiers.",
    },
    "breast_cancer": {
        "source": "sklearn",
        "loader_key": "breast_cancer",
        "description": "Breast cancer Wisconsin diagnostic dataset",
        "rows": 569,
        "cols": 31,
        "level": "Advanced",
        "concepts": ["binary classification", "medical diagnostics"],
        "citation_apa": "Wolberg, W.H., Street, W.N., & Mangasarian, O.L. (1995).",
    },
}

def list_datasets():
    """List all available built-in datasets."""
    rows = []
    for name, info in DATASET_REGISTRY.items():
        rows.append({
            "Name": name,
            "Rows": info["rows"],
            "Cols": info["cols"],
            "Level": info["level"],
            "Key Concepts": ", ".join(info["concepts"][:3]),
        })
    table = Table(title="📦 BizLens Built-in Datasets")
    for col in ["Name", "Rows", "Cols", "Level", "Key Concepts"]:
        table.add_column(col, style="cyan" if col == "Name" else "white")
    for row in rows:
        table.add_row(*[str(v) for v in row.values()])
    console.print(table)
    return [name for name in DATASET_REGISTRY.keys()]


def dataset_info(name: str):
    """Show detailed information and citation for a dataset."""
    name = name.lower().strip()
    if name not in DATASET_REGISTRY:
        raise ValueError(f"Dataset '{name}' not found. Available: {list_datasets()}")
    
    info = DATASET_REGISTRY[name]
    console.print(f"\n[bold]📋 Dataset: {name.upper()}[/bold]")
    console.print(f"Description: {info['description']}")
    console.print(f"Size: {info['rows']} rows × {info['cols']} columns")
    console.print(f"Level: {info['level']}")
    console.print(f"Key Concepts: {', '.join(info['concepts'])}")
    console.print(f"\n[bold yellow]Citation (APA):[/bold yellow]\n {info['citation_apa']}")
    return info


def load_dataset(name: str, show_citation: bool = True) -> pl.DataFrame:
    """Load a built-in dataset."""
    name = name.lower().strip()
    if name not in DATASET_REGISTRY:
        raise ValueError(f"Dataset '{name}' not found. Available: {list_datasets()}")
    
    info = DATASET_REGISTRY[name]
    import seaborn as sns
    df_pd = sns.load_dataset(info["loader_key"])
    df = pl.from_pandas(df_pd)

    if show_citation:
        console.print(f"[bold green]✅ Loaded '{name}'[/bold green] ({info['rows']} rows × {info['cols']} columns)")
        console.print(f"[dim]{info['description']}[/dim]")
        console.print(f"[bold yellow]📚 Citation (APA):[/bold yellow] {info['citation_apa']}")
        console.print(f"[dim]Level: {info['level']} | Concepts: {', '.join(info['concepts'])}[/dim]")

    return df