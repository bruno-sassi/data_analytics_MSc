"""
Data Cleaning Module

This module handles cleaning and preprocessing of the data.
Students should complete the TODO sections to handle missing values,
data type conversions, and other cleaning tasks.
"""

import pandas as pd


def handle_missing_values(df, strategy='drop'):
    """
    Handle missing values in the DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to clean
        strategy (str): Strategy to use - 'drop' to remove rows with missing values,
                       'fill_zero' to fill with 0, 'fill_mean' to fill numeric columns with mean
        
    Returns:
        pd.DataFrame: The cleaned DataFrame
    """
    # TODO: Implement the missing value handling based on the strategy parameter
    # If strategy is 'drop', use df.dropna() to remove rows with any missing values
    # If strategy is 'fill_zero', use df.fillna(0) to fill missing values with 0
    # If strategy is 'fill_mean', fill numeric columns with their mean values
    #   (hint: use df.select_dtypes(include=['number']) to get numeric columns)
    
    if strategy == 'drop':
        df_cleaned = df.dropna()
    elif strategy == 'fill_zero':
        df_cleaned = df.fillna(0)
    elif strategy == 'fill_mean':
        df_cleaned = df.copy()
        numeric_cols = df_cleaned.select_dtypes(include=['number']).columns
        df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].mean())
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    return df_cleaned


def standardize_column_names(df):
    """
    Standardize column names to lowercase with underscores.
    
    Args:
        df (pd.DataFrame): The DataFrame with potentially inconsistent column names
        
    Returns:
        pd.DataFrame: DataFrame with standardized column names
    """
    # TODO: Convert all column names to lowercase
    # Replace any spaces with underscores
    # Return the DataFrame with renamed columns
    # Hint: use df.rename() with a dictionary or df.columns.str methods
    
    pass


def convert_to_numeric(df, columns=None):
    """
    Convert specified columns to numeric type, coercing errors to NaN.
    
    Args:
        df (pd.DataFrame): The DataFrame to process
        columns (list, optional): List of column names to convert. If None, convert all columns.
        
    Returns:
        pd.DataFrame: DataFrame with converted columns
    """
    # TODO: If columns is None, convert all columns to numeric
    # If columns is provided, convert only those columns
    # Use pd.to_numeric() with errors='coerce' to handle conversion errors
    # Return the modified DataFrame
    
    df_converted = df.copy()
    if columns is None:
        for col in df_converted.columns:
            df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
    else:
        for col in columns:
            if col in df_converted.columns:
                df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
    return df_converted


def remove_duplicates(df):
    """
    Remove duplicate rows from the DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to process
        
    Returns:
        pd.DataFrame: DataFrame with duplicates removed
    """
    # TODO: Use df.drop_duplicates() to remove duplicate rows
    # Return the cleaned DataFrame
    
    return df.drop_duplicates()

