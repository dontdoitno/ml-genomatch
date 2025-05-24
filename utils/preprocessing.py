# Dictionary for column name standardization
rename_dict = {
    # Диагноз
    'Hemaological Diagnosis': 'diagnosis',
    'genotype': 'diagnosis',
    'disease': 'diagnosis',
    'Diagnosis': 'diagnosis',
    'Indication for  BMT': 'diagnosis',

    # Статус заболевания
    'disgrade': 'disease_status',
    'Disease Status': 'disease_status',
    'Status': 'disease_status',

    # Возраст пациента
    'R_Age at BMT': 'patient_age',
    'recipient_age': 'patient_age',
    'age': 'patient_age',
    'Age': 'patient_age',
    'R_Age': 'patient_age',

    # Пол пациента
    'R_Sex': 'patient_sex',
    'recipient_gender': 'patient_sex',
    'sex': 'patient_sex',
    'Sex': 'patient_sex',
    'Gender': 'patient_sex',

    # Этническая принадлежность пациента
    'Nationality': 'patient_ethnicity',
    'ethgp': 'patient_ethnicity',
    'Ethnicity': 'patient_ethnicity',
    'Race': 'patient_ethnicity',

    # Родственные связи пациента с донором
    'D_relation': 'donor_relation',
    'donorgp': 'donor_relation',
    'Donor Relation': 'donor_relation',
    'Relation': 'donor_relation',

    # Пол донора
    'D_sex': 'donor_sex',
    'Donor Sex': 'donor_sex',
    'Donor Gender': 'donor_sex',

    # Соответствие HLA
    'HLA match': 'hla_match_score',
    'HLA_match': 'hla_match_score',
    'hla_match': 'hla_match_score',
    'HLA Match': 'hla_match_score',
    'NEW HLA': 'hla_match_score',

    # Источник стволовых клеток
    'stem_cell_source': 'source_of_cells',
    'graftype': 'source_of_cells',
    'Graft Type': 'source_of_cells',
    'Source': 'source_of_cells',

    # Режим лечения
    'condint': 'conditioning_regimen',
    'Conditioning': 'conditioning_regimen',
    'Regimen': 'conditioning_regimen',

    # Профилактика ГВП
    'GVHD Prophylaxis': 'gvhd_prophylaxis',
    'gvhdgp': 'gvhd_prophylaxis',
    'Prophylaxis': 'gvhd_prophylaxis',

    # Доза CD34
    'CD34_x1e6_per_kg': 'cd34_dose',
    'CD34 Dose': 'cd34_dose',
    'CD34': 'cd34_dose',

    # Время от диагноза до трансплантации
    'Diagnosis to BMT time months': 'days_from_diagnosis_to_hct',
    'indxtx2': 'days_from_diagnosis_to_hct',
    'Time to Transplant': 'days_from_diagnosis_to_hct',

    # Выздоровление
    'GVHD ': 'engraftment_success',
    'ANC_recovery': 'engraftment_success',
    'anc': 'engraftment_success',
    'Engraftment': 'engraftment_success',

    # Время до выздоровления
    'time_to_ANC_recovery': 'engraftment_days',
    'intxanc': 'engraftment_days',
    'Time to Engraftment': 'engraftment_days',

    # Степень острого ГВП
    'GVHD severity ': 'acute_gvhd_grade',
    'agvhd24': 'acute_gvhd_grade',
    'acute_GvHD_II_III_IV': 'acute_gvhd_grade',
    'Acute GVHD': 'acute_gvhd_grade',

    # Хронический ГВП
    'extensive_chronic_GvHD': 'chronic_gvhd',
    'cgvhd': 'chronic_gvhd',
    'Chronic GVHD': 'chronic_gvhd',

    # Выживаемость
    'DEAD/Y/N': 'overall_survival_1y',
    'survival_status': 'overall_survival_1y',
    'dead': 'overall_survival_1y',
    'Survival': 'overall_survival_1y',

    # Рецидив
    'rel': 'relapse',
    'Relapse': 'relapse',
    'Disease Relapse': 'relapse',

    # Смертность, связанная с трансплантацией
    'trm': 'trm',
    'TRM': 'trm',
    'Transplant Related Mortality': 'trm'
}

def get_standard_columns() -> list:
    """
    Returns list of standardized column names from rename_dict
    """
    return sorted(list(set(rename_dict.values())))

def rename_columns(df):
    """
    Унифицирует названия столбцов датасета для дальнейшей работы.
    'как_есть': 'как_надо'
    """
    # Создаем словарь с ключами в нижнем регистре для нечувствительного к регистру сопоставления
    rename_dict_lower = {k.lower(): v for k, v in rename_dict.items()}

    # Получаем фактические названия колонок из датасета
    actual_columns = df.columns.tolist()

    # Создаем сопоставление фактических названий колонок с унифицированными
    final_mapping = {}
    for col in actual_columns:
        col_lower = col.lower()
        if col_lower in rename_dict_lower:
            final_mapping[col] = rename_dict_lower[col_lower]
        elif col in rename_dict:
            final_mapping[col] = rename_dict[col]

    # Переименовываем колонки
    df = df.rename(columns=final_mapping)

    return df
