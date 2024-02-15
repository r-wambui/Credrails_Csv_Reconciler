# CSV Reconciler

CSV Reconciler is a Python application that reconciles data between two CSV files, identifying missing records and discrepancies between them.

## Features

- **Missing in Target**: Identifies records that are present in the source CSV file but missing in the target CSV file.
- **Missing in Source**: Identifies records that are present in the target CSV file but missing in the source CSV file.
- **Field Discrepancy**: Identifies records that exist in both CSV files but have differing values for specific fields.

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/r-wambui/Credrails_Csv_Reconciler.git
    ```

2. Navigate to the project directory:

    ```
    cd Credrails_Csv_Reconciler
    ```
3. Create a virtual environment

    ```
    virtualenv venv
    ```
4. Install the required dependencies:

    
    ```
    pip install -r requirements.txt
    ```

5. To ensure the code runs in bash, Make the script executable by changing permissions

    ```
    chmod +x csv_reconciler.py 
    ```

6. Copy the script in the virtual environment

   ```
   cp /path/to/your/csv_reconciler.py /path/to/your/venv/bin/csv_reconciler

   ``` 


## Usage

To reconcile two CSV files, use the following command-line arguments:

```
csv_reconciler -s <source-csv-file> -t <target-csv-file> -o <output-csv-file> 
```

## Example

```
csv_reconciler -s examples/source.csv -t examples/target.csv -o examples/reconciliation_report.csv 
```

This command reconciles the `source.csv` file with the `target.csv` file and saves the reconciliation report to `reconciliation_report.csv`. All the files are saved in the examples directory

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

