# BizLens Dataset Generation Guide 📊
## Creating Copyright-Safe, Pedagogically-Aligned Datasets

---

## Philosophy

All datasets should follow:
1. **Pedagogically Intentional** — Illustrate specific concepts
2. **Realistic but Synthetic** — Real-world distributions without privacy concerns
3. **Copyright-Free** — No data sourced from copyrighted materials
4. **Reproducible** — Seeded randomness for consistent examples
5. **Well-Documented** — Clear provenance and usage

---

## Architecture: `src/bizlens/datasets/`

```
src/bizlens/datasets/
├── __init__.py
├── loader.py                    # Main API: load_dataset()
├── generators/
│   ├── distributions.py         # Normal, exponential, etc.
│   ├── business.py             # Business datasets
│   ├── academic.py             # Academic/student datasets
│   ├── healthcare.py           # Health/clinical datasets
│   └── social.py               # Social/demographic datasets
└── metadata/
    ├── school_cafeteria.json   # Dataset info + textbook links
    ├── student_gpa.json
    └── ...
```

---

## API Design

### Simple Usage
```python
import bizlens as bl

# Load high school dataset
df = bl.load_dataset('school_cafeteria')

# Load with parameters
df = bl.load_dataset('student_gpa', n_students=1000, seed=42)

# List available datasets
bl.list_datasets()

# Get dataset info
bl.dataset_info('student_gpa')
```

### Metadata Structure
```json
{
  "name": "student_gpa",
  "description": "GPA data from 500 students across 5 majors",
  "size": 500,
  "education_level": ["undergraduate", "master's"],
  "concepts": ["multivariate analysis", "distribution comparison", "hypothesis testing"],
  "textbooks": [
    {
      "title": "An Introduction to Statistical Learning",
      "chapter": 3,
      "section": "Linear Regression"
    }
  ],
  "columns": {
    "student_id": "Unique identifier",
    "major": "Categorical: STEM, Business, Liberal Arts, etc.",
    "gpa": "Continuous: 0-4.0 scale",
    "study_hours": "Continuous: hours per week",
    "gender": "Categorical: M/F"
  },
  "license": "CC0",
  "generation_method": "Synthetic from real aggregate statistics",
  "real_world_inspiration": "Based on IPEDS data 2023"
}
```

---

## Phase 1: v0.6.0 Dataset Implementation

### Dataset 1: school_cafeteria

**Purpose**: Teach descriptive statistics and categorical analysis at high school level

**Generation Code** (`datasets/generators/business.py`):
```python
import numpy as np
import polars as pl
from typing import Optional

def generate_school_cafeteria(n_students: int = 200, seed: int = 42) -> pl.DataFrame:
    """
    Generate realistic school cafeteria data.

    Concepts taught:
    - Descriptive statistics (mean spending)
    - Categorical analysis (lunch type preferences)
    - Correlation (satisfaction vs. spending)
    - Skewness (most students spend little, few spend lots)
    """
    np.random.seed(seed)

    # Base data
    student_ids = np.arange(1, n_students + 1)

    # Lunch type: categorical with realistic proportions
    lunch_types = np.random.choice(
        ["hot_meal", "packed_lunch", "salad", "pizza", "other"],
        size=n_students,
        p=[0.35, 0.25, 0.20, 0.15, 0.05]
    )

    # Spending: skewed (exponential distribution, not normal!)
    # Most students spend $5-10, few spend $15+
    spending = np.random.exponential(scale=4.5, size=n_students).round(2)
    spending = np.minimum(spending, 25)  # Cap at $25

    # Satisfaction: depends on lunch type
    satisfaction = np.zeros(n_students)
    for i, lunch_type in enumerate(lunch_types):
        # Hot meal: higher satisfaction
        if lunch_type == "hot_meal":
            satisfaction[i] = np.random.normal(7.5, 1.5, 1)[0]
        # Packed lunch: medium satisfaction
        elif lunch_type == "packed_lunch":
            satisfaction[i] = np.random.normal(6.5, 1.5, 1)[0]
        # Pizza: high satisfaction
        elif lunch_type == "pizza":
            satisfaction[i] = np.random.normal(8.0, 1.2, 1)[0]
        else:
            satisfaction[i] = np.random.normal(6.0, 2.0, 1)[0]

    satisfaction = np.clip(satisfaction, 1, 10).round(1)

    # Age (high school: 14-18)
    age = np.random.choice(
        [14, 15, 16, 17, 18],
        size=n_students,
        p=[0.20, 0.25, 0.25, 0.20, 0.10]
    )

    # Create DataFrame
    df = pl.DataFrame({
        "student_id": student_ids,
        "age": age,
        "lunch_type": lunch_types,
        "spending": spending,
        "satisfaction": satisfaction,
    })

    return df

# Metadata
SCHOOL_CAFETERIA_META = {
    "name": "school_cafeteria",
    "description": "High school student lunch spending and satisfaction",
    "size": 200,
    "education_level": ["high_school", "undergraduate"],
    "concepts": [
        "descriptive statistics",
        "categorical analysis",
        "skewness",
        "correlation"
    ],
    "textbooks": [
        {
            "title": "The Basic Practice of Statistics",
            "authors": "Moore & Notz",
            "chapter": 2,
            "concepts": ["Describing Distributions", "Describing Relationships"]
        }
    ],
    "columns": {
        "student_id": "Unique student identifier (1-200)",
        "age": "Student age (14-18)",
        "lunch_type": "Type of lunch: hot_meal, packed_lunch, salad, pizza, other",
        "spending": "Daily spending in dollars (0-25)",
        "satisfaction": "Satisfaction rating (1-10)"
    },
    "teaching_notes": [
        "Spending is skewed (exponential) - great for teaching non-normality",
        "Satisfaction varies by lunch type - shows categorical relationships",
        "Correlation between spending and satisfaction is not 1.0 - teaches imperfect correlation"
    ]
}
```

