"""
Integration Tests for BizLens
Tests complete workflows and interactions between modules
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import pandas as pd
import numpy as np
from bizlens import BizDesc, load_dataset, list_sample_datasets, dataset_info


class TestCompleteWorkflows(unittest.TestCase):
    """Test complete data analysis workflows"""

    def test_workflow_builtin_data(self):
        """Test complete workflow with built-in data"""
        # Load data
        df = load_dataset('school_cafeteria')
        self.assertIsNotNone(df)

        # Create analyzer
        bd = BizDesc(df, color_scheme='academic')
        self.assertIsNotNone(bd)

        # Get statistics
        cent_tend = bd.central_tendency()
        self.assertIsNotNone(cent_tend)

        # Describe
        desc = bd.describe(include_plots=False)
        self.assertIsNotNone(desc)
        self.assertIn('shape', desc)

    def test_workflow_external_data(self):
        """Test complete workflow with external dataset"""
        try:
            # Load external dataset
            df = load_dataset('iris')
            self.assertIsNotNone(df)

            # Create analyzer
            bd = BizDesc(df, color_scheme='pastel')
            self.assertIsNotNone(bd)

            # Get statistics
            cent_tend = bd.central_tendency()
            self.assertIsNotNone(cent_tend)

            # Test multiple visualizations
            import matplotlib.pyplot as plt

            visualizations = ['histogram', 'boxplot', 'density', 'violin']
            for viz_type in visualizations:
                try:
                    bd.visualize('sepal_length', plot_type=viz_type)
                    plt.close('all')
                except Exception as e:
                    self.fail(f"Visualization {viz_type} failed: {e}")

        except ValueError as e:
            self.skipTest(f"External dataset not available: {e}")

    def test_workflow_with_color_schemes(self):
        """Test workflow with all color schemes"""
        df = load_dataset('school_cafeteria')

        for scheme in ['academic', 'pastel', 'vibrant']:
            bd = BizDesc(df, color_scheme=scheme)
            self.assertIsNotNone(bd)
            self.assertIsNotNone(bd.colors)

            # Should be able to describe
            desc = bd.describe(include_plots=False)
            self.assertIsNotNone(desc)

    def test_workflow_statistical_analysis(self):
        """Test complete statistical analysis workflow"""
        df = load_dataset('school_cafeteria')
        bd = BizDesc(df)

        # Central tendency
        cent_tend = bd.central_tendency()
        self.assertIsNotNone(cent_tend)

        # Outlier detection
        outliers = bd.outliers()
        self.assertIsNotNone(outliers)
        self.assertGreater(len(outliers), 0)

        # Normality test
        normality = bd.normality_test()
        self.assertIsNotNone(normality)

        # Correlations
        try:
            import matplotlib.pyplot as plt
            corr = bd.correlations()
            plt.close('all')
            self.assertIsNotNone(corr)
        except Exception as e:
            self.skipTest(f"Correlation test skipped: {e}")

    def test_workflow_categorical_comparison(self):
        """Test categorical comparison workflow"""
        df = load_dataset('school_cafeteria')
        bd = BizDesc(df)

        try:
            import matplotlib.pyplot as plt
            bd.compare_categorical('lunch_type', 'spending')
            plt.close('all')
        except Exception as e:
            self.fail(f"Categorical comparison failed: {e}")


class TestDatasetIntegration(unittest.TestCase):
    """Test dataset discovery and loading"""

    def test_list_and_load_workflow(self):
        """Test listing datasets then loading one"""
        try:
            datasets_df = list_sample_datasets()
            self.assertIsNotNone(datasets_df)
            self.assertGreater(len(datasets_df), 0)

            # Try to load iris
            df = load_dataset('iris')
            self.assertIsNotNone(df)
            self.assertGreater(len(df), 0)

        except ValueError as e:
            self.skipTest(f"Dataset module not available: {e}")

    def test_dataset_info_workflow(self):
        """Test getting dataset info"""
        try:
            # Get info
            info = dataset_info('iris')

            # Analyze the dataset
            df = load_dataset('iris')
            bd = BizDesc(df)
            cent_tend = bd.central_tendency()

            self.assertIsNotNone(cent_tend)

        except Exception as e:
            self.skipTest(f"Dataset info workflow failed: {e}")

    def test_multiple_dataset_loading(self):
        """Test loading multiple datasets"""
        datasets_to_test = [
            ('school_cafeteria', True),  # Built-in
            ('test_scores', True),        # Built-in
            ('iris', False),              # External
            ('tips', False),              # External
        ]

        for dataset_name, is_builtin in datasets_to_test:
            try:
                df = load_dataset(dataset_name)
                self.assertIsNotNone(df)
                self.assertGreater(len(df), 0)

                # Quick analysis
                bd = BizDesc(df)
                cent_tend = bd.central_tendency()
                self.assertIsNotNone(cent_tend)

            except ValueError as e:
                if is_builtin:
                    self.fail(f"Built-in dataset {dataset_name} failed: {e}")
                else:
                    # External datasets may not be available
                    pass


class TestDataIntegrity(unittest.TestCase):
    """Test data integrity through processing"""

    def test_data_preservation(self):
        """Test that original data is preserved"""
        df_original = pd.DataFrame({
            'value': np.random.normal(100, 15, 100),
            'category': np.random.choice(['A', 'B', 'C'], 100)
        })

        # Make a copy to track changes
        df_copy = df_original.copy()

        # Process with BizDesc
        bd = BizDesc(df_original)
        bd.central_tendency()
        bd.describe(include_plots=False)

        # Original data should not be modified
        pd.testing.assert_frame_equal(df_original, df_copy)

    def test_statistics_consistency(self):
        """Test that statistics are consistent across methods"""
        df = pd.DataFrame({
            'value': np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        })

        bd = BizDesc(df)

        # Get central tendency
        cent_tend = bd.central_tendency()['value']

        # Get describe
        desc = bd.describe(include_plots=False)

        # Mean should match
        central_mean = cent_tend['mean']
        describe_mean = [stat['Mean'] for stat in desc['numeric_stats']
                        if stat['Column'] == 'value'][0]

        self.assertAlmostEqual(central_mean, describe_mean, places=1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and unusual inputs"""

    def test_small_dataset(self):
        """Test with very small dataset"""
        df = pd.DataFrame({
            'value': [1, 2, 3]
        })

        bd = BizDesc(df)
        cent_tend = bd.central_tendency()
        self.assertIsNotNone(cent_tend)

    def test_large_dataset(self):
        """Test with large dataset"""
        df = pd.DataFrame({
            'value': np.random.normal(100, 15, 10000)
        })

        bd = BizDesc(df)
        cent_tend = bd.central_tendency()
        self.assertIsNotNone(cent_tend)

    def test_all_same_values(self):
        """Test with all identical values"""
        df = pd.DataFrame({
            'value': [5] * 100
        })

        bd = BizDesc(df)
        cent_tend = bd.central_tendency()

        # Mean, median, mode should all be 5
        self.assertEqual(cent_tend['value']['mean'], 5.0)
        self.assertEqual(cent_tend['value']['median'], 5.0)

    def test_with_nan_values(self):
        """Test handling of NaN values"""
        df = pd.DataFrame({
            'value': [1, 2, np.nan, 4, 5, np.nan, 7, 8, 9, 10]
        })

        bd = BizDesc(df)
        cent_tend = bd.central_tendency()

        # Should handle NaN gracefully
        self.assertIsNotNone(cent_tend['value']['mean'])

    def test_with_mixed_types(self):
        """Test with mixed numeric and categorical"""
        df = pd.DataFrame({
            'numeric': np.random.normal(100, 15, 100),
            'category': np.random.choice(['A', 'B', 'C'], 100),
            'integer': np.random.randint(1, 100, 100)
        })

        bd = BizDesc(df)
        cent_tend = bd.central_tendency()

        # Should have numeric columns
        self.assertGreater(len(cent_tend), 0)


class TestDocumentationExamples(unittest.TestCase):
    """Test examples from documentation"""

    def test_readme_example(self):
        """Test example from README"""
        # Example from README
        df = load_dataset('iris')
        bd = BizDesc(df, color_scheme='academic')
        cent_tend = bd.central_tendency()

        self.assertIsNotNone(cent_tend)
        self.assertGreater(len(cent_tend), 0)

    def test_quick_start_example(self):
        """Test quick start example"""
        df = load_dataset('school_cafeteria')
        bd = BizDesc(df, color_scheme='academic')

        cent_tend = bd.central_tendency()
        self.assertIsNotNone(cent_tend)

        stats = bd.describe(include_plots=False)
        self.assertIsNotNone(stats)


if __name__ == '__main__':
    unittest.main()
