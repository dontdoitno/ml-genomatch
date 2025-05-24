import pandas as pd

def yes_no_to_numbers(var) -> int:
    """
    Converts 'yes' to 1, 'no' to 0, and handles float values
    """
    if pd.isna(var):
        return None
    if isinstance(var, (int, float)):
        return int(var)
    if isinstance(var, str):
        if var.lower() == 'yes':
            return 1
        elif var.lower() == 'no':
            return 0
    return None


def convert_hla_match(hla) -> int:
    """
    Converts HLA match data to numeric values, handling both string and float inputs
    """
    if pd.isna(hla):
        return None
    if isinstance(hla, (int, float)):
        return int(hla)
    if isinstance(hla, str):
        # 6-10/10, 6-10 OF 10 и 12 OF 12
        hla_variants = ['10/10', '10 OF 10', '12 OF 12']
        if hla in hla_variants:
            return 10
        else:
            return int(hla[0])
    return None
