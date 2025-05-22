def rename_columns(df):
    """
    Унифицирует названия столбцов датасета для дальнейшей работы.
    'как_надо': 'как_есть'
    """
    rename_dict = {
        'diagnosis': 'diagnosis',
        'diagnosis': 'Hemaological Diagnosis',
        'diagnosis': 'genotype',
        'diagnosis': 'disease',

        'disease_status': 'disease_status',
        'disease_status': 'disgrade',

        'patient_age': 'age_patient',
        'patient_age': 'R_Age at BMT',
        'patient_age': 'recipient_age',
        'patient_age': 'age',

        'patient_sex': 'sex_patient',
        'patient_sex': 'R_Sex',
        'patient_sex': 'recipient_gender',
        'patient_sex': 'sex',

        'patient_ethnicity': 'ethnicity_patient',
        'patient_ethnicity': 'Nationality',
        'patient_ethnicity': 'ethgp',

        'donor_relation': 'relation_donor',
        'donor_relation': 'D_relation',
        'donor_relation': 'donorgp',

        'donor_age': 'age_donor',

        'donor_sex': 'sex_donor',
        'donor_sex': 'D_sex',

        'donor_ethnicity': 'ethnicity_donor',

        'hla_match_score': 'hla_score',
        'hla_match_score': 'HLA match',
        'hla_match_score': 'HLA_match',
        'hla_match_score': 'hla_match',

        'source_of_cells': 'source_cells',
        'source_of_cells': 'stem_cell_source',
        'source_of_cells': 'graftype',

        'conditioning_regimen': 'conditioning',
        'conditioning_regimen': 'condint',

        'gvhd_prophylaxis': 'gvhd_prophylaxis',
        'gvhd_prophylaxis': 'GVHD Prophylaxis',
        'gvhd_prophylaxis': 'gvhdgp',

        'cd34_dose': 'cd34_dose',
        'cd34_dose': 'CD34_x1e6_per_kg',

        'days_from_diagnosis_to_hct': 'days_to_hct',
        'days_from_diagnosis_to_hct': 'Diagnosis to BMT time months',
        'days_from_diagnosis_to_hct': 'indxtx2',

        'engraftment_success': 'engraftment_success',
        'engraftment_success': 'GVHD ',
        'engraftment_success': 'ANC_recovery',
        'engraftment_success': 'anc',

        'engraftment_days': 'engraftment_days',
        'engraftment_days': 'time_to_ANC_recovery',
        'engraftment_days': 'intxanc',

        'acute_gvhd_grade': 'acute_gvhd',
        'acute_gvhd_grade': 'GVHD severity ',
        'acute_gvhd_grade': 'agvhd24',
        'acute_gvhd_grade': 'acute_GvHD_II_III_IV',

        'chronic_gvhd': 'chronic_gvhd',
        'chronic_gvhd': 'extensive_chronic_GvHD',
        'chronic_gvhd': 'cgvhd',

        'overall_survival_1y': 'survival_1y',
        'overall_survival_1y': 'DEAD/Y/N',
        'overall_survival_1y': 'survival_status',
        'overall_survival_1y': 'dead',

        'relapse': 'relapse',
        'relapse': 'rel',

        'trm': 'trm',
    }

    return df.rename(columns=rename_dict)
