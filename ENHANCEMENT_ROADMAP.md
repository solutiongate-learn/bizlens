# BizLens Enhancement Roadmap 🗺️
## v0.6.0 - v1.0 Implementation Plan

---

## Overview

**Goal**: Move BizLens from "nice descriptive stats tool" → "must-have educational analytics platform"

**Timeline**:
- **v0.6.0** (4 weeks): Hypothesis testing + HTML exports
- **v0.7.0** (8 weeks): Advanced analytics + data quality
- **v1.0** (12 weeks): Production-ready with full test coverage

---

## 🎯 v0.6.0: Educational + Professional (4 weeks)

### Feature 1: Hypothesis Testing for Normality

**Why**: Teaches students what p-values mean; differentiates from competitors

**Implementation**:
```python
# In src/bizlens/core.py - add to BizDesc class

def normality_test(self, alpha: float = 0.05) -> Dict[str, Any]:
    """
    Run Shapiro-Wilk test for normality on numeric columns.

    Returns:
        {
            "revenue": {
                "statistic": 0.892,
                "p_value": 0.0001,
                "is_normal": False,
                "interpretation": "Data significantly deviates from normal (p < 0.05)"
            },
            ...
        }
    """
    from scipy.stats import shapiro

    nw_df = self.df
    numeric_cols = nw_df.select(nw.col(nw.NUMERIC_DTYPES)).columns
    results = {}

    for col in numeric_cols:
        col_data = np.array(nw_df[col].to_numpy())
        col_data = col_data[~np.isnan(col_data)]

        if len(col_data) < 3:
            continue

        stat, p_value = shapiro(col_data)
        is_normal = p_value > alpha

        results[col] = {
            "statistic": round(float(stat), 4),
            "p_value": round(float(p_value), 6),
            "is_normal": is_normal,
            "interpretation": (
                f"Normal distribution (p = {p_value:.4f} > 0.05)"
                if is_normal
                else f"Not normal (p = {p_value:.4f} < 0.05)"
            )
        }

    return results
```

**Integration**:
- Call in `summary()` by default
- Print results in `_print_rich_summary()`
- Add to returned dictionary

**Testing**:
```python
# tests/test_bizlens.py - add test case

def test_normality_test_skewed_data():
    """Exponential data should fail normality test."""
    data = np.random.exponential(scale=100, size=100)
    df = pl.DataFrame({"revenue": data})
    bd = BizDesc(df)
    result = bd.normality_test()

    assert result["revenue"]["is_normal"] == False
    assert result["revenue"]["p_value"] < 0.05
```

**Documentation**:
- Add to README under "Statistical Testing"
- Example: "Teaching students p-values"

**Effort**: ~2-3 hours

---

### Feature 2: HTML Report Export

**Why**: Professional shareable reports; table stakes for business use

**Implementation Steps**:

#### Step 1: Create HTML template (`src/bizlens/templates/report.html`)
```html
<!DOCTYPE html>
<html>
<head>
    <title>BizLens Report - {{ dataset_name }}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 20px; background: #f5f5f5; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #3498db; color: white; }
        .stat-badge { display: inline-block; padding: 5px 10px; background: #ecf0f1; border-radius: 4px; margin: 2px; }
        .warning { color: #e74c3c; font-weight: bold; }
        .success { color: #27ae60; }
    </style>
</head>
<body>
    <div class="card header">
        <h1>📊 BizLens Data Analysis Report</h1>
        <p><strong>Dataset:</strong> {{ dataset_name }}</p>
        <p><strong>Generated:</strong> {{ timestamp }}</p>
    </div>

    <!-- Summary Stats -->
    <div class="card">
        <h2>📈 Overview</h2>
        <p>
            <span class="stat-badge"><strong>Rows:</strong> {{ rows }}</span>
            <span class="stat-badge"><strong>Columns:</strong> {{ cols }}</span>
            <span class="stat-badge"><strong>Missing:</strong> {{ total_missing }}</span>
        </p>
    </div>

    <!-- Numeric Statistics -->
    <div class="card">
        <h2>🔢 Numeric Columns</h2>
        <table>
            <tr>
                <th>Column</th>
                <th>Mean</th>
                <th>Median</th>
                <th>Skewness</th>
                <th>Std Dev</th>
                <th>Normal?</th>
            </tr>
            {% for stat in numeric_stats %}
            <tr>
                <td><strong>{{ stat.Column }}</strong></td>
                <td>{{ stat.Mean }}</td>
                <td>{{ stat.Median }}</td>
                <td><span class="{% if stat.Skewness|abs > 1 %}warning{% else %}success{% endif %}">{{ stat.Skewness }}</span></td>
                <td>{{ stat.Std_Dev }}</td>
                <td><span class="{% if normality_results[stat.Column].is_normal %}success{% else %}warning{% endif %}">
                    {% if normality_results[stat.Column].is_normal %}✓ Yes{% else %}✗ No{% endif %}
                </span></td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <!-- Charts -->
    <div class="card">
        <h2>📉 Distribution Visualizations</h2>
        <div id="charts-container">
            {% for chart_html in chart_divs %}
            {{ chart_html|safe }}
            {% endfor %}
        </div>
    </div>

    <!-- Normality Testing -->
    <div class="card">
        <h2>🔬 Hypothesis Testing (Shapiro-Wilk)</h2>
        <table>
            <tr>
                <th>Column</th>
                <th>Statistic</th>
                <th>p-value</th>
                <th>Conclusion (α=0.05)</th>
            </tr>
            {% for col, result in normality_results.items() %}
            <tr>
                <td><strong>{{ col }}</strong></td>
                <td>{{ result.statistic }}</td>
                <td>{{ result.p_value }}</td>
                <td><span class="{% if result.is_normal %}success{% else %}warning{% endif %}">
                    {{ result.interpretation }}
                </span></td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <!-- Footer -->
    <div class="card" style="text-align: center; color: #7f8c8d; font-size: 12px;">
        <p>Generated by BizLens v{{ bizlens_version }}</p>
        <p><a href="https://github.com/yourusername/bizlens">Learn more →</a></p>
    </div>
</body>
</html>
```