**Textbook Alignment**:
- **AP Statistics**: Chapter 2 (Distributions of Sample Data)
- **Moore & Notz**: Chapter 2 (Describing Distributions)
- **Concept**: "Why is average spending misleading? (Median is better for skewed data)"

---

### Dataset 2: test_scores

**Purpose**: Teach distribution analysis and normality testing

**Generation Code**:
```python
def generate_test_scores(n_students: int = 100, seed: int = 42) -> pl.DataFrame:
    """
    Generate test scores across subjects.

    Concepts taught:
    - Different distributions (normal, bimodal)
    - Mean vs. median
    - Standard deviation
    - Outliers
    - Group comparisons
    """
    np.random.seed(seed)

    student_ids = np.arange(1, n_students + 1)

    # Subject performance varies by student "ability"
    # Hidden latent ability: roughly normal
    ability = np.random.normal(loc=70, scale=15, size=n_students)

    # Math scores: mostly normal, some very high performers
    math_scores = ability + np.random.normal(0, 8, n_students)
    math_scores = np.clip(math_scores, 0, 100).round(1)

    # English scores: bimodal (some very good, some struggling)
    english_scores = np.concatenate([
        np.random.normal(65, 10, int(0.6 * n_students)),  # Majority
        np.random.normal(85, 8, int(0.4 * n_students))    # Top performers
    ])
    english_scores = english_scores[:n_students]
    english_scores = np.clip(english_scores, 0, 100).round(1)

    # Science: normal distribution
    science_scores = ability + np.random.normal(0, 10, n_students)
    science_scores = np.clip(science_scores, 0, 100).round(1)

    # Subjects
    subjects = np.tile(
        ["Math", "English", "Science"],
        (n_students // 3 + 1, 1)
    ).flatten()[:n_students]

    # Create long format
    all_data = []
    for i in range(n_students):
        all_data.append({"student_id": i+1, "subject": "Math", "score": math_scores[i]})
        all_data.append({"student_id": i+1, "subject": "English", "score": english_scores[i]})
        all_data.append({"student_id": i+1, "subject": "Science", "score": science_scores[i]})

    df = pl.DataFrame(all_data)
    return df

TEST_SCORES_META = {
    "name": "test_scores",
    "description": "Student test scores in Math, English, Science",
    "size": 300,  # 100 students × 3 subjects
    "education_level": ["high_school"],
    "concepts": [
        "distribution shape",
        "normality testing",
        "group comparison",
        "bimodal distribution"
    ],
    "textbooks": [
        {
            "title": "AP Statistics",
            "chapter": 2,
            "concepts": ["Quantitative Data Distributions"]
        },
        {
            "title": "OpenIntro Statistics",
            "chapter": 4,
            "concepts": ["Distributions of Random Variables"]
        }
    ],
    "teaching_notes": [
        "Math: approximately normal distribution",
        "English: bimodal (two peaks) - shows non-normal but unimodal isn't universal",
        "Science: slightly skewed - more realistic than pure normal"
    ]
}
```

