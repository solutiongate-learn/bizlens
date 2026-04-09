# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.15] - 2026-04-09

### Added
- **Process Mining Enhancements**
  - `petri_net_from_log()` - Generate Petri nets from event logs
  - `visualize_petri_net()` - Render Petri net diagrams using NetworkX
  - `causal_net_from_log()` - Discover causal relationships in processes
  - `visualize_causal_net()` - Interactive Plotly visualization of causal nets
  - `alpha_algorithm()` - Implement the α-algorithm for workflow discovery
  - Complete workflow net validation and conformance checking framework

- **Google Colab Support**
  - "Open in Colab" badges on all 14 notebooks
  - Automatic Google Drive mount setup cells
  - Full pip install integration for Colab environment

- **New Notebook: Process_Mining_Foundations.ipynb**
  - 17 comprehensive cells covering Petri nets, causal nets, Alpha algorithm
  - Theory and practical implementation examples
  - Complete workflow net validation examples
  - Conformance checking with token replay

- **Dependency: NetworkX**
  - Added networkx >= 2.6.0 for graph visualization and Petri net analysis

### Fixed
- **Critical Import Error in core.py**
  - Fixed: `from . import quality` → `from .quality import quality`
  - Impact: Resolved AttributeError in `bl.describe()` method
  - Root cause: Module import vs class import confusion
  - Status: Verified with sample data

- **Variable Unpacking Bug in process_mining.transition_matrix()**
  - Fixed: Corrected unpacking of `value_counts().items()` tuples
  - Changed: `for _, row in ...items()` → `for (from_act, to_act), count in ...items()`
  - Impact: Eliminated "'int' object is not subscriptable" error
  - Status: Tested with event log data

- **Timedelta Serialization in process_mining.timeline_visualization()**
  - Fixed: Added timedelta → hours conversion for Plotly compatibility
  - Changed: `duration_hours = duration.total_seconds() / 3600`
  - Impact: Resolved "Object of type timedelta is not JSON serializable" error
  - Status: Timeline visualizations now render correctly

- **Rich Table Rendering in tables.summary_statistics()**
  - Fixed: String conversion for integer column names
  - Changed: `table.add_row(col, ...)` → `table.add_row(str(col), ...)`
  - Impact: Tables now render when column is integer (e.g., from unnamed Series)
  - Status: Verified with various column types

- **Pandas Boolean Dtype Compatibility**
  - Fixed: Added `astype(float)` before statsmodels OLS/Logit in 3 notebooks
  - Notebooks affected: Conjoint_Analysis, Linear_Regression, Logistic_Regression
  - Impact: Models now fit correctly with pandas >= 1.5.0
  - Status: Regression models verified working

- **Missing Seaborn Import in Q_Learning.ipynb**
  - Fixed: Added `import seaborn as sns` to imports cell
  - Status: Notebook now runs without NameError

### Changed
- **Enhanced Matplotlib Styling (All 14 Notebooks)**
  - Consistent theme across all visualizations:
    ```python
    plt.rcParams.update({
        'font.family': 'DejaVu Sans',
        'font.size': 12,
        'axes.titlesize': 15,
        'axes.titleweight': 'bold',
        'figure.dpi': 130,
        'figure.figsize': [10, 6],
        'figure.facecolor': 'white',
        'axes.facecolor': '#FAFAFA',
        'axes.grid': True,
        'grid.alpha': 0.4,
        'axes.spines.top': False,
        'axes.spines.right': False,
    })
    ```
  - Color palette: 8-color professional scheme
  - Line width: 2.2pt for better visibility
  - Figure DPI: 130 for high-quality output

- **Updated Dependencies in pyproject.toml**
  - numpy >= 1.21.0 (maintained)
  - pandas >= 1.5.0 (maintained)
  - scipy >= 1.9.0 (maintained)
  - statsmodels >= 0.13.0 (maintained)
  - matplotlib >= 3.6.0 (maintained)
  - seaborn >= 0.12.0 (maintained)
  - plotly >= 5.0.0 (maintained)
  - **networkx >= 2.6.0 (NEW)**
  - scikit-learn >= 1.0.0 (maintained)
  - rich >= 13.0.0 (maintained)

### Testing
- **Code Coverage**
  - 166+ notebook code cells executed successfully
  - 0 errors in final validation run
  - All 14 notebooks tested in Colab environment

- **Functionality Tests**
  - All core modules: ✅ Pass
  - All process mining functions: ✅ Pass
  - All table formatting: ✅ Pass
  - All notebook imports: ✅ Pass
  - All data visualizations: ✅ Pass

### Documentation
- Created: `v2.2.15_RELEASE_SUMMARY.md` - Detailed release notes
- Created: `COLAB_NOTEBOOKS.md` - All Colab notebook links
- Created: `v2.2.15_UPLOAD_CHECKLIST.md` - Upload validation checklist
- Updated: `README.md` - Version and feature updates
- Added: Process Mining Foundations notebook with comprehensive theory

### Security
- No security vulnerabilities introduced
- All external dependencies are stable, widely-used libraries
- No breaking changes to public API

### Deprecations
- None

### Removed
- None

## [2.2.14] - 2026-03-15

### Added
- Initial release of v2.2.14 features
- Basic process mining capabilities
- Statistical inference modules
- Descriptive analytics

### Changed
- Previous version features and improvements

---

## Guidelines for Future Releases

### Version Numbering
- **Major (X.0.0)**: Breaking changes, new architecture
- **Minor (0.X.0)**: New features, non-breaking additions
- **Patch (0.0.X)**: Bug fixes, minor improvements

### Release Checklist
- [ ] Update version in pyproject.toml
- [ ] Update version in src/bizlens/__init__.py
- [ ] Test all code cells in all notebooks
- [ ] Build distribution files: `python -m build`
- [ ] Update CHANGELOG.md
- [ ] Create GitHub release with tag
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Verify PyPI page
- [ ] Update documentation

### Testing Requirements
- All notebook cells must execute without errors
- Integration tests must pass: `pytest tests/`
- No import errors across modules
- Visualizations must render correctly
- Colab notebooks must run in cloud environment

---

## Contact & Issues

For bug reports and feature requests, please visit:
https://github.com/solutiongate-learn/bizlens/issues

For questions and discussions:
https://github.com/solutiongate-learn/bizlens/discussions
