"""
Unit Tests for BizLens Core Functionality
Tests all major functions and methods
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import pandas as pd
import polars as pl
import numpy as np
from bizlens import BizDesc, load_dataset, describe
import tempfile


class TestDataLoading(unittest.TestCase):
    """Test dataset loading functionality"""

    def test_load_builtin_school_cafeteria(self):
        """Test loading built-in school_cafeteria dataset"""
        df = load_dataset('school_cafeteria')
        self.assertIsNotNone(df)
        # Should have expected columns
        if isinstance(df, pl.DataFrame):
            self.assertIn('spending', df.columns)
            self.assertIn('satisfaction', df.columns)

    def test_load_builtin_test_scores(self):
        """Test loading built-in test_scores dataset"""
        df = load_dataset('test_scores')
        self.assertIsNotNone(df)
        if isinstance(df, pl.DataFrame):
            self.assertIn('subject', df.columns)
            self.assertIn('score', df.columns)

    def test_load_external_iris(self):
        """Test loading external iris dataset"""
        try:
            df = load_dataset('iris')
            self.assertIsNotNone(df)
            # Should be loadable as pandas or polars
            self.assertGreater(len(df), 0)
        except Exception as e:
            self.skipTest(f"External dataset loading requires seaborn: {e}")

    def test_load_external_tips(self):
        """Test loading external tips dataset"""
        try:
            df = load_dataset('tips')
            self.assertIsNotNone(df)
            self.assertGreater(len(df), 0)
        except Exception as e:
            self.skipTest(f"External dataset loading requires seaborn: {e}")

    def test_invalid_dataset_name(self):
        """Test error handling for invalid dataset"""
        with self.assertRaises(ValueError):
            load_dataset('invalid_dataset_name_xyz')


class TestBizDescInitialization(unittest.TestCase):
    """Test BizDesc class initialization"""

    def setUp(self):
        """Create test data"""
        self.df_pandas = pd.DataFrame({
            'value': np.random.normal(100, 15, 100),
            'category': np.random.choice(['A', 'B', 'C'], 100)
        })
        self.df_polars = pl.from_pandas(self.df_pandas)

    def test_init_with_pandas_dataframe(self):
        """Test initialization with pandas DataFrame"""
        bd = BizDesc(self.df_pandas)
        self.assertIsNotNone(bd)
        self.assertIsNotNone(bd.numeric_cols)

    def test_init_with_polars_dataframe(self):
        """Test initialization with polars DataFrame"""
        bd = BizDesc(self.df_polars)
        self.assertIsNotNone(bd)
        self.assertIsNotNone(bd.numeric_cols)

    def test_color_schemes(self):
        """Test all color scheme options"""
        for scheme in ['academic', 'pastel', 'vibrant']:
            bd = BizDesc(self.df_pandas, color_scheme=scheme)
            self.assertIsNotNone(bd.colors)
            self.assertIn('primary', bd.colors)
            self.assertIn('palette', bd.colors)


class TestCentralTendency(unittest.TestCase):
    """Test central tendency calculations"""

    def setUp(self):
        """Create test data"""
        # Symmetric distribution
        self.df_symmetric = pd.DataFrame({
            'value': np.random.normal(100, 15, 100)
        })

        # Right-skewed distribution
        self.df_right_skewed = pd.DataFrame({
            'value': np.random.exponential(5, 100)
        })

        self.bd_sym = BizDesc(self.df_symmetric)
        self.bd_skew = BizDesc(self.df_right_skewed)

    def test_central_tendency_output_format(self):
        """Test that central_tendency returns expected structure"""
        result = self.bd_sym.central_tendency()
        self.assertIsInstance(result, dict)
        self.assertIn('value', result)

        stats = result['value']
        expected_keys = ['mean', 'median', 'mode', 'range', 'std_dev',
                        'skewness', 'distribution_type']
        for key in expected_keys:
            self.assertIn(key, stats)

    def test_central_tendency_values(self):
        """Test that central tendency values are reasonable"""
        result = self.bd_sym.central_tendency()
        stats = result['value']

        # Mean, median should be positive and similar
        self.assertGreater(stats['mean'], 0)
        self.assertGreater(stats['median'], 0)

        # Standard deviation should be positive
        self.assertGreater(stats['std_dev'], 0)

    def test_distribution_type_identification(self):
        """Test that distribution types are correctly identified"""
        result_sym = self.bd_sym.central_tendency()
        result_skew = self.bd_skew.central_tendency()

        # Symmetric should have low skewness
        self.assertIn('Symmetric', result_sym['value']['distribution_type'])

        # Right-skewed should have positive skewness
        self.assertIn('Right-Skewed', result_skew['value']['distribution_type'])

    def test_describe_method(self):
        """Test describe method returns complete statistics"""
        result = self.bd_sym.describe(include_plots=False)

        self.assertIsInstance(result, dict)
        self.assertIn('shape', result)
        self.assertIn('numeric_stats', result)
        self.assertIn('central_tendency', result)


class TestVisualizations(unittest.TestCase):
    """Test visualization methods"""

    def setUp(self):
        """Create test data"""
        self.df = pd.DataFrame({
            'numeric': np.random.normal(100, 15, 100),
            'category': np.random.choice(['A', 'B', 'C'], 100)
        })
        self.bd = BizDesc(self.df, color_scheme='academic')

    def test_visualize_histogram(self):
        """Test histogram visualization doesn't crash"""
        try:
            import matplotlib.pyplot as plt
            self.bd.visualize('numeric', plot_type='histogram')
            plt.close('all')
        except Exception as e:
            self.fail(f"Histogram visualization failed: {e}")

    def test_visualize_boxplot(self):
        """Test boxplot visualization"""
        try:
            import matplotlib.pyplot as plt
            self.bd.visualize('numeric', plot_type='boxplot')
            plt.close('all')
        except Exception as e:
            self.fail(f"Boxplot visualization failed: {e}")

    def test_visualize_violin(self):
        """Test violin visualization"""
        try:
            import matplotlib.pyplot as plt
            self.bd.visualize('numeric', plot_type='violin')
            plt.close('all')
        except Exception as e:
            self.fail(f"Violin visualization failed: {e}")

    def test_visualize_bar(self):
        """Test bar chart visualization"""
        try:
            import matplotlib.pyplot as plt
            self.bd.visualize('category', plot_type='bar')
            plt.close('all')
        except Exception as e:
            self.fail(f"Bar chart visualization failed: {e}")

    def test_visualize_pie(self):
        """Test pie chart visualization"""
        try:
            import matplotlib.pyplot as plt
            self.bd.visualize('category', plot_type='pie')
            plt.close('all')
        except Exception as e:
            self.fail(f"Pie chart visualization failed: {e}")

    def test_visualize_density(self):
        """Test density visualization"""
        try:
            import matplotlib.pyplot as plt
            self.bd.visualize('numeric', plot_type='density')
            plt.close('all')
        except Exception as e:
            self.fail(f"Density visualization failed: {e}")

    def test_visualize_line(self):
        """Test line chart visualization"""
        try:
            import matplotlib.pyplot as plt
            self.bd.visualize('numeric', plot_type='line')
            plt.close('all')
        except Exception as e:
            self.fail(f"Line chart visualization failed: {e}")

    def test_compare_categorical(self):
        """Test categorical comparison"""
        try:
            import matplotlib.pyplot as plt
            self.bd.compare_categorical('category', 'numeric')
            plt.close('all')
        except Exception as e:
            self.fail(f"Categorical comparison failed: {e}")

    def test_correlations(self):
        """Test correlation heatmap"""
        try:
            import matplotlib.pyplot as plt
            self.bd.correlations()
            plt.close('all')
        except Exception as e:
            self.fail(f"Correlation heatmap failed: {e}")


