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
    ACUTE_GVHD_GRADE_MAP,
)

def load_raw_data() -> pd.DataFrame:
    """
    Загружает данные из файла .csv
    """
    df = pd.read_csv('raw_datasets/bone-marrow-dataset.csv')
    return df


def preprocess_data() -> pd.DataFrame:
    """
    Preprocesses the Bone Marrow dataset
    """
    try:
        # Load raw data
        df = pd.read_csv('raw_datasets/bone-marrow-dataset.csv')

        # Replace unknown values with NaN
        df = df.replace(['Unknown', 'unknown', 'UNKNOWN', '99', 99, '99.', 99., 'N/A', 'NA', 'Not Available', 'Not Specified'], np.nan)

        # Rename columns to standard names
        df = rename_columns(df)

        # Map categorical values
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

        for col, mapping in categorical_maps.items():
            if col in df.columns:
                # Convert to string and handle NaN values
                df[col] = df[col].fillna('').astype(str)
                df[col] = df[col].str.strip()
                # Replace empty strings with NaN
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
                # Convert to string and handle NaN values
                df[col] = df[col].fillna('').astype(str)
                df[col] = df[col].str.strip()
                # Replace empty strings with NaN
                df[col] = df[col].replace('', np.nan)
                # Apply conversion
                df[col] = df[col].apply(yes_no_to_numbers)

        # Convert HLA match score
        if 'hla_match_score' in df.columns:
            # Convert to string and handle NaN values
            df['hla_match_score'] = df['hla_match_score'].fillna('').astype(str)
            df['hla_match_score'] = df['hla_match_score'].str.strip()
            # Replace empty strings with NaN
            df['hla_match_score'] = df['hla_match_score'].replace('', np.nan)
            # Apply conversion
            df['hla_match_score'] = df['hla_match_score'].apply(convert_hla_match)

        # Convert numeric columns
        numeric_columns = [
            'patient_age',
            'days_from_diagnosis_to_hct',
            'engraftment_days',
            'cd34_dose'
        ]

        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    except Exception as e:
        raise Exception(f"Error in preprocessing Bone Marrow dataset: {str(e)}")
