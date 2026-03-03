"""
Tests for the ingest module.

Some tests are complete and working. Students should complete the TODO tests.
"""

import pytest
import pandas as pd
import os
from data_pipeline.ingest import read_csv_file, get_data_info, validate_dataframe


def test_read_csv_file_exists():
    """Test that read_csv_file can read an existing CSV file."""
    file_path = "../data/iris.csv"
    df = read_csv_file(file_path)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) > 0


def test_read_csv_file_not_exists():
    """Test that read_csv_file raises FileNotFoundError for non-existent file."""
    file_path = "data/nonexistent_file.csv"
    
    with pytest.raises(FileNotFoundError):
        read_csv_file(file_path)


def test_get_data_info():
    """Test that get_data_info returns correct structure."""
    file_path = "../data/iris.csv"
    df = read_csv_file(file_path)
    info = get_data_info(df)
    
    assert isinstance(info, dict)
    assert 'shape' in info
    assert 'columns' in info
    assert 'dtypes' in info
    assert isinstance(info['shape'], tuple)
    assert isinstance(info['columns'], list)
    assert isinstance(info['dtypes'], dict)


def test_get_data_info_shape():
    """Test that get_data_info returns correct shape."""
    file_path = "../data/iris.csv"
    df = read_csv_file(file_path)
    info = get_data_info(df)
    
    # TODO: Assert that info['shape'] matches df.shape
    # Add your assertion here


def test_validate_dataframe_valid():
    """Test validate_dataframe with a valid DataFrame."""
    file_path = "../data/iris.csv"
    df = read_csv_file(file_path)
    
    # TODO: Assert that validate_dataframe returns True for a valid DataFrame
    assert validate_dataframe(df) == True


def test_validate_dataframe_empty():
    """Test validate_dataframe with an empty DataFrame."""
    empty_df = pd.DataFrame()
    
    # TODO: Assert that validate_dataframe returns False for an empty DataFrame
    assert validate_dataframe(empty_df) == False

