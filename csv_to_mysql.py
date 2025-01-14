import csv
import sys
from pathlib import Path
import os

def csv_column_to_mysql_tuple(csv_file, column_name, add_quotes=True):
    """
    Convert a specific column from CSV file to MySQL tuple format.
    
    Args:
        csv_file (str): Path to the CSV file
        column_name (str): Name of the column to extract
        add_quotes (bool, optional): Whether to add single quotes around values. Defaults to True.
        
    Returns:
        str: MySQL-compatible tuple string
        
    Example:
        ```source.csv
            PRODUCT_CAT_CODE
            AA11031000001
            AA11032500001
            AA11033500001
        ```
        
        # With quotes (default)
        csv_column_to_mysql_tuple('source.csv', 'PRODUCT_CAT_CODE')
        # Output: ('AA11031000001', 'AA11032500001', 'AA11033500001')
        
        # Without quotes
        csv_column_to_mysql_tuple('source.csv', 'PRODUCT_CAT_CODE', add_quotes=False)
        # Output: (AA11031000001, AA11032500001, AA11033500001)
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            # Read the CSV file with the correct dialect
            reader = csv.DictReader(f)
            
            # Print available columns for debugging
            print(f"Available columns: {', '.join(reader.fieldnames)}")
            
            # Try to find the column by exact match or by joining space-separated arguments
            actual_column = None
            for col in reader.fieldnames:
                if col.lower() == column_name.lower():
                    actual_column = col
                    break
            
            if not actual_column:
                print(f"Warning: Column '{column_name}' not found exactly, trying to find a match...")
                for col in reader.fieldnames:
                    if col.lower().replace(' ', '') == column_name.lower().replace(' ', ''):
                        actual_column = col
                        print(f"Found matching column: '{col}'")
                        break
            
            if not actual_column:
                print(f"Error: Could not find column matching '{column_name}'")
                return None
            
            # Extract values using the found column name and clean up whitespace
            values = []
            for row in reader:
                value = row[actual_column].strip()
                if value:  # Only add non-empty values
                    values.append(value)
            
            if not values:
                print(f"Warning: No values found for column '{actual_column}'")
                return None
                
            # Format values into MySQL tuple string with optional quotes
            if add_quotes:
                formatted_values = "(" + ", ".join(f"'{value}'" for value in values) + ")"
            else:
                formatted_values = "(" + ", ".join(values) + ")"
            return formatted_values
            
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
        return None

def csv_to_mysql_update_script(csv_file, table_name):
    """
    Convert CSV content to MySQL update script.
    
    Args:
        csv_file (str): Path to the CSV file
        table_name (str): Name of the MySQL table to update
        
    Returns:
        str: MySQL update script
        
    Example:
        ```source.csv
            id,name,age
            1,'may',10
            2,'Allen',15
        ```
        
        csv_to_mysql_update_script('source.csv', 'user')
        # Output:
        # Update user set name = 'may', age = 10 where id = 1;
        # Update user set name = 'Allen', age = 15 where id = 2;
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            update_statements = []
            
            for row in reader:
                set_clause = ", ".join([f"{col} = {value}" for col, value in row.items() if col != 'id'])
                update_statement = f"Update {table_name} set {set_clause} where id = {row['id']};"
                update_statements.append(update_statement)
            
            return "\n".join(update_statements)
            
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
        return None

def save_to_file(content, output_file):
    """
    Save content to a file.
    
    Args:
        content (str): Content to save
        output_file (str): Path to output file
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Result saved to: {output_file}")
    except Exception as e:
        print(f"Error saving to file: {str(e)}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python csv_to_mysql.py <csv_file> <column_name> [--no-quotes] [output_file]")
        return
    
    # Parse arguments
    csv_file = sys.argv[1]
    args = sys.argv[2:]
    
    # Check for --no-quotes flag
    add_quotes = True
    if '--no-quotes' in args:
        add_quotes = False
        args.remove('--no-quotes')
    
    # Join remaining arguments between the file and output path as the column name
    last_arg = args[-1]
    if len(args) > 1 and last_arg.startswith('output'):
        column_name = ' '.join(args[:-1])
        output_file = last_arg
    else:
        column_name = ' '.join(args)
        output_file = None
    
    if column_name.lower() == 'update_script':
        table_name = args[0]
        result = csv_to_mysql_update_script(csv_file, table_name)
    else:
        result = csv_column_to_mysql_tuple(csv_file, column_name, add_quotes)
    
    if result:
        if output_file:
            save_to_file(result, output_file)
        print(result)

if __name__ == "__main__":
    main()
