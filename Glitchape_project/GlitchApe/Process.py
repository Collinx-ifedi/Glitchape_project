import json
import re
import os
import sys

# --- CONFIGURATION ---

# 1. Define the mapping of Model IDs to the final Apparel Type name.
# This controls both filtering and renaming.
MODEL_TO_APPAREL_MAP = {
    "Gildan 18500": "Hoodie",
    "Gildan 64000": "T-Shirt",
    "Gildan 18000": "Sweatshirt",
    "Gildan 2400": "Long Sleeve Shirt",
    "Gildan 64800": "Polo Shirt",
    "85900": "Long Sleeve Polo Shirt" 
}

# 2. Define the input and output filenames
INPUT_FILENAME = "variant_map.json"
OUTPUT_FILENAME = "ai_mapped_variants.json"

# --- SCRIPT LOGIC ---

def load_variants(filename: str) -> list[dict[str, any]]:
    """
    Loads the variant map from the specified JSON file with error handling.
    """
    if not os.path.exists(filename):
        print(f"Error: Input file '{filename}' not found in the current directory.", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(f"Error: Input file '{filename}' is not a JSON list.", file=sys.stderr)
            sys.exit(1)
        print(f"Successfully loaded {len(data)} total variants from '{filename}'.")
        return data
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filename}'. Check file for syntax errors.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}", file=sys.stderr)
        sys.exit(1)

def process_variants(all_variants: list[dict[str, any]]) -> list[dict[str, any]]:
    """
    Filters and transforms the variant list based on the MODEL_TO_APPAREL_MAP.
    """
    filtered_and_renamed_variants = []
    model_ids_to_keep = list(MODEL_TO_APPAREL_MAP.keys())
    
    for variant in all_variants:
        product_name = variant.get('product_name')
        if not product_name:
            continue

        found_model_id = None
        
        # 1. Filtering: Check if the product name contains any of the model IDs
        for model_id in model_ids_to_keep:
            # Use regex with word boundary (\b) to ensure we match the whole model ID
            if re.search(r'\b' + re.escape(model_id) + r'\b', product_name):
                found_model_id = model_id
                break
        
        # 2. Renaming: If a match was found, process the variant
        if found_model_id:
            # Create a copy to avoid modifying the original list (good practice)
            modified_variant = variant.copy()
            
            # Get the new simple apparel type (e.g., "Hoodie")
            apparel_type = MODEL_TO_APPAREL_MAP[found_model_id]
            
            # Extract the size/color string, e.g., "(S, White)"
            # We find the last parenthesis to ensure we get the right part
            size_color_string = ""
            start_index = product_name.rfind('(')
            if start_index != -1:
                size_color_string = product_name[start_index:]

            # 3. Construct the NEW product_name
            # This replaces the entire old name
            new_product_name = f"{apparel_type}"
            modified_variant['product_name'] = new_product_name
            
            filtered_and_renamed_variants.append(modified_variant)
            
    return filtered_and_renamed_variants

def save_variants(filename: str, variants: list[dict[str, any]]):
    """
    Saves the processed variant list to the output JSON file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(variants, f, indent=2)
        print(f"\nSuccess! Filtered and saved {len(variants)} variants to '{filename}'.")
    except Exception as e:
        print(f"An error occurred while writing the output file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """
    Main execution function.
    """
    print("Starting variant processing script...")
    
    # Load
    variants = load_variants(INPUT_FILENAME)
    
    # Process
    processed_data = process_variants(variants)
    
    # Save
    save_variants(OUTPUT_FILENAME, processed_data)
    
    # Show a sample of the new data
    print("\n--- Sample of renamed data (first 3 entries) ---")
    print(json.dumps(processed_data[:3], indent=2))
    print("-------------------------------------------------")

if __name__ == "__main__":
    main()