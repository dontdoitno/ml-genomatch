import pandas as pd
import numpy as np
from typing import List

def validate_dataframe(df: pd.DataFrame) -> List[str]:
    """
    Validates the dataframe for data quality issues
    Returns a list of validation issues found
    """
    issues = []

    # Проверяем наличие необходимых колонок
    required_columns = {
        'patient_age', 'donor_age', 'patient_sex', 'donor_sex',
        'diagnosis', 'disease_status', 'source_of_cells',
        'donor_relation', 'hla_match_score', 'engraftment_success',
        'engraftment_days', 'acute_gvhd', 'chronic_gvhd',
        'relapse', 'survival'
    }

    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        issues.append(f"Missing required columns: {', '.join(missing_columns)}")

    # Проверяем категориальные значения
    valid_values = {
        'patient_sex': {'M', 'F'},
        'donor_sex': {'M', 'F'},
        'diagnosis': {'ALL', 'AML', 'CML', 'MDS', 'NHL', 'HL', 'MM', 'Other'},
        'disease_status': {'CR1', 'CR2', 'PR', 'Relapse', 'Refractory'},
        'source_of_cells': {'BM', 'PBSC', 'Cord'},
        'donor_relation': {'MRD', 'MUD', 'MMUD', 'Haplo'},
        'hla_match_score': {6, 7, 8, 9, 10}
    }

    for col, valid_set in valid_values.items():
        if col in df.columns:
            # Преобразуем в строку для сравнения
            values = df[col].astype(str).str.upper()
            invalid_values = set(values.dropna().unique()) - valid_set
            if invalid_values:
                issues.append(f"Invalid values in {col}: {', '.join(map(str, invalid_values))}")

    # Проверяем числовые значения
    numeric_ranges = {
        'patient_age': (0, 100),
        'donor_age': (0, 100),
        'engraftment_days': (0, 3650),
        'acute_gvhd_days': (0, 365),
        'chronic_gvhd_days': (0, 365),
        'relapse_days': (0, 3650),
        'survival_days': (0, 3650)
    }

    for col, (min_val, max_val) in numeric_ranges.items():
        if col in df.columns:
            try:
                # Преобразуем в числовые значения, преобразуя ошибки в NaN
                numeric_values = pd.to_numeric(df[col], errors='coerce')
                if not numeric_values.between(min_val, max_val).all():
                    issues.append(f"Values in {col} outside valid range [{min_val}, {max_val}]")
            except Exception as e:
                issues.append(f"Error validating {col}: {str(e)}")

    # Проверяем логику
    if 'engraftment_success' in df.columns and 'engraftment_days' in df.columns:
        # Преобразуем в числовые значения для сравнения
        engraftment_days = pd.to_numeric(df['engraftment_days'], errors='coerce')
        success_mask = df['engraftment_success'] == 1
        if not engraftment_days[success_mask].between(0, 100).all():
            issues.append("Invalid engraftment days for successful engraftments")

    return issues

def print_validation_results(issues: List[str]) -> None:
    """
    Prints validation results in a formatted way
    """
    if not issues:
        print("No validation issues found!")
        return

    print("\nValidation Issues:")
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")
