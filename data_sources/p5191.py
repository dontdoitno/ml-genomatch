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

def preprocess_data() -> pd.DataFrame:
    """
    Preprocesses the P5191 dataset
    """
    try:
        # Load raw data
        df = pd.read_sas('raw_datasets/p5191.sas7bdat')

        # Replace unknown values with NaN
        df = df.replace([99, 99., '99', '99.', 'Unknown', 'unknown', 'UNKNOWN', 'N/A', 'NA', 'Not Available', 'Not Specified'], np.nan)

        # Map raw column names to standard names
        column_mapping = {
            'sex': 'patient_sex',
            'rcmv': 'recipient_cmv',
            'graftype': 'source_of_cells',
            'age': 'patient_age',
            'intxsurv': 'time_to_survival',
            'kps': 'karnofsky_score',
            'anc': 'engraftment_success',
            'intxanc': 'engraftment_days',
            'dwoanc': 'days_without_anc',
            'platelet': 'platelet_count',
            'intxplatelet': 'time_to_platelet_recovery',
            'dwoplatelet': 'days_without_platelets',
            'cgvhd': 'chronic_gvhd',
            'intxcgvhd': 'time_to_chronic_gvhd',
            'dwocgvhd': 'days_without_chronic_gvhd',
            'gf': 'graft_failure',
            'intxgf': 'time_to_graft_failure',
            'dwogf': 'days_without_graft_failure',
            'hctcigp': 'hct_ci_group',
            'condreg': 'conditioning_regimen',
            'atg': 'anti_thymocyte_globulin',
            'agvhd24': 'acute_gvhd_grade',
            'intxagvhd24': 'time_to_acute_gvhd',
            'dwoagvhd24': 'days_without_acute_gvhd',
            'secondary_malig': 'secondary_malignancy',
            'intx2malig': 'time_to_secondary_malignancy',
            'stroke': 'stroke',
            'acs': 'acute_coronary_syndrome',
            'hla_match': 'hla_match_score',
            'genotype': 'diagnosis',
            'donorgp': 'donor_relation',
            'gvhdgp': 'gvhd_prophylaxis',
            'dead': 'overall_survival_1y'
        }

        # Rename columns
        df = df.rename(columns=column_mapping)

        # Convert numeric columns first
        numeric_columns = [
            'patient_age',
            'donor_age',
            'days_from_diagnosis_to_hct',
            'engraftment_days',
            'cd34_dose',
            'hla_match_score',
            'karnofsky_score',
            'platelet_count',
            'time_to_platelet_recovery',
            'days_without_platelets',
            'time_to_chronic_gvhd',
            'days_without_chronic_gvhd',
            'time_to_graft_failure',
            'days_without_graft_failure',
            'time_to_acute_gvhd',
            'days_without_acute_gvhd',
            'time_to_secondary_malignancy'
        ]

        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

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
                # Convert numeric values to strings for mapping
                df[col] = df[col].fillna(-1).astype(int).astype(str)
                df[col] = df[col].replace('-1', np.nan)
                # Create reverse mapping for numeric values
                reverse_mapping = {str(int(float(k))): v for k, v in mapping.items() if k.replace('.', '').isdigit()}
                df[col] = df[col].replace(reverse_mapping)

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
                df[col] = df[col].fillna(-1).astype(int)
                df[col] = df[col].replace(-1, np.nan)
                df[col] = df[col].apply(yes_no_to_numbers)

        return df

    except Exception as e:
        raise Exception(f"Error in preprocessing P5191 dataset: {str(e)}")