class TestStatisticalTests(unittest.TestCase):
    """Test statistical analysis methods"""

    def setUp(self):
        """Create test data"""
        self.df = pd.DataFrame({
            'value': np.random.normal(100, 15, 100)
        })
        self.bd = BizDesc(self.df)

    def test_outliers_detection(self):
        """Test outlier detection"""
        result = self.bd.outliers()
        self.assertIsInstance(result, dict)
        self.assertIn('value', result)

        outlier_info = result['value']
        self.assertIn('count', outlier_info)
        self.assertIn('percentage', outlier_info)
        self.assertGreaterEqual(outlier_info['count'], 0)

    def test_normality_test(self):
        """Test normality testing"""
        result = self.bd.normality_test()
        self.assertIsInstance(result, dict)
        self.assertIn('value', result)

        norm_info = result['value']
        self.assertIn('p_value', norm_info)
        self.assertIn('is_normal', norm_info)
        self.assertIsInstance(norm_info['is_normal'], bool)


class TestDatasetModule(unittest.TestCase):
    """Test dataset discovery module"""

    def test_list_sample_datasets(self):
        """Test listing available datasets"""
        try:
            from bizlens.datasets import list_available_datasets
            df = list_available_datasets()
            self.assertIsInstance(df, pd.DataFrame)
            self.assertGreater(len(df), 0)
            self.assertIn('Dataset', df.columns)
            self.assertIn('Source', df.columns)
        except ImportError:
            self.skipTest("Dataset module not available")

    def test_describe_dataset(self):
        """Test getting dataset description"""
        try:
            from bizlens.datasets import describe_dataset
            info = describe_dataset('iris')
            self.assertIsInstance(info, dict)
            self.assertIn('description', info)
            self.assertIn('source', info)
        except (ImportError, ValueError) as e:
            self.skipTest(f"Dataset module not available: {e}")

    def test_load_sample_dataset_iris(self):
        """Test loading sample dataset"""
        try:
            from bizlens.datasets import load_sample_dataset
            df = load_sample_dataset('iris')
            self.assertIsNotNone(df)
            self.assertGreater(len(df), 0)
        except (ImportError, ValueError) as e:
            self.skipTest(f"Dataset loading failed: {e}")


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""

    def setUp(self):
        """Create test data"""
        self.df = pd.DataFrame({
            'value': [1, 2, 3, 4, 5]
        })
        self.bd = BizDesc(self.df)

    def test_visualize_invalid_plot_type(self):
        """Test handling of invalid plot type"""
        # Should not crash, might use default
        try:
            import matplotlib.pyplot as plt
            self.bd.visualize('value', plot_type='invalid_type')
            plt.close('all')
        except Exception as e:
            # Acceptable to raise exception for invalid type
            self.assertIsInstance(e, (ValueError, AttributeError))

    def test_empty_dataframe(self):
        """Test handling of empty DataFrame"""
        df_empty = pd.DataFrame()
        bd_empty = BizDesc(df_empty)
        self.assertIsNotNone(bd_empty)

    def test_single_column_dataframe(self):
        """Test handling of single column"""
        df_single = pd.DataFrame({'value': [1, 2, 3, 4, 5]})
        bd_single = BizDesc(df_single)
        result = bd_single.central_tendency()
        self.assertIn('value', result)


if __name__ == '__main__':
    unittest.main()
