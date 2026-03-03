"""
Tests for the clean module.

Some tests are complete and working. Students should complete the TODO tests.
"""

import pytest
import pandas as pd
import numpy as np
from data_pipeline.clean import (
    handle_missing_values,
    standardize_column_names,
    convert_to_numeric,
    remove_duplicates
)


@pytest.fixture
def sample_df():
    """Create a sample DataFrame with missing values for testing."""
    return pd.DataFrame({
        'sepal_length': [5.1, 4.9, None, 4.6],
        'sepal_width': [3.5, 3.0, None, 3.1],
        'petal_length': [1.4, None, 1.3, 1.5],
        'species': ['Iris-setosa', 'Iris-setosa', 'Iris-versicolor', 'Iris-setosa']
    })


def test_handle_missing_values_drop(sample_df):
    """Test handle_missing_values with 'drop' strategy."""
    result = handle_missing_values(sample_df, strategy='drop')
    
    assert result.isna().sum().sum() == 0
    assert len(result) < len(sample_df)


def test_handle_missing_values_fill_zero(sample_df):
    """Test handle_missing_values with 'fill_zero' strategy."""
    result = handle_missing_values(sample_df, strategy='fill_zero')
    
    # TODO: Assert that there are no missing values in the result
    # TODO: Check that numeric columns have 0 where there were missing values
    # Add your assertions here


def test_standardize_column_names():
    """Test standardize_column_names converts names to lowercase."""
    df = pd.DataFrame({
        'Sepal Length': [5.1, 4.9, 4.7],
        'Petal Width': [0.2, 0.2, 0.2],
        'Species Name': ['Iris-setosa', 'Iris-setosa', 'Iris-setosa']
    })
    
    result = standardize_column_names(df)
    
    # TODO: Assert that all column names are lowercase
    # TODO: Assert that spaces are replaced with underscores
    assert all(col.islower() for col in result.columns)
    assert 'sepal_length' in result.columns
    assert 'petal_width' in result.columns
    assert 'species_name' in result.columns


def test_convert_to_numeric_specific_columns():
    """Test convert_to_numeric with specific columns."""
    df = pd.DataFrame({
        'species': ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'],
        'sepal_length': ['5.1', '4.9', '4.7'],
        'petal_width': ['0.2', '0.2', '0.2']
    })
    
    result = convert_to_numeric(df, columns=['sepal_length', 'petal_width'])
    
    # TODO: Assert that 'sepal_length' and 'petal_width' columns are numeric
    # TODO: Assert that 'species' column is still string type
    assert pd.api.types.is_numeric_dtype(result['sepal_length'])
    assert pd.api.types.is_numeric_dtype(result['petal_width'])
    assert result['species'].dtype == 'object'


def test_remove_duplicates():
    """Test remove_duplicates removes duplicate rows."""
    df = pd.DataFrame({
        'sepal_length': [5.1, 4.9, 5.1, 4.6],
        'sepal_width': [3.5, 3.0, 3.5, 3.1],
        'species': ['Iris-setosa', 'Iris-setosa', 'Iris-setosa', 'Iris-setosa']
    })
    
    result = remove_duplicates(df)
    
    # TODO: Assert that the result has fewer or equal rows than the original
    # TODO: Assert that there are no duplicate rows in the result
    # Add your assertions here

