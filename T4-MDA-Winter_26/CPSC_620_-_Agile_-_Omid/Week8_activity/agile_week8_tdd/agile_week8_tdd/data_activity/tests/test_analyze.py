"""
Tests for the analyze module.

All tests are skeleton functions that students must complete.
Students should implement the test logic for each function.
"""

import pytest
import pandas as pd
from data_pipeline.analyze import (
    calculate_basic_stats,
    count_by_category,
    filter_by_condition,
    calculate_correlation
)


@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'sepal_length': [5.1, 4.9, 4.7, 4.6, 5.0],
        'sepal_width': [3.5, 3.0, 3.2, 3.1, 3.6],
        'petal_length': [1.4, 1.4, 1.3, 1.5, 1.4],
        'petal_width': [0.2, 0.2, 0.2, 0.2, 0.2],
        'species': ['Iris-setosa', 'Iris-setosa', 'Iris-setosa', 'Iris-setosa', 'Iris-setosa']
    })


def test_calculate_basic_stats():
    """
    Test calculate_basic_stats function.
    
    TODO: Create a DataFrame with numeric data, call calculate_basic_stats,
    and assert that the returned dictionary contains the expected keys
    (mean, median, std, min, max) with correct values.
    """
    df = pd.DataFrame({'sepal_length': [5.1, 4.9, 4.7, 4.6, 5.0]})
    stats = calculate_basic_stats(df, 'sepal_length')
    
    # TODO: Add assertions here
    assert 'mean' in stats
    assert 'median' in stats
    assert 'std' in stats
    assert 'min' in stats
    assert 'max' in stats
    assert stats['mean'] == pytest.approx(4.86, rel=1e-2)
    assert stats['min'] == 4.6
    assert stats['max'] == 5.1


def test_calculate_basic_stats_invalid_column():
    """
    Test calculate_basic_stats with invalid column name.
    
    TODO: Test that calculate_basic_stats raises a ValueError
    when given a column name that doesn't exist in the DataFrame.
    """
    df = pd.DataFrame({'Value': [10, 20, 30]})
    
    # TODO: Add test using pytest.raises to check for ValueError
    with pytest.raises(ValueError):
        calculate_basic_stats(df, 'NonExistentColumn')


def test_count_by_category():
    """
    Test count_by_category function.
    
    TODO: Create a DataFrame with categorical data, call count_by_category,
    and assert that the returned Series has the correct counts for each category.
    """
    df = pd.DataFrame({'species': ['Iris-setosa', 'Iris-versicolor', 'Iris-setosa', 'Iris-versicolor', 'Iris-setosa']})
    counts = count_by_category(df, 'species')
    
    # TODO: Add assertions here
    assert isinstance(counts, pd.Series)
    assert counts['Iris-setosa'] == 3
    assert counts['Iris-versicolor'] == 2


def test_filter_by_condition_greater_than():
    """
    Test filter_by_condition with '>' operator.
    
    TODO: Create a DataFrame, filter it using '>' condition,
    and assert that all filtered rows meet the condition.
    """
    df = pd.DataFrame({'sepal_length': [5.1, 4.9, 4.7, 4.6, 5.0]})
    result = filter_by_condition(df, 'sepal_length', '>', 4.8)
    
    # TODO: Add assertions here
    assert len(result) == 3
    assert all(result['sepal_length'] > 4.8)


def test_filter_by_condition_equals():
    """
    Test filter_by_condition with '==' operator.
    
    TODO: Create a DataFrame, filter it using '==' condition,
    and assert that all filtered rows have the exact value.
    """
    df = pd.DataFrame({'species': ['Iris-setosa', 'Iris-versicolor', 'Iris-setosa', 'Iris-versicolor']})
    result = filter_by_condition(df, 'species', '==', 'Iris-setosa')
    
    # TODO: Add assertions here
    assert len(result) == 2
    assert all(result['species'] == 'Iris-setosa')


def test_calculate_correlation():
    """
    Test calculate_correlation function.
    
    TODO: Create a DataFrame with two numeric columns that have a known correlation,
    call calculate_correlation, and assert that the result is a float and within
    the expected range (-1.0 to 1.0).
    """
    df = pd.DataFrame({
        'sepal_length': [5.1, 4.9, 4.7, 4.6, 5.0],
        'petal_length': [1.4, 1.4, 1.3, 1.5, 1.4]
    })
    correlation = calculate_correlation(df, 'sepal_length', 'petal_length')
    
    # TODO: Add assertions here
    assert isinstance(correlation, float)
    assert -1.0 <= correlation <= 1.0
    # For iris data, sepal_length and petal_length should have positive correlation
    assert correlation > 0