#### Step 2: Add export method to `core.py`
```python
def export_html(self, filepath: str, include_normality: bool = True):
    """
    Export analysis as self-contained HTML report.

    Args:
        filepath: Where to save HTML (e.g., "report.html")
        include_normality: Include Shapiro-Wilk test results
    """
    from jinja2 import Template
    from pathlib import Path
    import json
    from datetime import datetime

    # Generate current analysis if not cached
    if not self._last_result:
        self.summary(include_plots=False)

    # Generate normality test results
    normality_results = self.normality_test() if include_normality else {}

    # Generate charts as Plotly JSON
    chart_divs = self._generate_plotly_charts()  # New helper method

    # Load template
    template_path = Path(__file__).parent / "templates" / "report.html"
    with open(template_path) as f:
        template_str = f.read()

    template = Template(template_str)

    # Render
    html = template.render(
        dataset_name=getattr(self, 'filename', 'DataFrame'),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        rows=self._last_result['shape'][0],
        cols=self._last_result['shape'][1],
        total_missing=sum(self._last_result['missing_values'].values()),
        numeric_stats=self._last_result['numeric_stats'],
        normality_results=normality_results,
        chart_divs=chart_divs,
        bizlens_version=__version__
    )

    # Write
    Path(filepath).write_text(html)
    console.print(f"[bold green]✅ Report exported to {filepath}[/bold green]")
```

#### Step 3: Add Plotly chart generation
```python
def _generate_plotly_charts(self) -> List[str]:
    """Generate Plotly charts as HTML divs."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    nw_df = self.df
    numeric_cols = nw_df.select(nw.col(nw.NUMERIC_DTYPES)).columns
    chart_divs = []

    for col in numeric_cols[:5]:  # Limit to 5 for file size
        data = np.array(nw_df[col].to_numpy())
        data = data[~np.isnan(data)]

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(f"Distribution: {col}", "Z-Score vs Normal"),
            specs=[[{"type": "histogram"}, {"type": "histogram"}]]
        )

        # Left: Data histogram
        fig.add_trace(
            go.Histogram(x=data, name=col, nbinsx=30, marker_color='#3498db'),
            row=1, col=1
        )

        # Right: Z-score comparison
        mean_v, std_v = np.mean(data), np.std(data)
        z_data = (data - mean_v) / std_v
        fig.add_trace(
            go.Histogram(x=z_data, name="Z-Score", nbinsx=30, marker_color='#e74c3c'),
            row=1, col=2
        )

        fig.update_layout(height=400, showlegend=True)

        # Convert to HTML div
        html_div = fig.to_html(include_plotlyjs=False, div_id=f"chart_{col}")
        chart_divs.append(html_div)

    return chart_divs
```

**Testing**:
```python
def test_export_html(tmp_path):
    """Test HTML export functionality."""
    df = pl.DataFrame({
        "revenue": np.random.exponential(1000, 100),
        "satisfaction": np.random.normal(7, 1.5, 100)
    })

    bd = BizDesc(df)
    html_path = tmp_path / "report.html"
    bd.export_html(str(html_path))

    assert html_path.exists()
    html_content = html_path.read_text()
    assert "BizLens" in html_content
    assert "Shapiro" in html_content
    assert "plotly" in html_content.lower()
```

**Effort**: ~4-5 hours

---

### Feature 3: Outlier Detection

**Why**: Data quality flag; teaches data cleaning

