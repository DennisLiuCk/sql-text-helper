import pandas as pd
import os
from datetime import datetime

def deduplicate_csv(input_file, output_dir=None):
    """
    Remove duplicate rows from CSV file while preserving the header.
    
    Args:
        input_file (str): Path to input CSV file
        output_dir (str, optional): Directory for output file. If None, uses same directory as input
    
    Returns:
        str: Path to output file

    Example:
        ```source.csv
            ID
            1
            2
            2
            3
        ```
        
        deduplicate_csv('source.csv')
        # Output: 'source_deduplicated_20230101_123456.csv'
        ``` output.csv
            ID
            1
            2
            3
        ```
    """
    # Read CSV file
    df = pd.read_csv(input_file)
    
    # Remove duplicates while keeping first occurrence
    df_deduplicated = df.drop_duplicates()
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    input_filename = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{input_filename}_deduplicated_{timestamp}.csv"
    
    # Determine output directory
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct full output path
    output_path = os.path.join(output_dir, output_filename)
    
    # Write to CSV without index
    df_deduplicated.to_csv(output_path, index=False)
    
    # Print statistics
    total_rows = len(df)
    unique_rows = len(df_deduplicated)
    duplicates = total_rows - unique_rows
    
    print(f"Processing complete:")
    print(f"Total rows: {total_rows}")
    print(f"Unique rows: {unique_rows}")
    print(f"Duplicates removed: {duplicates}")
    print(f"Output saved to: {output_path}")
    
    return output_path

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Remove duplicate rows from CSV file while preserving the header.')
    parser.add_argument('input_file', help='Path to input CSV file')
    parser.add_argument('--output-dir', default='output', help='Directory for output file (default: output)')
    
    args = parser.parse_args()
    deduplicate_csv(args.input_file, args.output_dir)
