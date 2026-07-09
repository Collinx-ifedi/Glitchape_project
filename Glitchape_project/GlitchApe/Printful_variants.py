import pandas as pd
import json
import logging
import sys
from typing import List, Optional

# --- Configuration Constants ---
INPUT_FILENAME = "USA_printful_products.csv"
OUTPUT_FILENAME = "variant_map.json"
SEARCH_TERMS = ['shirt', 'trousers', 'hoodie', 'joggers']

# --- Setup basic logging ---
# This logs messages to the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Explicitly log to standard output
    ]
)


def load_data(filepath: str) -> Optional[pd.DataFrame]:
    """
    Loads product data from a CSV file and standardizes column names.

    Args:
        filepath: The path to the input CSV file.

    Returns:
        A pandas DataFrame with the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(filepath)
        logging.info(f"Successfully loaded data from {filepath}")
        
        # Standardize column names (e.g., 'Product Name' -> 'product_name')
        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace(r'[\(\)]', '', regex=True) # Remove parentheses
        )
        
        return df
        
    except FileNotFoundError:
        logging.error(f"Error: The file '{filepath}' was not found.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading data: {e}")
        return None


def filter_products(df: pd.DataFrame, terms: List[str]) -> pd.DataFrame:
    """
    Filters the DataFrame based on search terms in product_name or product_type.

    Args:
        df: The input DataFrame with product data.
        terms: A list of lowercase strings to search for.

    Returns:
        A new DataFrame containing only the filtered rows.
    """
    if 'product_name' not in df.columns or 'product_type' not in df.columns:
        logging.warning("Columns 'product_name' or 'product_type' not found. Filtering may be incomplete.")
        return pd.DataFrame() # Return empty frame

    search_pattern = '|'.join(terms)
    
    # Filter using case-insensitive regex on both columns
    mask = (
        df['product_name'].str.contains(search_pattern, case=False, na=False) |
        df['product_type'].str.contains(search_pattern, case=False, na=False)
    )
    
    filtered_df = df[mask].copy()
    
    # Drop the 'notes' column if it exists, as it's often sparse
    if 'notes' in filtered_df.columns:
        filtered_df = filtered_df.drop(columns=['notes'])
        
    logging.info(f"Found {len(filtered_df)} products matching the search terms.")
    return filtered_df


def save_json(df: pd.DataFrame, filepath: str) -> bool:
    """
    Saves the DataFrame to a JSON file in 'records' orientation.

    Args:
        df: The DataFrame to save.
        filepath: The destination JSON file path.

    Returns:
        True if saving was successful, False otherwise.
    """
    try:
        # Use orient='records' for a clean list of objects: [ {col: val}, ... ]
        # indent=4 makes the file human-readable
        df.to_json(filepath, orient='records', indent=4)
        
        logging.info(f"Successfully saved filtered data to {filepath}")
        return True
        
    except IOError as e:
        logging.error(f"Error writing to file '{filepath}': {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving JSON: {e}")
        return False


def main():
    """
    Main function to run the data processing pipeline.
    """
    logging.info("Starting product filtering process...")
    
    product_df = load_data(INPUT_FILENAME)
    
    if product_df is not None:
        filtered_df = filter_products(product_df, SEARCH_TERMS)
        
        if not filtered_df.empty:
            save_json(filtered_df, OUTPUT_FILENAME)
        else:
            logging.info("No products matched the filter criteria. No output file created.")
            
    logging.info("Product filtering process finished.")


# Standard Python entry point
if __name__ == "__main__":
    main()