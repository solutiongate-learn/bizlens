"""
Sample Dataset Discovery and Loading
Integrates datasets from scipy, sklearn, and seaborn
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings

warnings.filterwarnings("ignore")

# ============================================================================
# DATASET REGISTRY WITH DESCRIPTIONS
# ============================================================================

DATASET_REGISTRY = {
    # SEABORN DATASETS
    "iris": {
        "source": "seaborn",
        "description": "Classic iris flower dataset with 150 samples",
        "education_level": "High School, Undergraduate Year 1",
        "concepts": ["Classification", "Multivariate analysis", "Central tendency"],
        "size": "150 rows × 5 columns",
        "features": "Sepal length/width, Petal length/width, Species"
    },

    "titanic": {
        "source": "seaborn",
        "description": "Titanic passenger data with 891 records",
        "education_level": "Undergraduate Year 1-2",
        "concepts": ["Categorical analysis", "Missing data", "Correlation"],
        "size": "891 rows × 15 columns",
        "features": "Passenger info, Survival status, Fare, Class"
    },

    "tips": {
        "source": "seaborn",
        "description": "Restaurant tips dataset with 244 observations",
        "education_level": "High School, Undergraduate Year 1",
        "concepts": ["Categorical comparison", "Correlation", "Distribution"],
        "size": "244 rows × 7 columns",
        "features": "Total bill, Tip amount, Sex, Day, Time, Party size"
    },

    "penguins": {
        "source": "seaborn",
        "description": "Palmer Penguins dataset with 344 observations",
        "education_level": "Undergraduate Year 1-2",
        "concepts": ["Species comparison", "Multivariate", "Outlier detection"],
        "size": "344 rows × 7 columns",
        "features": "Species, Island, Culmen measurements, Body mass, Sex"
    },

    "diamonds": {
        "source": "seaborn",
        "description": "Diamond prices dataset with 53,940 records",
        "education_level": "Undergraduate Year 2-3",
        "concepts": ["Correlation", "Regression", "Multivariate analysis"],
        "size": "53,940 rows × 10 columns",
        "features": "Price, Carat, Cut, Color, Clarity, Dimensions"
    },

    "flights": {
        "source": "seaborn",
        "description": "Airline passenger data (1949-1960), 144 rows",
        "education_level": "Undergraduate Year 2+",
        "concepts": ["Time series", "Trend analysis", "Seasonality"],
        "size": "144 rows × 5 columns",
        "features": "Year, Month, Passengers (time series)"
    },

    "mpg": {
        "source": "seaborn",
        "description": "Auto MPG dataset with 398 cars",
        "education_level": "Undergraduate Year 1-2",
        "concepts": ["Regression", "Categorical analysis", "Correlation"],
        "size": "398 rows × 9 columns",
        "features": "MPG, Cylinders, Displacement, Horsepower, Weight"
    },

    "planets": {
        "source": "seaborn",
        "description": "Exoplanet discovery data with 1,000+ records",
        "education_level": "Undergraduate Year 2+",
        "concepts": ["Distribution", "Outlier detection", "Multivariate"],
        "size": "1,000+ rows × 6 columns",
        "features": "Discovery method, Orbital period, Mass, Distance"
    },

    "exercise": {
        "source": "seaborn",
        "description": "Exercise physiology data with 180 observations",
        "education_level": "Undergraduate Year 1-2",
        "concepts": ["Categorical analysis", "Correlation", "Distribution"],
        "size": "180 rows × 5 columns",
        "features": "Athlete data, Pulse, Oxygen uptake, Duration, Intensity"
    },

    # SKLEARN DATASETS
    "digits": {
        "source": "sklearn",
        "description": "Handwritten digits (0-9) with 1,797 samples",
        "education_level": "Undergraduate Year 3+",
        "concepts": ["Image classification", "Multivariate", "Clustering"],
        "size": "1,797 rows × 64 columns",
        "features": "8×8 pixel images of digits"
    },

    "wine": {
        "source": "sklearn",
        "description": "Wine classification dataset with 178 samples",
        "education_level": "Undergraduate Year 1-2",
        "concepts": ["Classification", "Multivariate", "Central tendency"],
        "size": "178 rows × 13 columns",
        "features": "Wine properties, Alcohol %, Color intensity, Acidity"
    },

    "breast_cancer": {
        "source": "sklearn",
        "description": "Cancer diagnosis dataset with 569 samples",
        "education_level": "Postgraduate",
        "concepts": ["Medical classification", "Feature importance", "Binary outcomes"],
        "size": "569 rows × 30 columns",
        "features": "Cell measurements, Diagnosis (Benign/Malignant)"
    },

    # SCIPY DATASETS
    "student_t": {
        "source": "scipy_generated",
        "description": "Simulated Student's t-distribution (500 samples)",
        "education_level": "Undergraduate Year 2+",
        "concepts": ["Distribution shape", "Heavy tails", "Statistical inference"],
        "size": "500 rows × 1 column",
        "features": "Values from t-distribution with df=10"
    },

    "normal_dist": {
        "source": "scipy_generated",
        "description": "Simulated normal distribution (500 samples)",
        "education_level": "High School, Undergraduate Year 1",
        "concepts": ["Normal distribution", "Central limit theorem", "Percentiles"],
        "size": "500 rows × 1 column",
        "features": "Values from standard normal distribution"
    },

    "exponential_dist": {
        "source": "scipy_generated",
        "description": "Simulated exponential distribution (500 samples)",
        "education_level": "Undergraduate Year 2+",
        "concepts": ["Right-skewed", "Waiting times", "Poisson process"],
        "size": "500 rows × 1 column",
        "features": "Values from exponential distribution (λ=1)"
    },
}


# ============================================================================
# DATASET LOADING FUNCTIONS
# ============================================================================

def list_available_datasets() -> pd.DataFrame:
    """
    List all available sample datasets with descriptions.

    Returns:
        DataFrame with dataset information
    """
    records = []
    for name, info in DATASET_REGISTRY.items():
        records.append({
            "Dataset": name,
            "Source": info["source"],
            "Size": info["size"],
            "Education Level": info["education_level"],
            "Description": info["description"]
        })

    df = pd.DataFrame(records)
    return df.sort_values("Dataset")


def describe_dataset(name: str) -> Dict:
    """
    Get detailed description of a specific dataset.

    Args:
        name: Dataset name

    Returns:
        Dictionary with full dataset information
    """
    if name not in DATASET_REGISTRY:
        available = list(DATASET_REGISTRY.keys())
        raise ValueError(f"Dataset '{name}' not found. Available: {available}")

    return DATASET_REGISTRY[name]


def load_sample_dataset(name: str) -> pd.DataFrame:
    """
    Load a sample dataset.

    Args:
        name: Dataset name (see list_available_datasets())

    Returns:
        Loaded DataFrame

    Examples:
        df = load_sample_dataset('iris')
        df = load_sample_dataset('tips')
        df = load_sample_dataset('titanic')
    """
    if name not in DATASET_REGISTRY:
        available = list(DATASET_REGISTRY.keys())
        raise ValueError(f"Dataset '{name}' not found. Available: {available}")

    info = DATASET_REGISTRY[name]
    source = info["source"]

    try:
        if source == "seaborn":
            import seaborn as sns
            df = sns.load_dataset(name)

        elif source == "sklearn":
            from sklearn import datasets

            if name == "digits":
                data = datasets.load_digits()
            elif name == "wine":
                data = datasets.load_wine()
            elif name == "breast_cancer":
                data = datasets.load_breast_cancer()
            else:
                raise ValueError(f"Unknown sklearn dataset: {name}")

            df = pd.DataFrame(data.data, columns=data.feature_names)
            if hasattr(data, 'target'):
                df['target'] = data.target

        elif source == "scipy_generated":
            from scipy import stats as sp_stats

            np.random.seed(42)
            if name == "student_t":
                values = sp_stats.t.rvs(df=10, size=500)
            elif name == "normal_dist":
                values = np.random.normal(0, 1, 500)
            elif name == "exponential_dist":
                values = np.random.exponential(1, 500)
            else:
                raise ValueError(f"Unknown scipy dataset: {name}")

            df = pd.DataFrame({name: values})

        else:
            raise ValueError(f"Unknown source: {source}")

        print(f"✅ Loaded '{name}' ({info['size']})")
        print(f"   {info['description']}")

        return df

    except Exception as e:
        raise RuntimeError(f"Error loading dataset '{name}': {str(e)}")


def print_dataset_info(name: str):
    """
    Print detailed information about a dataset.

    Args:
        name: Dataset name
    """
    if name not in DATASET_REGISTRY:
        print("❌ Dataset not found!")
        print("\nAvailable datasets:")
        for dataset_name in sorted(DATASET_REGISTRY.keys()):
            print(f"  - {dataset_name}")
        return

    info = DATASET_REGISTRY[name]

    print(f"\n{'='*70}")
    print(f"📊 {name.upper()}")
    print(f"{'='*70}")
    print(f"Description: {info['description']}")
    print(f"Source: {info['source']}")
    print(f"Size: {info['size']}")
    print(f"Education Level: {info['education_level']}")
    print(f"\nConcepts Covered:")
    for concept in info['concepts']:
        print(f"  • {concept}")
    print(f"\nFeatures:")
    print(f"  {info['features']}")
    print(f"{'='*70}\n")


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def explore_datasets():
    """
    Interactive dataset exploration.
    Shows all available datasets and allows quick access.
    """
    df = list_available_datasets()
    print("\n" + "="*100)
    print("📚 AVAILABLE SAMPLE DATASETS")
    print("="*100 + "\n")
    print(df.to_string(index=False))
    print("\n" + "="*100)
    print("\nUsage:")
    print("  from src.bizlens.datasets import load_sample_dataset, describe_dataset")
    print("  df = load_sample_dataset('iris')")
    print("  info = describe_dataset('iris')")
    print("="*100 + "\n")


if __name__ == "__main__":
    explore_datasets()