---

## Phase 2: v0.7.0 New Datasets

### Pattern: Add 4 datasets per phase

```
v0.7.0 additions:
├── student_gpa (500 students)        — Multivariate regression
├── housing_market (1000 properties)  — Feature interaction
├── ice_cream_sales (30 weeks)        — Spurious correlation
└── nobel_chocolate (30 countries)    — Correlation interpretation
```

---

## Implementation in core.py

### Add to `src/bizlens/__init__.py`

```python
from .datasets import load_dataset, list_datasets, dataset_info

__all__ = [
    "describe",
    "BizDesc",
    "create_interactive_demo",
    "load_dataset",           # NEW
    "list_datasets",          # NEW
    "dataset_info",           # NEW
]
```

### Create `src/bizlens/datasets/loader.py`

```python
import polars as pl
from typing import Optional, Dict, List
from pathlib import Path
import json

# Import generators
from .generators import (
    generate_school_cafeteria,
    generate_test_scores,
    generate_student_gpa,
    # ... more as added
)

# Metadata registry
DATASETS = {
    "school_cafeteria": {
        "generator": generate_school_cafeteria,
        "meta": SCHOOL_CAFETERIA_META,
    },
    "test_scores": {
        "generator": generate_test_scores,
        "meta": TEST_SCORES_META,
    },
    # ... more as added
}

def load_dataset(
    name: str,
    n_samples: Optional[int] = None,
    seed: int = 42
) -> pl.DataFrame:
    """
    Load an educational dataset.

    Args:
        name: Dataset name (e.g., 'school_cafeteria')
        n_samples: Override default size (if supported)
        seed: Random seed for reproducibility

    Returns:
        Polars DataFrame with educational data

    Example:
        >>> df = bl.load_dataset('student_gpa')
        >>> bl.describe(df)
    """
    if name not in DATASETS:
        available = ", ".join(DATASETS.keys())
        raise ValueError(f"Unknown dataset '{name}'. Available: {available}")

    generator = DATASETS[name]["generator"]

    # Call generator with appropriate parameters
    if n_samples:
        df = generator(n_samples=n_samples, seed=seed)
    else:
        df = generator(seed=seed)

    return df

def list_datasets() -> List[str]:
    """List available educational datasets."""
    return list(DATASETS.keys())

def dataset_info(name: str) -> Dict:
    """Get detailed info about a dataset."""
    if name not in DATASETS:
        raise ValueError(f"Unknown dataset: {name}")

    return DATASETS[name]["meta"]
```

---

## Quality Assurance for Datasets

### For each dataset, verify:

```python
# test_datasets.py

def test_school_cafeteria():
    """Validate school_cafeteria dataset."""
    df = bl.load_dataset('school_cafeteria')

    # Check structure
    assert df.shape[0] == 200
    assert set(df.columns) == {"student_id", "age", "lunch_type", "spending", "satisfaction"}

    # Check data types
    assert df['age'].dtype == pl.Int64
    assert df['spending'].dtype == pl.Float64

    # Check ranges
    assert df['age'].min() >= 14 and df['age'].max() <= 18
    assert df['spending'].min() >= 0 and df['spending'].max() <= 25
    assert df['satisfaction'].min() >= 1 and df['satisfaction'].max() <= 10

    # Check distribution properties
    # Spending should be skewed (positive skewness)
    from scipy.stats import skew
    spending_skewness = skew(df['spending'].to_numpy())
    assert spending_skewness > 0.5, "Spending should be right-skewed"

    # Satisfaction should vary by lunch type
    pizza_satisfaction = df.filter(df['lunch_type'] == 'pizza')['satisfaction'].mean()
    other_satisfaction = df.filter(df['lunch_type'] == 'other')['satisfaction'].mean()
    assert pizza_satisfaction > other_satisfaction, "Pizza satisfaction should be highest"

def test_reproducibility():
    """Datasets with same seed should be identical."""
    df1 = bl.load_dataset('school_cafeteria', seed=42)
    df2 = bl.load_dataset('school_cafeteria', seed=42)

    assert df1.equals(df2)

def test_copyright_compliance():
    """Verify no copyrighted data in datasets."""
    for dataset_name in bl.list_datasets():
        meta = bl.dataset_info(dataset_name)

        # Check license
        assert 'license' in meta
        assert meta['license'] in ['CC0', 'CC-BY', 'public domain']

        # Check provenance
        assert 'generation_method' in meta
        assert 'synthetic' in meta['generation_method'].lower()
```

