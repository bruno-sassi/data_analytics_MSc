"""
Data Ingestion Module

This module handles reading data from CSV files and loading it into a pandas DataFrame.
Students should complete the TODO sections.
"""

import pandas as pd
import os


def read_csv_file(file_path):
    """
    Read a CSV file and return it as a pandas DataFrame.
    
    Args:
        file_path (str): Path to the CSV file to read
        
    Returns:
        pd.DataFrame: The loaded data as a DataFrame
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file cannot be read as CSV
    """
    # TODO: Check if the file exists using os.path.exists()
    # If it doesn't exist, raise a FileNotFoundError with a descriptive message
    
    # TODO: Use pandas.read_csv() to read the file
    # Return the DataFrame
    
    # Partial implementation provided:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # TODO: Complete the read_csv call below
    df = pd.read_csv(file_path)
    return df


def get_data_info(df):
    """
    Get basic information about the DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze
        
    Returns:
        dict: A dictionary containing:
            - 'shape': tuple of (rows, columns)
            - 'columns': list of column names
            - 'dtypes': dictionary of column names to data types
    """
    # TODO: Return a dictionary with:
    # - 'shape': the shape of the DataFrame (use df.shape)
    # - 'columns': list of column names (use df.columns.tolist())
    # - 'dtypes': dictionary mapping column names to their data types (use df.dtypes.to_dict())
    
    info = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict()
    }
    return info


def validate_dataframe(df):
    """
    Validate that the DataFrame is not empty and has at least one column.
    
    Args:
        df (pd.DataFrame): The DataFrame to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # TODO: Check if the DataFrame is empty (no rows or no columns)
    # Return False if empty, True otherwise
    
    pass

