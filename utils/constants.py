# Мапы для изменения данных в датасетах на валидные (унифицирование данных)
# 'как_есть': 'как_надо'

# Пол
SEX_MAP = {
    'MALE': 'M', 'Male': 'M', 'male': 'M', '1': 'M',
    'FEMALE': 'F', 'Female': 'F', 'female': 'F', '2': 'F'
}

# Диагнозы
DIAGNOSIS_MAP = {
    'AML': 'AML', 'Acute myeloid leukemia': 'AML', '10': 'AML',
    'ALL': 'ALL', 'B-ALL': 'ALL', 'T-ALL': 'ALL', '20': 'ALL',
    'SCD': 'SCD', 'Sickle Cell Disease': 'SCD', '1': 'SCD', '2': 'SCD',
    'Thalassemia': 'Thalassemia', 'Beta thalassemia major': 'Thalassemia', 'Beta thalassemia intermedia': 'Thalassemia'
}

# Источник стволовых клеток
SOURCE_OF_CELLS_MAP = {
    'peripheral_blood': 'PBSC', '2': 'PBSC', '22': 'PBSC',
    'bone_marrow': 'BM', '1': 'BM',
}

# Родственные связи пациента с донором
# sibling, matched unrelated, parent, other related
DONOR_RELATION_MAP = {
    'BROTHER': 'sibling', 'SISTER': 'sibling', '1': 'sibling',
    'FATHER': 'parent', 'MOTHER': 'parent',
    'SON': 'other related', 'DAUGHTER': 'other related', 'UNCLE': 'other related', 'SELF': 'other related', 'COUSIN': 'other related',
    'UNRELATED': 'matched unrelated', '3': 'matched unrelated'
}

# Статус заболевания: ремиссия, активно, рецидив
# remission, aсtive, relapse
DISEASE_STATUS_MAP = {
    '1': 'remission', '2': 'remission',
    '3': 'relapse',
    '4': 'active'
}

# Этническая группа пациента
# white, black, asian, hispanic, other
PATIENT_ETHNICITY_MAP = {
    '1': 'white', 'EGYPTIAN': 'white', 'SYRIAN': 'white', 'YEMENI': 'white',
    '2': 'black', 'SUDANESE': 'black', 'ETHIOPIAN': 'black',
    '3': 'asian', 'BANGLADESHI': 'asian', 'INDIAN': 'asian', 'AFGHANISTAN': 'asian', 'PAKISTANI': 'asian',
    '4': 'other', '5': 'other', 'EMIRATI': 'other',
    '6': 'hispanic',
    }

# Тип кондиционирования перед ТКМ
# myeloblative, reduced_intensity, other
CONDITIONING_REGIMEN_MAP = {
    '1': 'myeloblative',
    '2': 'reduced_intensity',
    '3': 'other'
}

# Профилактика GVHD
GVHD_PROPHYLAXIS_MAP = {
    '1': 'ex_vivo_depletion', '2': 'ex_vivo_depletion',
    '3': 'post_cy', '4': 'post_cy',
    '5': 'cni_mmf',
    '6': 'cni_mtx',
    '7': 'cni_alone',
    '8': 'siro', '9': 'siro',
    '10': 'other', '11': 'other', '20': 'other',
    'Cyclosporin+MTX': 'cni_mtx',
    'MMF+Tacrolimus+Ruxolitinib': 'cni_mmf',
    'Cyclophosphamide+MMF+Tacrolimus': 'post_cy',
    'UNKNOWN': 'other',
    'Tacrolimus': 'cni_alone',
    'Cyclosporin': 'cni_alone',
    'Cyclosporin+MTX+Tacrolimus': 'cni_mtx',
    'Cyclosporin+MMF': 'cni_mmf',
    'Tacrolimus+MMF': 'cni_mmf',
    'Tacrolimus+MTX': 'cni_mtx',
    'MMF+Tacrolimus+MTX': 'cni_mmf',
    'Cyclophosphamide+MMF': 'post_cy',
    'Sirolimus': 'siro',
    'Cyclophosphamide+MMF+Sirolimus': 'post_cy',
    'MMF': 'other',
    'Cyclosporin+Abatacept': 'other',
    'Cyclophosphamide+MMF+Tacrolimus+Ruxolitinib': 'post_cy',
    'Cyclosporin+MTX+MMF+Leflunomide+Sirolimus': 'siro',
    'Cyclophosphamide+MMF+Tacrolimus+Cyclosporin': 'post_cy',
    'Cyclosporin+MTX+ Abatacept': 'cni_mtx',
}

# степень острой GVHD
ACUTE_GVHD_GRADE_MAP = {
    'MILD': 2,
    'MODERATE': 3,
    'SEVERE': 4
}
