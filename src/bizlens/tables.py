"""
BizLens Tables Module — Educational Statistical Tables & Summaries
Version: 2.2.11
Purpose: Create professional statistical tables for data summarization and comparison
Teaching Focus: Understanding frequency distributions, percentiles, contingency tables,
                and how to communicate statistical insights clearly

Dependencies:
- pandas (data manipulation)
- numpy (numerical operations)
- scipy (statistical distributions and chi-square test)
- rich (beautiful console output)
"""

import pandas as pd
import numpy as np
from scipy import stats
from rich.table import Table as RichTable
from rich.console import Console
from typing import Union, Tuple, Optional

console = Console()


class tables:
    """
    Professional statistical tables for data exploration and communication.

    **Purpose (Educational):**
    These methods help you summarize data in tables that are clear, informative,
    and suitable for presentations or reports. Each table tells a story about
    your data and helps you answer specific questions.

    **When to use each method:**
    - frequency_table: "What are the most common values?"
    - percentile_table: "Where does this value rank?"
    - contingency_table: "How do two categorical variables relate?"
    - summary_statistics: "What are the key numbers I need?"
    - group_comparison: "Do different groups have different averages?"
    - distribution_fit: "What distribution does this data follow?"
    - descriptive_comparison: "How do two datasets compare?"
    """

    @staticmethod
    def frequency_table(series: pd.Series, top_n: int = 10) -> RichTable:
        """
        Create a frequency distribution table showing value counts.

        **What this does (Educational):**
        Shows the count, percentage, and cumulative percentage of each unique value.
        This helps you understand the distribution of a categorical variable and
        identify the most common categories.

        **Parameters:**
        -----------
        series : pd.Series
            The data column to analyze (categorical or numerical)
        top_n : int, default=10
            Number of top values to display

        **Returns:**
        --------
        rich.table.Table
            A formatted table with counts and percentages

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> data = pd.Series(['A', 'B', 'A', 'C', 'B', 'A'])
        >>> bl.tables.frequency_table(data)

        **Educational Notes:**
        - The sum of all counts equals the total number of observations
        - Percentages show what proportion each category represents
        - Cumulative % shows what % of data falls up to that value (ordered by frequency)
        - Useful for identifying dominant categories and data imbalance
        """
        # Remove missing values (NaN) - consistent with pandas describe()
        data = series.dropna()

        # Count occurrences of each value and sort by frequency
        # LEARNING POINT: value_counts() returns sorted counts by default
        value_counts = data.value_counts()

        # Limit to top N values to keep table readable
        value_counts = value_counts.head(top_n)

        # Calculate percentages and cumulative percentages
        # LEARNING POINT: Percentage = (count / total) * 100
        total = len(data)
        percentages = (value_counts / total * 100).round(2)
        cumulative_pct = (value_counts.cumsum() / total * 100).round(2)

        # Create rich table for beautiful console output
        table = RichTable(title=f"Frequency Table — {series.name or 'Series'}",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Value", style="cyan")
        table.add_column("Count", justify="right", style="magenta")
        table.add_column("Percentage", justify="right", style="green")
        table.add_column("Cumulative %", justify="right", style="yellow")

        # Add rows to table
        for value, count in value_counts.items():
            table.add_row(
                str(value),
                str(count),
                f"{percentages[value]:.2f}%",
                f"{cumulative_pct[value]:.2f}%"
            )

        # Add summary row
        if len(value_counts) > top_n:
            other_count = len(data) - value_counts.sum()
            table.add_row(
                f"[Other ({len(data.unique()) - top_n} categories)]",
                str(other_count),
                f"{(other_count / total * 100):.2f}%",
                "100.00%"
            )

        return table

    @staticmethod
    def percentile_table(series: pd.Series) -> RichTable:
        """
        Create a percentile breakdown table (quartiles and beyond).

        **What this does (Educational):**
        Shows where values fall in the distribution using percentiles (0, 25, 50, 75, 100).
        A percentile tells you: "This value is higher than X% of the data."
        For example, the 75th percentile is higher than 75% of the values.

        **Parameters:**
        -----------
        series : pd.Series
            Numerical column to analyze

        **Returns:**
        --------
        rich.table.Table
            Quartile breakdown with statistical interpretation

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        >>> bl.tables.percentile_table(data)

        **Educational Notes:**
        - 0th percentile = minimum value
        - 25th percentile (Q1) = lower quartile
        - 50th percentile (Q2/Median) = middle value
        - 75th percentile (Q3) = upper quartile
        - 100th percentile = maximum value
        - IQR (Interquartile Range) = Q3 - Q1 = where middle 50% of data lives
        """
        # Remove missing values
        data = series.dropna()

        # LEARNING POINT: numpy.percentile calculates the value at a given percentile
        # Different methods exist (linear, lower, higher, midpoint, nearest)
        percentiles = [0, 25, 50, 75, 100]
        percentile_values = np.percentile(data, percentiles)

        # Calculate IQR (Interquartile Range)
        # LEARNING POINT: IQR is robust to outliers and shows data spread
        q1 = percentile_values[1]
        q3 = percentile_values[3]
        iqr = q3 - q1

        # Create table
        table = RichTable(title=f"Percentile Table — {series.name or 'Series'}",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Percentile", style="cyan")
        table.add_column("Value", justify="right", style="magenta")
        table.add_column("Interpretation", style="green")

        interpretations = [
            "Minimum value (lowest)",
            "First Quartile (Q1) — 25% of data below this",
            "Median — 50% above, 50% below",
            "Third Quartile (Q3) — 75% of data below this",
            "Maximum value (highest)"
        ]

        for pct, value, interp in zip(percentiles, percentile_values, interpretations):
            table.add_row(
                f"{pct}th" if pct != 50 else "50th (Median)",
                f"{value:.4f}".rstrip('0').rstrip('.'),
                interp
            )

        # Add IQR information
        table.add_row("", "", "")
        table.add_row(
            "[bold]IQR[/bold]",
            f"{iqr:.4f}".rstrip('0').rstrip('.'),
            "Q3 - Q1 = middle 50% spread"
        )

        return table

    @staticmethod
    def contingency_table(df: pd.DataFrame, row_col: str, col_col: str) -> Tuple[RichTable, dict]:
        """
        Create a contingency (crosstab) table showing relationships between two categorical variables.

        **What this does (Educational):**
        Shows how two categorical variables are related using a cross-tabulation.
        Includes marginal totals and chi-square test for independence.

        **Parameters:**
        -----------
        df : pd.DataFrame
            Input dataframe
        row_col : str
            Column name for table rows
        col_col : str
            Column name for table columns

        **Returns:**
        --------
        Tuple[RichTable, dict]
            - Table: Formatted contingency table with margins
            - dict: Chi-square test results {chi2, p_value, dof, interpretation}

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> df = pd.DataFrame({
        ...     'gender': ['M', 'F', 'M', 'F'],
        ...     'purchase': ['Yes', 'No', 'Yes', 'Yes']
        ... })
        >>> table, stats = bl.tables.contingency_table(df, 'gender', 'purchase')

        **Educational Notes:**
        - Contingency table shows joint distribution of two variables
        - Marginal totals show distribution of each variable alone
        - Chi-square test checks if variables are independent
        - p-value < 0.05 suggests variables are related (not independent)
        - Cramér's V measures strength of association (0=none, 1=perfect)
        """
        # Create pivot table (crosstab)
        # LEARNING POINT: pd.crosstab creates joint frequency distribution
        crosstab = pd.crosstab(df[row_col], df[col_col], margins=True)

        # Perform chi-square test for independence
        # LEARNING POINT: Chi-square tests if two categorical variables are independent
        chi2, p_value, dof, expected = stats.chi2_contingency(
            pd.crosstab(df[row_col], df[col_col])
        )

        # Calculate Cramér's V (effect size for contingency)
        # LEARNING POINT: Cramér's V ranges 0-1, shows strength of association
        n = len(df)
        min_dim = min(len(df[row_col].unique()), len(df[col_col].unique())) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0

        # Create rich table
        table = RichTable(title=f"Contingency Table — {row_col} × {col_col}",
                         show_header=True,
                         header_style="bold blue")
        table.add_column(row_col, style="cyan")

        # Add column headers
        for col in crosstab.columns:
            table.add_column(str(col), justify="right")

        # Add rows
        for idx, row in crosstab.iterrows():
            table.add_row(str(idx), *[str(int(val)) for val in row])

        # Prepare chi-square results
        chi_results = {
            'chi2': chi2,
            'p_value': p_value,
            'dof': dof,
            'cramers_v': cramers_v,
            'independent': p_value > 0.05,
            'interpretation': (
                f"Variables are {'independent' if p_value > 0.05 else 'associated'} "
                f"(p={p_value:.4f}, Cramér's V={cramers_v:.3f})"
            )
        }

        return table, chi_results

    @staticmethod
    def summary_statistics(df: pd.DataFrame) -> RichTable:
        """
        Create a comprehensive summary statistics table (better than pandas.describe()).

        **What this does (Educational):**
        Shows count, mean, std, min, quartiles, max, and null count for all numeric columns.
        This gives you a complete picture of your data at a glance.

        **Parameters:**
        -----------
        df : pd.DataFrame
            Input dataframe

        **Returns:**
        --------
        RichTable
            Formatted summary statistics table

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> df = pd.DataFrame({'a': [1, 2, 3, 4, 5]})
        >>> bl.tables.summary_statistics(df)

        **Educational Notes:**
        - Count: How many non-null values (N)
        - Mean: Average value
        - Std: Standard deviation (spread of data)
        - Min: Smallest value
        - 25%, 50%, 75%: Quartiles (distribution position)
        - Max: Largest value
        - Null: How many missing values (data quality)
        """
        # Get numeric columns
        numeric_df = df.select_dtypes(include=[np.number])

        # Calculate summary statistics
        summary = numeric_df.describe(include='all').T

        # Add null count
        summary['null_count'] = df[numeric_df.columns].isnull().sum()
        summary['null_pct'] = (summary['null_count'] / len(df) * 100).round(2)

        # Create table
        table = RichTable(title="Summary Statistics",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Count", justify="right")
        table.add_column("Mean", justify="right", style="green")
        table.add_column("Std", justify="right")
        table.add_column("Min", justify="right")
        table.add_column("25%", justify="right")
        table.add_column("50%", justify="right")
        table.add_column("75%", justify="right")
        table.add_column("Max", justify="right")
        table.add_column("Null", justify="right", style="red")

        for col in summary.index:
            table.add_row(
                col,
                str(int(summary.loc[col, 'count'])),
                f"{summary.loc[col, 'mean']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, 'std']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, 'min']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, '25%']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, '50%']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, '75%']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, 'max']:.4f}".rstrip('0').rstrip('.'),
                f"{int(summary.loc[col, 'null_count'])} ({summary.loc[col, 'null_pct']:.1f}%)"
            )

        return table

    @staticmethod
    def group_comparison(df: pd.DataFrame, group_col: str, numeric_cols: list = None) -> Tuple[RichTable, dict]:
        """
        Compare statistics across groups with ANOVA test.

        **What this does (Educational):**
        Shows mean and std for numeric columns broken down by groups.
        Tests whether the groups have significantly different means using ANOVA.

        **Parameters:**
        -----------
        df : pd.DataFrame
            Input dataframe
        group_col : str
            Column defining groups
        numeric_cols : list, optional
            Numeric columns to compare. If None, analyzes all numeric columns.

        **Returns:**
        --------
        Tuple[RichTable, dict]
            - Table: Group comparison with means and stds
            - dict: ANOVA results {f_stat, p_value, interpretation}

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> df = pd.DataFrame({
        ...     'group': ['A', 'A', 'B', 'B'],
        ...     'value': [1, 2, 3, 4]
        ... })
        >>> table, stats = bl.tables.group_comparison(df, 'group', ['value'])

        **Educational Notes:**
        - Compares means across groups
        - ANOVA tests: "Are group means significantly different?"
        - p-value < 0.05 suggests groups differ significantly
        """
        if numeric_cols is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Create comparison table
        table = RichTable(title=f"Group Comparison — {group_col}",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Column", style="cyan")

        # Add column for each group
        groups = sorted(df[group_col].unique())
        for group in groups:
            table.add_column(f"{group} (Mean ± Std)", justify="right")

        # Add rows
        anova_results = {}
        for col in numeric_cols:
            table.add_row(col, end_section=False)

            # Calculate ANOVA
            # LEARNING POINT: ANOVA tests if means differ across groups
            group_data = [df[df[group_col] == g][col].dropna().values for g in groups]
            f_stat, p_value = stats.f_oneway(*group_data)

            anova_results[col] = {
                'f_stat': f_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }

            # Get data for each group
            row_data = [col]
            for group in groups:
                group_vals = df[df[group_col] == group][col].dropna()
                mean = group_vals.mean()
                std = group_vals.std()
                row_data.append(f"{mean:.2f} ± {std:.2f}")

            table.add_row(*row_data)

        return table, anova_results

    @staticmethod
    def distribution_fit(series: pd.Series) -> Tuple[RichTable, dict]:
        """
        Test which distribution fits the data best.

        **What this does (Educational):**
        Tests common distributions (normal, exponential, poisson) and returns
        which one fits your data best. Useful for choosing appropriate statistical tests.

        **Parameters:**
        -----------
        series : pd.Series
            Numeric data to analyze

        **Returns:**
        --------
        Tuple[RichTable, dict]
            - Table: Goodness-of-fit results
            - dict: Best fit distribution with parameters

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> data = pd.Series(np.random.normal(0, 1, 1000))
        >>> table, result = bl.tables.distribution_fit(data)

        **Educational Notes:**
        - Different distributions suit different data types
        - Normal: Many natural phenomena
        - Exponential: Waiting times
        - Poisson: Count data (events in time)
        """
        data = series.dropna()

        # Test different distributions
        # LEARNING POINT: Kolmogorov-Smirnov test compares data to theoretical distribution
        distributions_to_test = {
            'Normal': stats.norm,
            'Exponential': stats.expon,
            'Lognormal': stats.lognorm,
        }

        results = {}
        for dist_name, dist in distributions_to_test.items():
            try:
                params = dist.fit(data)
                ks_stat, p_value = stats.kstest(data, lambda x: dist.cdf(x, *params))
                results[dist_name] = {
                    'ks_stat': ks_stat,
                    'p_value': p_value,
                    'params': params
                }
            except:
                results[dist_name] = {'ks_stat': np.nan, 'p_value': 0}

        # Create table
        table = RichTable(title="Distribution Fit Test",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Distribution", style="cyan")
        table.add_column("KS Statistic", justify="right")
        table.add_column("P-value", justify="right")
        table.add_column("Fit", style="green")

        best_dist = min(results.items(), key=lambda x: x[1]['ks_stat'])

        for dist_name, result in results.items():
            fit_qual = "✓ Best Fit" if dist_name == best_dist[0] else ""
            table.add_row(
                dist_name,
                f"{result['ks_stat']:.4f}",
                f"{result['p_value']:.4f}",
                fit_qual
            )

        return table, {'best_fit': best_dist[0], 'results': results}

    @staticmethod
    def descriptive_comparison(df1: pd.DataFrame, df2: pd.DataFrame,
                               label1: str = "Data 1", label2: str = "Data 2") -> RichTable:
        """
        Compare descriptive statistics between two datasets.

        **What this does (Educational):**
        Compares means, stds, and counts between two datasets side-by-side.
        Useful for sample vs population or before/after comparisons.

        **Parameters:**
        -----------
        df1, df2 : pd.DataFrame
            Datasets to compare
        label1, label2 : str
            Labels for each dataset

        **Returns:**
        --------
        RichTable
            Side-by-side comparison of statistics

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> sample = pd.DataFrame({'value': [1, 2, 3]})
        >>> population = pd.DataFrame({'value': [1, 2, 3, 4, 5]})
        >>> bl.tables.descriptive_comparison(sample, population, "Sample", "Population")

        **Educational Notes:**
        - Useful for sample vs population comparison
        - Shows if sample statistics represent the population well
        - Larger sample size generally gives more reliable estimates
        """
        # Get numeric columns
        numeric_cols = df1.select_dtypes(include=[np.number]).columns

        # Create comparison table
        table = RichTable(title=f"{label1} vs {label2} Comparison",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Metric", style="cyan")
        table.add_column(label1, justify="right", style="magenta")
        table.add_column(label2, justify="right", style="green")
        table.add_column("Difference", justify="right", style="yellow")

        for col in numeric_cols:
            d1 = df1[col].dropna()
            d2 = df2[col].dropna()

            # Compare means
            mean1 = d1.mean()
            mean2 = d2.mean()
            table.add_row(
                f"{col} (mean)",
                f"{mean1:.4f}".rstrip('0').rstrip('.'),
                f"{mean2:.4f}".rstrip('0').rstrip('.'),
                f"{(mean1 - mean2):.4f}".rstrip('0').rstrip('.')
            )

            # Compare stds
            std1 = d1.std()
            std2 = d2.std()
            table.add_row(
                f"{col} (std)",
                f"{std1:.4f}".rstrip('0').rstrip('.'),
                f"{std2:.4f}".rstrip('0').rstrip('.'),
                f"{(std1 - std2):.4f}".rstrip('0').rstrip('.')
            )

            # Compare counts
            table.add_row(
                f"{col} (N)",
                str(len(d1)),
                str(len(d2)),
                str(len(d1) - len(d2))
            )

            table.add_row("", "", "", "")  # Spacing

        return table
