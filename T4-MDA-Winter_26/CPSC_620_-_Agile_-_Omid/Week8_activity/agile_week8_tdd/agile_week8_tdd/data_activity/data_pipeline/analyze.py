"""
Data Analysis Module

This module provides functions for analyzing the cleaned data.
Students should complete the TODO sections to implement statistical analysis functions.
"""

import pandas as pd


def calculate_basic_stats(df, column):
    """
    Calculate basic statistics for a numeric column.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze
        column (str): Name of the column to analyze
        
    Returns:
        dict: Dictionary containing mean, median, std, min, max
    """
    # TODO: Calculate and return a dictionary with:
    # - 'mean': mean value of the column
    # - 'median': median value of the column
    # - 'std': standard deviation of the column
    # - 'min': minimum value of the column
    # - 'max': maximum value of the column
    # Use df[column] to access the column and pandas methods like .mean(), .median(), etc.
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    pass


def count_by_category(df, column):
    """
    Count occurrences of each value in a categorical column.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze
        column (str): Name of the categorical column
        
    Returns:
        pd.Series: Series with value counts (index = values, values = counts)
    """
    # TODO: Use df[column].value_counts() to count occurrences of each value
    # Return the resulting Series
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    return df[column].value_counts()


def filter_by_condition(df, column, condition, value):
    """
    Filter DataFrame rows based on a condition.
    
    Args:
        df (pd.DataFrame): The DataFrame to filter
        column (str): Name of the column to filter on
        condition (str): Condition operator - '>', '<', '==', '>=', '<=', '!='
        value: Value to compare against
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    # TODO: Implement filtering based on the condition
    # Use comparison operators to create a boolean mask
    # Apply the mask to the DataFrame using df[mask]
    # Return the filtered DataFrame
    # Hint: You can use eval() or if/elif statements to handle different conditions
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    if condition == '>':
        mask = df[column] > value
    elif condition == '<':
        mask = df[column] < value
    elif condition == '==':
        mask = df[column] == value
    elif condition == '>=':
        mask = df[column] >= value
    elif condition == '<=':
        mask = df[column] <= value
    elif condition == '!=':
        mask = df[column] != value
    else:
        raise ValueError(f"Unknown condition: {condition}")
    
    return df[mask]


def calculate_correlation(df, column1, column2):
    """
    Calculate correlation between two numeric columns.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze
        column1 (str): Name of the first column
        column2 (str): Name of the second column
        
    Returns:
        float: Correlation coefficient between the two columns
    """
    # TODO: Use pandas correlation method to calculate correlation between two columns
    # Return the correlation value as a float
    # Hint: df[column1].corr(df[column2])
    
    if column1 not in df.columns or column2 not in df.columns:
        raise ValueError(f"One or both columns not found in DataFrame")
    
    return df[column1].corr(df[column2])