**Implementation**:
```python
def flag_anomalies(self, method: str = 'iqr', threshold: float = 1.5) -> Dict[str, Any]:
    """
    Detect outliers using IQR or Z-score method.

    Args:
        method: 'iqr' or 'zscore'
        threshold: IQR multiplier (1.5) or Z-score threshold (3.0)

    Returns:
        {
            "revenue": {
                "count": 5,
                "percentage": 5.0,
                "indices": [10, 42, 88, ...],
                "values": [45000, 52000, ...],
                "bounds": {"lower": 100, "upper": 5000}
            }
        }
    """
    nw_df = self.df
    numeric_cols = nw_df.select(nw.col(nw.NUMERIC_DTYPES)).columns
    results = {}

    native_df = nw_df.to_native()
    if isinstance(native_df, pl.DataFrame):
        native_df = native_df.to_pandas()

    for col in numeric_cols:
        data = native_df[col].dropna()

        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - threshold * IQR
            upper = Q3 + threshold * IQR
        else:  # zscore
            mean, std = data.mean(), data.std()
            lower = mean - threshold * std
            upper = mean + threshold * std

        outliers_mask = (data < lower) | (data > upper)
        outlier_indices = data[outliers_mask].index.tolist()
        outlier_values = data[outliers_mask].values.tolist()

        results[col] = {
            "count": int(outliers_mask.sum()),
            "percentage": float(100 * outliers_mask.sum() / len(data)),
            "indices": outlier_indices,
            "values": outlier_values,
            "bounds": {"lower": float(lower), "upper": float(upper)}
        }

    return results
```

**Effort**: ~2 hours

---

### Feature 4: Categorical Analysis

**Why**: Complete descriptive statistics for all data types

**Implementation**:
```python
def _analyze_categorical(self, cat_cols: List[str]) -> List[Dict]:
    """Analyze categorical columns."""
    results = []

    nw_df = self.df
    native_df = nw_df.to_native()
    if isinstance(native_df, pl.DataFrame):
        native_df = native_df.to_pandas()

    for col in cat_cols:
        value_counts = native_df[col].value_counts()

        results.append({
            "Column": col,
            "Distinct": len(value_counts),
            "Top": value_counts.index[0],
            "Top_Count": int(value_counts.iloc[0]),
            "Missing": int(native_df[col].isna().sum()),
            "Entropy": self._calculate_entropy(value_counts)
        })

    return results

def _calculate_entropy(self, value_counts):
    """Calculate Shannon entropy for categorical column."""
    proportions = value_counts / value_counts.sum()
    entropy = -np.sum(proportions * np.log2(proportions + 1e-10))
    return round(float(entropy), 2)
```

**Effort**: ~2 hours

---

## Timeline & Checkpoints

### Week 1: Hypothesis Testing
- [ ] Implement `normality_test()` method
- [ ] Add p-value interpretation
- [ ] Update test suite
- [ ] Update README

### Week 2: HTML Export Skeleton
- [ ] Create HTML template
- [ ] Implement `export_html()` method
- [ ] Test basic export
- [ ] Debug chart rendering

### Week 3: Charts + Polish
- [ ] Integrate Plotly charts
- [ ] Add CSS styling
- [ ] Test in browser
- [ ] Performance optimization

### Week 4: Outlier + Categorical
- [ ] Implement `flag_anomalies()`
- [ ] Expand categorical analysis
- [ ] Full integration test
- [ ] Prepare v0.6.0 release

---

## Dependencies to Add

```toml
# In pyproject.toml optional-dependencies

[project.optional-dependencies]
all = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "jinja2>=3.1.0",      # For HTML templates
    "plotly>=5.0.0",      # For interactive charts
]
```

---

## Quality Assurance

### Test Coverage Goals
- Hypothesis testing: 100%
- HTML export: 95%
- Outlier detection: 100%
- Categorical analysis: 95%

### Integration Testing
```python
def test_full_v0_6_pipeline():
    """Complete v0.6.0 workflow test."""
    df = bl.create_interactive_demo()
    bd = bl.BizDesc(df)

    # Test summary with new features
    result = bd.summary(include_plots=False)
    assert "normality_stats" in result

    # Test normality testing
    norm = bd.normality_test()
    assert "revenue" in norm
    assert "p_value" in norm["revenue"]

    # Test outlier detection
    outliers = bd.flag_anomalies()
    assert "revenue" in outliers

    # Test HTML export
    bd.export_html("test_report.html")
    assert Path("test_report.html").exists()
```

---

## Documentation Updates

### README Additions
- [ ] "Statistical Hypothesis Testing" section
- [ ] "Generate HTML Reports" example
- [ ] "Detect Outliers" use case
- [ ] Comparison with ydata-profiling

### API Documentation
- [ ] docstrings for new methods
- [ ] Parameter examples
- [ ] Return value structure
- [ ] Educational interpretation

### Jupyter Notebook
- [ ] Full workflow demo
- [ ] Before/after HTML report
- [ ] Teaching use cases
- [ ] Business examples

---

## Performance Benchmarks

Target completion time for v0.6.0 features:

| Dataset Size | Time | Target |
|-------------|------|--------|
| 1,000 rows | <1s | <1s |
| 10,000 rows | <2s | <2s |
| 100,000 rows | <5s | <10s |
| 1,000,000 rows | <15s | <30s |

**Polars advantage**: Zero-copy analysis on large datasets

---

## Success Criteria for v0.6.0 Release

✅ All 4 features implemented and tested
✅ >85% test coverage
✅ HTML report matches Sweetviz quality
✅ Shapiro-Wilk correctly detects non-normal data
✅ README updated with examples
✅ GitHub star count: 50+
✅ No critical bugs in first week

---

*Next update after v0.6.0 release: June 2026*
