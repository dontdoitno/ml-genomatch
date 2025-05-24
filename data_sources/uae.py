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
        print(f"Loading UAE dataset from {path}")
        df = pd.read_excel(path, sheet_name="Origional Data")
        print(f"Loaded dataset with shape: {df.shape}")
        print("Columns:", df.columns.tolist())
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
        print("\nCleaning column names...")
        df.columns = [str(col).strip() for col in df.columns]
        print("Cleaned columns:", df.columns.tolist())

        # Replace unknown values with NaN
        print("\nReplacing unknown values...")
        unknown_values = ['Unknown', 'unknown', 'UNKNOWN', '99', 99, '99.', 99., 'N/A', 'NA', 'Not Available', 'Not Specified', '']
        df = df.replace(unknown_values, np.nan)
        print("Sample of data after replacing unknown values:")
        print(df.head())

        # Create column mapping dictionary
        column_mapping = {
            'R_Sex': 'patient_sex',
            'Age': 'patient_age',
            'Nationality': 'patient_ethnicity',
            'Hemaological Diagnosis': 'diagnosis',
            'Diagnosis to BMT time months': 'days_from_diagnosis_to_hct',
            'R_Age at BMT': 'patient_age',
            'HLA match': 'hla_match_score',
            'NEW HLA': 'hla_match_score',
            'D_relation': 'donor_relation',
            'D_sex': 'donor_sex',
            'GVHD Prophylaxis': 'gvhd_prophylaxis',
            'GVHD': 'chronic_gvhd',
            'GVHD Acute/Chronic': 'acute_gvhd_grade',
            'GVHD severity': 'acute_gvhd_grade',
            'DEAD/Y/N': 'overall_survival_1y'
        }

        # Rename columns
        print("\nRenaming columns...")
        df = df.rename(columns=column_mapping)
        print("Renamed columns:", df.columns.tolist())

        # Handle duplicate columns by keeping the first occurrence
        df = df.loc[:, ~df.columns.duplicated()]

        # Convert numeric columns first
        print("\nConverting numeric columns...")
        numeric_columns = [
            'patient_age',
            'donor_age',
            'days_from_diagnosis_to_hct',
            'engraftment_days',
            'cd34_dose',
            'hla_match_score'  # Keep as numeric
        ]

        for col in numeric_columns:
            if col in df.columns:
                print(f"Converting {col} to numeric...")
                try:
                    # First convert to string to handle any non-string values
                    df[col] = df[col].astype(str)
                    # Replace any non-numeric strings with NaN
                    df[col] = df[col].replace(['nan', 'NaN', 'NULL', 'null', '', ' '], np.nan)
                    # Convert to numeric
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    print(f"{col} unique values:", df[col].dropna().unique())
                except Exception as e:
                    print(f"Error converting {col}: {str(e)}")
                    print(f"Column type: {df[col].dtype}")
                    print(f"Sample values: {df[col].head()}")

        # Define column-to-mapping dictionary
        print("\nProcessing categorical columns...")
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

        # Apply mapping for categorical columns
        for col, mapping in categorical_maps.items():
            if col in df.columns:
                print(f"\nProcessing {col}...")
                print(f"Before processing - unique values:", df[col].dropna().unique())
                # Convert values to strings and clean them
                df[col] = df[col].fillna('')
                df[col] = df[col].map(lambda x: str(x).strip() if pd.notnull(x) else '')
                df[col] = df[col].replace('', np.nan)
                # Apply mapping
                df[col] = df[col].map(mapping)
                print(f"After processing - unique values:", df[col].dropna().unique())

        # Convert binary values
        print("\nProcessing binary columns...")
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
                print(f"\nProcessing {col}...")
                print(f"Before processing - unique values:", df[col].dropna().unique())
                # Convert values to strings and clean them
                df[col] = df[col].fillna('')
                df[col] = df[col].map(lambda x: str(x).strip() if pd.notnull(x) else '')
                df[col] = df[col].replace('', np.nan)
                # Apply conversion
                df[col] = df[col].map(yes_no_to_numbers)
                print(f"After processing - unique values:", df[col].dropna().unique())

        print("\nFinal dataset shape:", df.shape)
        print("Final columns:", df.columns.tolist())
        print("\nSample of final data:")
        print(df.head())

        # Validate the processed dataframe
        validation_issues = validate_dataframe(df)
        print_validation_results(validation_issues)

        return df

    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print("Error type:", type(e))
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
        raise Exception(f"Error in preprocessing UAE dataset: {str(e)}")
