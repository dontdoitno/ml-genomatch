import pandas as pd

def validate_dataframe(df: pd.DataFrame) -> None:
    issues = []

    # Допустимые значения
    valid_values = {
        'diagnosis': {'AML', 'ALL', 'SCD', 'Thalassemia'},
        'disease_status': {'remission', 'active', 'relapse'},
        'patient_sex': {'M', 'F'},
        'patient_ethnicity': {'White', 'Black', 'Asian', 'Hispanic', 'Other'},
        'donor_relation': {'sibling', 'matched unrelated', 'parent'},
        'donor_sex': {'M', 'F'},
        'donor_ethnicity': {'White', 'Black', 'Asian', 'Hispanic', 'Other'},
        'source_of_cells': {'BM', 'PBSC', 'CB'},
        'conditioning_regimen': {'myeloablative', 'reduced intensity'},
        'gvhd_prophylaxis': {'CSA+MTX', 'Tac+MTX', 'Other'},
        'engraftment_success': {0, 1},
        'chronic_gvhd': {0, 1},
        'overall_survival_1y': {0, 1},
        'relapse': {0, 1},
        'trm (transplant-related_mortality)': {0, 1},
        'acute_gvhd_grade': {0, 1, 2, 3, 4}
    }

    # Проверка категориальных значений
    for col, allowed in valid_values.items():
        if col in df.columns:
            invalid = df[~df[col].isin(allowed)]
            if not invalid.empty:
                issues.append(f"Недопустимые значения в колонке '{col}': {set(df[col]) - allowed}")

    # Проверка числовых диапазонов
    if 'hla_match_score' in df.columns:
        if not df['hla_match_score'].between(0, 10).all():
            issues.append("Некорректные значения в 'hla_match_score' (ожидается от 0 до 10)")

    if 'patient_age' in df.columns:
        if not df['patient_age'].between(0, 25).all():
            issues.append("Некорректные значения в 'patient_age' (ожидается от 0 до 25)")

    if 'donor_age' in df.columns:
        if not df['donor_age'].between(0, 60).all():
            issues.append("Некорректные значения в 'donor_age' (ожидается от 0 до 60)")

    if 'cd34_dose' in df.columns:
        if not (df['cd34_dose'] > 0).all():
            issues.append("Некорректные значения в 'cd34_dose' (ожидается > 0)")

    if 'engraftment_days' in df.columns and 'engraftment_success' in df.columns:
        invalid_days = df[(df['engraftment_success'] == 1) & ((df['engraftment_days'] < 0) | (df['engraftment_days'] > 100))]
        if not invalid_days.empty:
            issues.append("Некорректные значения в 'engraftment_days' при успешном приживлении (ожидается 0–100)")

    # Вывод результатов
    if issues:
        print("Обнаружены проблемы с данными:")
        for issue in issues:
            print(" -", issue)
    else:
        print("Все данные соответствуют требованиям")
