# SQL Text Helper

A collection of utilities for processing SQL query results and CSV files.

## Table of Contents
- [Requirements](#requirements)
- [Features](#features)
  - [CSV to MySQL Tuple](#csv-to-mysql-tuple)
  - [CSV Deduplication](#csv-deduplication)

## Requirements

- Python 3.x
- pandas (for deduplication feature)

## Features

### CSV to MySQL Tuple

Convert CSV column values into MySQL tuple format, suitable for use in SQL IN clauses.

#### Technical Implementation
- Uses Python's built-in `csv.DictReader` for robust CSV parsing
- Implements case-insensitive column name matching
- Handles column names with spaces intelligently
- Supports UTF-8 encoded files for international character support
- Formats data into MySQL-compatible tuple string with proper quoting
- Includes error handling for file operations and data processing
- Provides flexible output options (console or file)
- Optional quote formatting for values

#### Usage
```bash
# Basic usage (with quotes)
python csv_to_mysql.py <csv_file> <column_name>

# Without quotes
python csv_to_mysql.py <csv_file> <column_name> --no-quotes

# Save to output file
python csv_to_mysql.py <csv_file> <column_name> [--no-quotes] output/result.txt
```

#### Example

Input CSV (`source.csv`):
```csv
PRODUCT_CAT_CODE,PRODUCT_NAME
AA11031000001,Product A
AA11032500001,Product B
AA11033500001,Product C
```

Command:
```bash
python csv_to_mysql.py source.csv PRODUCT_CAT_CODE
```

Output:
```sql
# With quotes (default)
('AA11031000001', 'AA11032500001', 'AA11033500001')

# Without quotes (using --no-quotes)
(AA11031000001, AA11032500001, AA11033500001)
```

SQL Usage:
```sql
SELECT * FROM products 
WHERE product_cat_code IN ('AA11031000001', 'AA11032500001', 'AA11033500001')
```

### CSV Deduplication

Remove duplicate rows from CSV files while preserving the header row.

#### Technical Implementation
- Uses `pandas` DataFrame for efficient data handling
- Implements `drop_duplicates()` function which compares all columns to identify duplicates
- Preserves the first occurrence of each unique row combination
- Memory efficient as it processes data in a streaming fashion
- Maintains data types and structure of the original CSV
- Generates timestamped output files for version tracking

#### Usage
```bash
# Basic usage with default output directory
python deduplicate_csv.py input_file.csv

# With custom output directory
python deduplicate_csv.py input_file.csv --output-dir custom_output
```

#### Example

Input CSV (`source.csv`):
```csv
STORE_SKU_ID,PRODUCT_CAT_CODE,ONLINE_STATUS
C0003001_S_amila008-1,AA28625015001,ONLINE
C0003001_S_amila008-1,AA28625015001,ONLINE
C0003001_S_amila008-2,AA28625015001,ONLINE
C0003001_S_amila008-2,AA28625015001,ONLINE
```

Command:
```bash
python deduplicate_csv.py source.csv
```

Output CSV (`source_deduplicated_20250109_160000.csv`):
```csv
STORE_SKU_ID,PRODUCT_CAT_CODE,ONLINE_STATUS
C0003001_S_amila008-1,AA28625015001,ONLINE
C0003001_S_amila008-2,AA28625015001,ONLINE
```

## Adding New Features

When adding new features to this repository:
1. Create a new Python script in the root directory
2. Add a new section in this README under the Features section
3. Include the following subsections:
   - Technical Implementation
   - Usage
   - Example
4. Update the Table of Contents
