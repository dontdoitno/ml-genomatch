import pandas as pd
import numpy as np
from typing import List, Optional
from data_sources.uae import preprocess_data as uae_preprocess
from data_sources.bone_marrow import preprocess_data as bone_marrow_preprocess
from data_sources.p5191 import preprocess_data as p5191_preprocess
from data_sources.p5303 import preprocess_data as p5303_preprocess
from utils.validate_dataframe import validate_dataframe, print_validation_results
from utils.preprocessing import get_standard_columns

def load_and_preprocess_datasets() -> List[pd.DataFrame]:
    """
    Loads and preprocesses all available datasets
    Returns a list of preprocessed dataframes
    """
    dfs = []
    data_sources = [
        ('UAE', uae_preprocess),
        ('Bone Marrow', bone_marrow_preprocess),
        ('P5191', p5191_preprocess),
        ('P5303', p5303_preprocess)
    ]

    for source_name, preprocess_func in data_sources:
        try:
            print(f"\nProcessing {source_name} dataset...")
            df = preprocess_func()

            # Print column information
            print(f"Columns in {source_name} dataset:")
            for col in df.columns:
                non_null = df[col].count()
                total = len(df)
                print(f"- {col}: {non_null}/{total} non-null values")

            dfs.append(df)
            print(f"Successfully processed {source_name} dataset")
        except Exception as e:
            print(f"Warning: Failed to process {source_name} dataset: {str(e)}")
            continue

    return dfs

def combine_datasets(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Combines multiple dataframes into a single dataset with standardized columns
    """
    if not dfs:
        raise ValueError("No dataframes to combine")

    # Get list of standardized columns
    standard_columns = get_standard_columns()
    print("\nStandard columns that will be in final dataset:")
    for col in standard_columns:
        print(f"- {col}")

    # Process each dataframe to ensure it has all standard columns
    processed_dfs = []
    for i, df in enumerate(dfs):
        print(f"\nProcessing dataframe {i+1}:")
        # Create a new dataframe with all standard columns
        new_df = pd.DataFrame(columns=standard_columns)

        # Copy existing columns that match standard names
        for col in standard_columns:
            if col in df.columns:
                new_df[col] = df[col]
                non_null = df[col].count()
                total = len(df)
                print(f"- {col}: {non_null}/{total} non-null values")
            else:
                new_df[col] = np.nan
                print(f"- {col}: 0/{len(df)} non-null values (filled with NaN)")

        processed_dfs.append(new_df)

    # Combine all dataframes
    print("\nCombining dataframes...")
    combined_df = pd.concat(processed_dfs, ignore_index=True)

    # Remove duplicate rows if any
    initial_rows = len(combined_df)
    combined_df = combined_df.drop_duplicates()
    if len(combined_df) < initial_rows:
        print(f"Removed {initial_rows - len(combined_df)} duplicate rows")

    return combined_df

def main():
    try:
        # Load and preprocess all datasets
        dfs = load_and_preprocess_datasets()

        if not dfs:
            raise ValueError("No datasets were successfully processed")

        # Combine datasets
        print("\nCombining datasets...")
        full_df = combine_datasets(dfs)

        # Validate the combined dataset
        print("\nValidating combined dataset...")
        validation_issues = validate_dataframe(full_df)
        print_validation_results(validation_issues)

        # Save the combined dataset
        output_path = "processed/transplant_data.csv"
        full_df.to_csv(output_path, index=False)
        print(f"\nCombined dataset saved to: {output_path}")
        print(f"Total rows: {len(full_df)}")
        print(f"Total columns: {len(full_df.columns)}")
        print("\nFinal column statistics:")
        for col in full_df.columns:
            non_null = full_df[col].count()
            total = len(full_df)
            print(f"- {col}: {non_null}/{total} non-null values ({non_null/total*100:.1f}%)")

    except Exception as e:
        print(f"Error in main pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()