---

## Documentation Template for Each Dataset

Create a `docs/datasets/{dataset_name}.md` for each:

```markdown
# Dataset: school_cafeteria

## Overview
High school student lunch spending and satisfaction data.

**Size**: 200 students
**Education Level**: High School, Intro Statistics
**Primary Concept**: Descriptive Statistics, Distributions

## Columns
- `student_id`: 1-200
- `age`: 14-18
- `lunch_type`: "hot_meal", "packed_lunch", "salad", "pizza", "other"
- `spending`: $0-25 per day
- `satisfaction`: 1-10 scale

## Key Characteristics
- **Spending is skewed**: Most students spend $5-10, few spend $15+
  - Teaching point: Mean (5.3) vs Median (4.8) differ
  - Shows why median is better for skewed data

- **Satisfaction varies by lunch type**
  - Pizza: highest average satisfaction (8.0)
  - Hot meals: moderate satisfaction (7.5)
  - Packed lunch: lowest satisfaction (6.5)
  - Teaching point: Categorical relationships

## Textbook References
- **AP Statistics** — Ch. 2: "Distributions of Sample Data"
- **Moore & Notz** — Ch. 2: "Describing Distributions"

## Student Exercises

### Exercise 1: Explore Distribution
```python
import bizlens as bl

df = bl.load_dataset('school_cafeteria')
bl.describe(df['spending'], plots=True)

# Questions:
# 1. Is spending normally distributed?
# 2. Why is the distribution skewed?
# 3. Is mean or median more representative?
```

### Exercise 2: Categorical Analysis
```python
# Compare spending by lunch type
df.groupby('lunch_type')['spending'].mean()

# Questions:
# 1. Which lunch type has highest spending?
# 2. Why might hot meals cost more?
# 3. Is this a causal relationship?
```

### Exercise 3: Relationship Analysis
```python
# Does satisfaction correlate with spending?
df.select([pl.col('spending'), pl.col('satisfaction')]).pearson_correlation()

# Questions:
# 1. What's the correlation coefficient?
# 2. Does more spending → higher satisfaction?
# 3. What's the correlation for each lunch type?
```

## License
CC0 (Public Domain) — Synthetic data, free to use

## Citation
Recommended citation:
```
Singh, S. (2026). School Cafeteria Dataset. BizLens Educational Analytics Library.
https://github.com/yourusername/bizlens
```
```

---

## Dataset Release Schedule

| Phase | Datasets Added | Release Date | Education Level |
|-------|----------------|--------------|-----------------|
| v0.6.0 | school_cafeteria, test_scores | Week 4 | High School |
| v0.7.0 | student_gpa, housing_market, ice_cream_sales, nobel_chocolate | Week 8 | Undergrad Y1 |
| v0.8.0 | ecommerce, student_health, survey_bias, restaurant_reviews | Week 12 | Undergrad Y3+ |
| v0.9.0 | ab_test, stock_prices, clinical_trial, education_intervention | Week 16 | Master's |
| v1.0 | hierarchical, network, spatial + 10 more | Week 20 | PhD |

---

## Copyright Compliance Matrix

| Dataset | Source Type | License | Verification |
|---------|-----------|---------|--------------|
| school_cafeteria | Synthetic | CC0 | ✅ Generated from scratch |
| test_scores | Synthetic | CC0 | ✅ Generated from scratch |
| student_gpa | Based on IPEDS aggregate stats | CC-BY | ✅ Public domain stats only |
| housing_market | Based on Zillow aggregate patterns | CC-BY | ✅ Synthetic matching real patterns |
| ice_cream_sales | Based on published correlation (Tyler Vigen) | CC-BY | ✅ Inspired by, not copied from |
| nobel_chocolate | Same source as ice_cream | CC-BY | ✅ Inspired by, not copied from |

---

## Technical Checklist for Each New Dataset

- [ ] Unique generation function with docstring
- [ ] Metadata JSON with complete info
- [ ] 5+ unit tests verifying properties
- [ ] Copyright compliance verified
- [ ] Teaching notes with concepts
- [ ] Example student exercise
- [ ] Documentation page
- [ ] Aligned with ≥2 textbooks
- [ ] Realistic but not real data
- [ ] Reproducible with seed

---

*Last updated: March 31, 2026*
*Next: Create Phase 1 datasets (Week 1-2)*
