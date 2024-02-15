#!/usr/bin/env python

import argparse
import csv
import pandas as pd


class CSV_Data:
    """Class to represent CSV data."""

    def __init__(self, file_path):
        """Initialize CSV data with the file path."""
        self.file_path = file_path
        self.data = pd.DataFrame()

    def read_csv(self):
        """Read the CSV file and store its contents."""
        try:
            self.data = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"Error: The file '{self.file_path}' not found.")
        except pd.errors.ParserError:
            print(f"Error: Invalid CSV format in file '{self.file_path}'.")
        except UnicodeDecodeError as e:
            print(f"Error: Unable to decode the contents \
                  of the CSV file '{self.file_path}': {e}")


class Reconciler:
    """Class to reconcile data between two CSV files."""

    def __init__(self, source_data, target_data):
        """Initialize the reconciler with source and target data."""
        self.source_data = source_data
        self.target_data = target_data

    def reconcile(self):
        """Reconcile the data between source and target files."""
        # Missing in target
        missing_in_target = self.source_data.data[
            ~self.source_data.data['ID'].isin(self.target_data.data['ID'])]

        # Missing in source
        missing_in_source = self.target_data.data[
            ~self.target_data.data['ID'].isin(self.source_data.data['ID'])]

        # Fields with discrepancies
        merged = pd.merge(self.source_data.data, self.target_data.data,
                          on='ID', suffixes=('_source', '_target'),
                          how='outer', indicator=True)
        discrepancies = merged[merged['_merge'] == 'both']

        return missing_in_target, missing_in_source, discrepancies


class ReportGenerator:
    """Class to generate reconciliation report."""

    def __init__(self, output_file, csv_data):
        """Initialize the report generator with output file and CSV data."""
        self.output_file = output_file
        self.csv_data = csv_data

    def write_report(self, missing_in_target,
                     missing_in_source, discrepancies):
        """Write the reconciliation report to the output file."""
        discrepancies_count = 0

        with open(self.output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Type', 'Record Identifier', 'Field',
                             'Source Value', 'Target Value'])
            for df, record_type in [(missing_in_target, 'Missing in Target'),
                                    (missing_in_source, 'Missing in Source'),
                                    (discrepancies, 'Field Discrepancy')]:
                for idx, row in df.iterrows():
                    if record_type == 'Field Discrepancy':
                        for column in self.csv_data.data.columns[1:]:
                            source_value = row[column + '_source']
                            target_value = row[column + '_target']
                            if source_value != target_value:
                                writer.writerow([record_type, row['ID'], column,
                                                 source_value, target_value])
                                discrepancies_count += 1
                    else:
                        writer.writerow([record_type] + row.values.tolist())

        return discrepancies_count


def main():
    """Main function to run the CSV reconciler."""
    parser = argparse.ArgumentParser(description='CSV Reconciler')
    parser.add_argument('-s', '--source', help='Path to the source CSV file')
    parser.add_argument('-t', '--target', help='Path to the target CSV file')
    parser.add_argument('-o', '--output', help='Path to save the output reconciliation report')
    args = parser.parse_args()

    source_data = CSV_Data(args.source)
    target_data = CSV_Data(args.target)

    source_data.read_csv()
    target_data.read_csv()

    reconciler = Reconciler(source_data, target_data)
    missing_in_target, missing_in_source, discrepancies = reconciler.reconcile()

    report_generator = ReportGenerator(args.output, source_data)
    discrepancies_count = report_generator.write_report(missing_in_target, missing_in_source, discrepancies)

    print("Reconciliation completed:")
    print(f"- Records missing in target: {len(missing_in_target)}")
    print(f"- Records missing in source: {len(missing_in_source)}")
    print(f"- Records with field discrepancies: {discrepancies_count}")
    print(f"Report saved to: {args.output}")


if __name__ == "__main__":
    main()
