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
    Preprocesses the P5303 dataset
    """
    try:
        # Load raw data
        df = pd.read_sas('raw_datasets/p5303.sas7bdat')

        # Replace unknown values with NaN
        df = df.replace([99, 99., '99', '99.', 'Unknown', 'unknown', 'UNKNOWN', 'N/A', 'NA', 'Not Available', 'Not Specified'], np.nan)

        # Map raw column names to standard names
        column_mapping = {
            'yeartx': 'transplant_year',
            'sex': 'patient_sex',
            'age': 'patient_age',
            'graftype': 'source_of_cells',
            'ragecat': 'recipient_age_category',
            'gvhdgp': 'gvhd_prophylaxis',
            'ethgp': 'patient_ethnicity',
            'kps': 'karnofsky_score',
            'invivo_tcd': 'in_vivo_tcell_depletion',
            'indxtx2': 'days_from_diagnosis_to_hct',
            'intxsurv': 'time_to_survival',
            'anc': 'engraftment_success',
            'intxanc': 'engraftment_days',
            'platelet': 'platelet_count',
            'intxplatelet': 'time_to_platelet_recovery',
            'agvhd24': 'acute_gvhd_grade',
            'intxagvhd24': 'time_to_acute_gvhd',
            'agvhd34': 'acute_gvhd_grade_34',
            'intxagvhd34': 'time_to_acute_gvhd_34',
            'cgvhd': 'chronic_gvhd',
            'intxcgvhd': 'time_to_chronic_gvhd',
            'rel': 'relapse',
            'intxrel': 'time_to_relapse',
            'condreg': 'conditioning_regimen',
            'yrgrp': 'year_group',
            'd_haplotypes_num': 'donor_haplotypes_number',
            'd_cen_regions_num': 'donor_centromeric_regions_number',
            'd_tel_regions_num': 'donor_telomeric_regions_number',
            'd_B_Content_alt': 'donor_b_content_alternative',
            'd_score_B_Content_ranking_num': 'donor_b_content_ranking_score',
            'kir_composite_score': 'kir_composite_score',
            'd_2DS1_NEW': 'donor_2ds1_new',
            'd_b_content': 'donor_b_content',
            'hla_match': 'hla_match_score',
            'disease': 'diagnosis',
            'disgrade': 'disease_status',
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
            'hla_match_score',  # Keep as numeric
            'karnofsky_score',
            'platelet_count',
            'time_to_platelet_recovery',
            'time_to_acute_gvhd',
            'time_to_acute_gvhd_34',
            'time_to_chronic_gvhd',
            'time_to_relapse',
            'donor_haplotypes_number',
            'donor_centromeric_regions_number',
            'donor_telomeric_regions_number',
            'donor_b_content_ranking_score',
            'kir_composite_score',
            'donor_b_content'
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
        raise Exception(f"Error in preprocessing P5303 dataset: {str(e)}")
