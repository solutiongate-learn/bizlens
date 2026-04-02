"""
BizLens Diagnostic Module — Data Quality & Statistical Diagnostics
Version: 2.2.11
Purpose: Assess data quality, identify anomalies, and diagnose data issues
Teaching Focus: Understanding outliers, normality, correlation, data integrity

Dependencies:
- pandas, numpy (data manipulation)
- scipy.stats (statistical tests)
- scikit-learn (outlier detection algorithms)
- seaborn, matplotlib (visualizations)
- rich (console output)
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from rich.table import Table as RichTable
from rich.console import Console
from typing import Union, Tuple, List, Dict

console = Console()


class diagnostic:
    """
    Data quality checks and diagnostic analytics.

    **Purpose (Educational):**
    Diagnostic analytics answer: "Is there something unusual about my data?"
    These methods help you identify:
    - Outliers (extreme values that don't fit the pattern)
    - Distribution issues (data isn't normally distributed)
    - Correlations (which variables are related)
    - Missing data patterns (are missing values random?)
    - Data type inconsistencies (is everything the right type?)

    **Key Principle:**
    Before doing any analysis, always diagnose your data quality first.
    Poor data quality leads to misleading conclusions.
    """

    @staticmethod
    def detect_outliers(series: pd.Series, method: str = 'iqr',
                       contamination: float = 0.1) -> Tuple[List[int], RichTable]:
        """
        Detect outliers using IQR, Z-score, or Isolation Forest.

        **What this does (Educational):**
        Outliers are extreme values that don't follow the pattern of the rest
        of the data. They can be legitimate unusual observations or data errors.
        This method identifies them using three statistical techniques.

        **Parameters:**
        -----------
        series : pd.Series
            Data to analyze
        method : str, default='iqr'
            Detection method: 'iqr' (robust), 'zscore' (parametric), 'isolation' (ML)
        contamination : float, default=0.1
            Expected proportion of outliers (for isolation forest)

        **Returns:**
        --------
        Tuple[List[int], RichTable]
            - Indices of outlier rows
            - Formatted table with outlier analysis

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> data = pd.Series([1, 2, 3, 4, 5, 100])  # 100 is outlier
        >>> indices, table = bl.diagnostic.detect_outliers(data)

        **Educational Notes:**
        - **IQR Method (Robust):**
          Outliers = values < Q1 - 1.5*IQR or > Q3 + 1.5*IQR
          Good for: Any distribution, resistant to extreme outliers

        - **Z-Score Method (Parametric):**
          Outliers = values > 3 standard deviations from mean
          Good for: Normal distributions, assumes mean/std are meaningful

        - **Isolation Forest (ML):**
          Uses decision trees to isolate anomalies
          Good for: Multivariate outliers, complex patterns
        """
        data = series.dropna()

        if method == 'iqr':
            # LEARNING POINT: IQR method is "robust" - not affected by extreme values
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outlier_mask = (data < lower_bound) | (data > upper_bound)

        elif method == 'zscore':
            # LEARNING POINT: Z-score = (value - mean) / std
            # Tells us how many standard deviations from the mean
            z_scores = np.abs(stats.zscore(data))
            outlier_mask = z_scores > 3

        elif method == 'isolation':
            # LEARNING POINT: Isolation Forest uses tree-based anomaly detection
            # Faster than classical methods for high dimensions
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(data.values.reshape(-1, 1))
            iso_forest = IsolationForest(contamination=contamination, random_state=42)
            predictions = iso_forest.fit_predict(data_scaled)
            outlier_mask = predictions == -1
        else:
            raise ValueError(f"Unknown method: {method}")

        # Get outlier indices and values
        outlier_indices = data[outlier_mask].index.tolist()
        outlier_values = data[outlier_mask].values
        outlier_scores = np.abs(stats.zscore(data[outlier_mask]))

        # Create table
        table = RichTable(title=f"Outlier Detection ({method.upper()})",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Index", style="cyan")
        table.add_column("Value", justify="right", style="red")
        table.add_column("Z-Score", justify="right", style="yellow")
        table.add_column("Severity", style="magenta")

        for idx, value, zscore in zip(outlier_indices[:20], outlier_values[:20], outlier_scores[:20]):
            severity = "⚠️ Critical" if zscore > 5 else "⚠️ High" if zscore > 3 else "⚠️ Medium"
            table.add_row(
                str(idx),
                f"{value:.4f}".rstrip('0').rstrip('.'),
                f"{zscore:.2f}",
                severity
            )

        if len(outlier_values) > 20:
            table.add_row("[...]", f"({len(outlier_values) - 20} more outliers)", "", "")

        console.print(f"\n[bold cyan]Found {len(outlier_indices)} outliers ({len(outlier_indices)/len(data)*100:.1f}%)[/bold cyan]")

        return outlier_indices, table

    @staticmethod
    def normality_test(series: pd.Series) -> Dict[str, Union[float, str, bool]]:
        """
        Test if data follows a normal (Gaussian) distribution.

        **What this does (Educational):**
        Many statistical tests (t-test, ANOVA, linear regression) assume
        data is normally distributed. This method tests that assumption using
        three complementary tests.

        **Parameters:**
        -----------
        series : pd.Series
            Data to test

        **Returns:**
        --------
        dict
            Test results with p-values and interpretations

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> data = pd.Series(np.random.normal(0, 1, 100))
        >>> results = bl.diagnostic.normality_test(data)

        **Educational Notes:**
        - **Null Hypothesis (H0):** Data IS normally distributed
        - **Decision Rule:** If p-value < 0.05, reject H0 (data is NOT normal)

        - **Shapiro-Wilk Test:**
          Best for n < 5000, most powerful for detecting non-normality

        - **Anderson-Darling Test:**
          More sensitive to tails than Shapiro-Wilk

        - **Kolmogorov-Smirnov Test:**
          General-purpose test, less powerful but works for any distribution
        """
        data = series.dropna()

        # Shapiro-Wilk Test
        # LEARNING POINT: Tests if sample could come from normal distribution
        sw_stat, sw_pval = stats.shapiro(data)

        # Anderson-Darling Test
        # LEARNING POINT: More sensitive to distribution tails
        ad_result = stats.anderson(data)
        ad_stat = ad_result.statistic
        ad_crit = ad_result.critical_values[2]  # 5% significance level
        ad_pval = ad_result.significance_level[2] / 100

        # Kolmogorov-Smirnov Test (against standard normal)
        # LEARNING POINT: Compares empirical distribution to theoretical
        ks_stat, ks_pval = stats.kstest(data, 'norm', args=(data.mean(), data.std()))

        # Summary table
        table = RichTable(title="Normality Tests",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Test", style="cyan")
        table.add_column("Statistic", justify="right", style="magenta")
        table.add_column("P-Value", justify="right", style="yellow")
        table.add_column("Result", style="green")

        sw_result = "✓ Normal" if sw_pval > 0.05 else "✗ Not Normal"
        ad_result_str = "✓ Normal" if ad_stat < ad_crit else "✗ Not Normal"
        ks_result_str = "✓ Normal" if ks_pval > 0.05 else "✗ Not Normal"

        table.add_row("Shapiro-Wilk", f"{sw_stat:.4f}", f"{sw_pval:.4f}", sw_result)
        table.add_row("Anderson-Darling", f"{ad_stat:.4f}", f"{ad_pval:.4f}", ad_result_str)
        table.add_row("Kolmogorov-Smirnov", f"{ks_stat:.4f}", f"{ks_pval:.4f}", ks_result_str)

        console.print(table)

        # Overall conclusion
        tests_passed = sum([sw_pval > 0.05, ad_pval > 0.05, ks_pval > 0.05])
        if tests_passed >= 2:
            console.print("[bold green]✓ Data appears NORMALLY distributed[/bold green]")
            is_normal = True
        else:
            console.print("[bold yellow]✗ Data does NOT appear normally distributed[/bold yellow]")
            console.print("[dim]Consider non-parametric tests (Mann-Whitney U, Kruskal-Wallis)[/dim]")
            is_normal = False

        return {
            'shapiro_wilk': {'stat': sw_stat, 'pval': sw_pval},
            'anderson_darling': {'stat': ad_stat, 'pval': ad_pval},
            'kolmogorov_smirnov': {'stat': ks_stat, 'pval': ks_pval},
            'is_normal': is_normal,
            'recommendation': 'parametric' if is_normal else 'non-parametric'
        }

    @staticmethod
    def correlation_analysis(df: pd.DataFrame) -> Tuple[RichTable, pd.DataFrame]:
        """
        Analyze correlations between numeric variables.

        **What this does (Educational):**
        Correlation measures how two variables move together.
        - Positive correlation: Variables increase together
        - Negative correlation: One increases, other decreases
        - Zero correlation: No linear relationship

        **Parameters:**
        -----------
        df : pd.DataFrame
            Input dataframe with numeric columns

        **Returns:**
        --------
        Tuple[RichTable, pd.DataFrame]
            - Formatted correlation table
            - Correlation matrix (for heatmap visualization)

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> df = pd.DataFrame({'a': [1,2,3], 'b': [2,4,6]})
        >>> table, corr_matrix = bl.diagnostic.correlation_analysis(df)

        **Educational Notes:**
        - **Pearson Correlation:**
          Measures linear relationship, ranges -1 to +1
          -1 = perfect negative, 0 = no relation, +1 = perfect positive

        - **Spearman Correlation:**
          Uses ranks instead of values, better for non-linear relationships
          More robust to outliers

        - **Interpretation:**
          |r| < 0.3: weak, 0.3-0.7: moderate, >0.7: strong
        """
        numeric_df = df.select_dtypes(include=[np.number])

        # Calculate Pearson and Spearman correlations
        # LEARNING POINT: Pearson uses actual values, Spearman uses ranks
        pearson_corr = numeric_df.corr(method='pearson')
        spearman_corr = numeric_df.corr(method='spearman')

        # Create correlation table
        table = RichTable(title="Correlation Analysis (Pearson & Spearman)",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Variable Pair", style="cyan")
        table.add_column("Pearson r", justify="right", style="magenta")
        table.add_column("Spearman ρ", justify="right", style="yellow")
        table.add_column("Strength", style="green")

        # Show significant correlations (|r| > 0.3)
        significant_pairs = []
        for i in range(len(pearson_corr.columns)):
            for j in range(i + 1, len(pearson_corr.columns)):
                col1, col2 = pearson_corr.columns[i], pearson_corr.columns[j]
                p_corr = pearson_corr.loc[col1, col2]
                s_corr = spearman_corr.loc[col1, col2]

                if abs(p_corr) > 0.3:  # Only show moderate and strong
                    strength = "Strong" if abs(p_corr) > 0.7 else "Moderate"
                    table.add_row(
                        f"{col1} ↔ {col2}",
                        f"{p_corr:.3f}",
                        f"{s_corr:.3f}",
                        strength
                    )
                    significant_pairs.append((col1, col2, p_corr))

        if not significant_pairs:
            table.add_row("[No significant correlations]", "-", "-", "-")

        console.print(table)

        # Create and show heatmap
        if len(numeric_df.columns) > 1:
            plt.figure(figsize=(8, 6))
            sns.heatmap(pearson_corr, annot=True, fmt='.2f', cmap='coolwarm',
                       center=0, vmin=-1, vmax=1, square=True)
            plt.title("Pearson Correlation Heatmap")
            plt.tight_layout()
            plt.savefig('/tmp/correlation_heatmap.png', dpi=100, bbox_inches='tight')
            plt.close()
            console.print("[dim]Correlation heatmap saved to /tmp/correlation_heatmap.png[/dim]")

        return table, pearson_corr

    @staticmethod
    def missing_value_analysis(df: pd.DataFrame) -> RichTable:
        """
        Analyze patterns and severity of missing data.

        **What this does (Educational):**
        Missing data is a data quality issue. Understanding its pattern helps
        decide whether to drop, impute, or investigate further.

        **Parameters:**
        -----------
        df : pd.DataFrame
            Input dataframe

        **Returns:**
        --------
        RichTable
            Missing value analysis

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> df = pd.DataFrame({'a': [1, None, 3], 'b': [4, 5, None]})
        >>> bl.diagnostic.missing_value_analysis(df)

        **Educational Notes:**
        - **MCAR:** Missing Completely At Random (safest, can be ignored)
        - **MAR:** Missing At Random (depends on observed data)
        - **MNAR:** Missing Not At Random (biased, investigate cause)
        """
        table = RichTable(title="Missing Value Analysis",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Missing Count", justify="right", style="red")
        table.add_column("Missing %", justify="right", style="yellow")
        table.add_column("Data Type", style="magenta")

        total_rows = len(df)
        total_missing = df.isnull().sum().sum()

        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_pct = (missing_count / total_rows) * 100

            severity = "🔴 Critical" if missing_pct > 50 else "🟠 High" if missing_pct > 20 else "🟡 Medium" if missing_pct > 5 else "✓ Low"

            table.add_row(
                col,
                str(missing_count),
                f"{missing_pct:.1f}%",
                f"{df[col].dtype}"
            )

        console.print(table)
        console.print(f"[bold]Total Missing Values: {total_missing}[/bold] ({total_missing/(total_rows*len(df))*100:.1f}% of all data)")

        return table

    @staticmethod
    def duplicate_analysis(df: pd.DataFrame) -> Tuple[int, RichTable]:
        """
        Identify exact duplicate rows.

        **What this does (Educational):**
        Duplicate records inflate sample size and bias analysis results.
        This identifies and removes them.

        **Parameters:**
        -----------
        df : pd.DataFrame
            Input dataframe

        **Returns:**
        --------
        Tuple[int, RichTable]
            - Count of duplicates
            - Sample of duplicates
        """
        duplicates = df[df.duplicated(keep=False)].sort_values(by=list(df.columns))
        dup_count = len(df) - len(df.drop_duplicates())

        table = RichTable(title=f"Duplicate Analysis (Found {dup_count} duplicates)",
                         show_header=True,
                         header_style="bold blue")

        if dup_count == 0:
            console.print("[bold green]✓ No duplicate rows found[/bold green]")
            return 0, table

        # Show first few columns of duplicates
        for col in df.columns[:5]:
            table.add_column(col, style="cyan")

        for idx, row in duplicates.head(10).iterrows():
            table.add_row(*[str(row[col])[:20] for col in df.columns[:5]])

        console.print(table)
        return dup_count, table

    @staticmethod
    def data_type_consistency(df: pd.DataFrame) -> RichTable:
        """
        Check for type inconsistencies within columns.

        **What this does (Educational):**
        Sometimes columns have mixed types (e.g., numbers and strings in same column).
        This identifies those issues.
        """
        table = RichTable(title="Data Type Consistency Check",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Primary Type", justify="right", style="magenta")
        table.add_column("Non-Null Count", justify="right")
        table.add_column("Unique Types", style="yellow")

        issues_found = 0
        for col in df.columns:
            primary_type = df[col].dtype
            non_null = df[col].notna().sum()
            unique_types = df[col].apply(type).nunique()

            if unique_types > 1:
                issues_found += 1
                status = "⚠️ Mixed types"
            else:
                status = "✓ Consistent"

            table.add_row(
                col,
                str(primary_type),
                str(non_null),
                f"{unique_types} ({status})"
            )

        console.print(table)
        if issues_found > 0:
            console.print(f"[bold yellow]⚠️ Found {issues_found} columns with mixed data types[/bold yellow]")

        return table

    @staticmethod
    def cardinality_analysis(df: pd.DataFrame) -> RichTable:
        """
        Analyze unique value counts and diversity per column.

        **What this does (Educational):**
        - Low cardinality: Few unique values (categorical)
        - High cardinality: Many unique values (unique identifiers, bad)
        """
        table = RichTable(title="Cardinality Analysis",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Unique Count", justify="right", style="magenta")
        table.add_column("Cardinality %", justify="right", style="yellow")
        table.add_column("Type", style="green")

        for col in df.columns:
            unique_count = df[col].nunique()
            cardinality_pct = (unique_count / len(df)) * 100

            if cardinality_pct < 5:
                col_type = "Low (Categorical)"
            elif cardinality_pct > 95:
                col_type = "High (Identifier?)"
            else:
                col_type = "Medium"

            table.add_row(
                col,
                str(unique_count),
                f"{cardinality_pct:.1f}%",
                col_type
            )

        console.print(table)
        return table

    @staticmethod
    def sample_vs_population(sample_data: pd.Series, pop_mean: float, pop_std: float,
                            column_name: str = "Value") -> Dict[str, Union[float, str]]:
        """
        Educational: Compare sample statistics to population parameters.

        **What this does (Educational):**
        Shows whether a sample is representative of the population.
        Uses t-test and effect size to assess the difference.

        **Parameters:**
        -----------
        sample_data : pd.Series
            Sample data
        pop_mean : float
            Known population mean
        pop_std : float
            Known population standard deviation
        column_name : str
            Column name for display

        **Returns:**
        --------
        dict
            T-test results and interpretation
        """
        # Perform one-sample t-test
        t_stat, p_value = stats.ttest_1samp(sample_data.dropna(), pop_mean)

        # Calculate effect size (Cohen's d)
        sample_mean = sample_data.mean()
        cohens_d = (sample_mean - pop_mean) / pop_std

        # Calculate confidence interval
        n = len(sample_data.dropna())
        se = sample_data.std() / np.sqrt(n)
        ci_lower = sample_mean - 1.96 * se
        ci_upper = sample_mean + 1.96 * se

        # Create results table
        table = RichTable(title=f"Sample vs Population — {column_name}",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Metric", style="cyan")
        table.add_column("Sample", justify="right", style="magenta")
        table.add_column("Population", justify="right", style="green")
        table.add_column("Difference", justify="right", style="yellow")

        table.add_row("Mean", f"{sample_mean:.4f}", f"{pop_mean:.4f}", f"{(sample_mean - pop_mean):.4f}")
        table.add_row("Std Dev", f"{sample_data.std():.4f}", f"{pop_std:.4f}", "-")
        table.add_row("N", str(len(sample_data.dropna())), "Unknown", "-")
        table.add_row("95% CI", f"[{ci_lower:.4f}, {ci_upper:.4f}]", "-", "-")

        console.print(table)
        console.print(f"\n[bold]T-Test Results:[/bold]")
        console.print(f"  t-statistic: {t_stat:.4f}")
        console.print(f"  p-value: {p_value:.4f}")
        console.print(f"  Cohen's d: {cohens_d:.4f}")

        if p_value < 0.05:
            console.print(f"[bold yellow]⚠️ Sample mean is significantly different from population mean (p < 0.05)[/bold yellow]")
        else:
            console.print(f"[bold green]✓ Sample mean is consistent with population mean (p ≥ 0.05)[/bold green]")

        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'sample_mean': sample_mean,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'is_different': p_value < 0.05
        }
