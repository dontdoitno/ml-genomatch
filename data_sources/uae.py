import pandas as pd
import numpy as np
from utils.preprocessing import rename_columns
from utils.converters import yes_no_to_numbers, convert_hla_match
from utils.constants import (
    SEX_MAP,
    DIAGNOSIS_MAP,
    SOURCE_OF_CELLS_MAP,
    DONOR_RELATION_MAP,
    DISEASE_STATUS_MAP,
    PATIENT_ETHNICITY_MAP,
    CONDITIONING_REGIMEN_MAP,
    GVHD_PROPHYLAXIS_MAP,
)
from utils.validate_dataframe import validate_dataframe, print_validation_results


def load_raw() -> pd.DataFrame:
    """
    Loads data from Excel file
    """
    try:
        path = "raw_datasets/uae.xlsx"
        df = pd.read_excel(path, sheet_name="Origional Data")
        return df
    except Exception as e:
        raise Exception(f"Error loading UAE dataset: {str(e)}")


def preprocess_data() -> pd.DataFrame:
    """
    Preprocesses the UAE dataset
    """
    try:
        # Load raw data
        df = load_raw()

        # Clean column names - remove extra whitespace
        df.columns = [col.strip() for col in df.columns]

        # Replace unknown values with NaN
        unknown_values = ['Unknown', 'unknown', 'UNKNOWN', '99', 99, '99.', 99., 'N/A', 'NA', 'Not Available', 'Not Specified', '']
        df = df.replace(unknown_values, np.nan)

        # Rename columns to standard names
        df = rename_columns(df)

        # Define column-to-mapping dictionary
        categorical_maps = {
            'diagnosis': DIAGNOSIS_MAP,
            'disease_status': DISEASE_STATUS_MAP,
            'patient_sex': SEX_MAP,
            'donor_sex': SEX_MAP,
            'donor_relation': DONOR_RELATION_MAP,
            'source_of_cells': SOURCE_OF_CELLS_MAP,
            'conditioning_regimen': CONDITIONING_REGIMEN_MAP,
            'gvhd_prophylaxis': GVHD_PROPHYLAXIS_MAP,
            'patient_ethnicity': PATIENT_ETHNICITY_MAP
        }

        # Apply mapping
        for col, mapping in categorical_maps.items():
            if col in df.columns:
                # Convert to string type first
                df[col] = df[col].astype(str)
                # Handle NaN values
                df[col] = df[col].replace('nan', '')
                df[col] = df[col].str.strip()
                df[col] = df[col].replace('', np.nan)
                # Apply mapping
                df[col] = df[col].map(mapping)

        # Convert binary values
        binary_columns = [
            'engraftment_success',
            'acute_gvhd_grade',
            'chronic_gvhd',
            'overall_survival_1y',
            'relapse',
            'trm'
        ]

        for col in binary_columns:
            if col in df.columns:
                # Convert to string type first
                df[col] = df[col].astype(str)
                # Handle NaN values
                df[col] = df[col].replace('nan', '')
                df[col] = df[col].str.strip()
                df[col] = df[col].replace('', np.nan)
                # Apply conversion
                df[col] = df[col].apply(yes_no_to_numbers)

        # Convert HLA match score
        if 'hla_match_score' in df.columns:
            # Convert to string type first
            df['hla_match_score'] = df['hla_match_score'].astype(str)
            # Handle NaN values
            df['hla_match_score'] = df['hla_match_score'].replace('nan', '')
            df['hla_match_score'] = df['hla_match_score'].str.strip()
            df['hla_match_score'] = df['hla_match_score'].replace('', np.nan)
            # Apply conversion
            df['hla_match_score'] = df['hla_match_score'].apply(convert_hla_match)

        # Convert numeric columns
        numeric_columns = [
            'patient_age',
            'donor_age',
            'days_from_diagnosis_to_hct',
            'engraftment_days',
            'cd34_dose'
        ]

        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Validate the processed dataframe
        validation_issues = validate_dataframe(df)
        print_validation_results(validation_issues)

        return df

    except Exception as e:
        raise Exception(f"Error in preprocessing UAE dataset: {str(e)}")
