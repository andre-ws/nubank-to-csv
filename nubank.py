#!/usr/bin/env python3
"""
HTML Regex Extractor Script

This script reads an HTML file and searches for a specific regex pattern,
extracting capture groups and writing them to a TSV file with tab separators.
"""

import re
import csv
import argparse
import sys
from pathlib import Path


def extract_data_from_html(html_file_path, output_csv_path):
    """
    Extract data from HTML file using regex and write to TSV.
    
    Args:
        html_file_path (str): Path to the input HTML file
        output_csv_path (str): Path to the output TSV file
    """
    # The regex pattern with 4 capture groups
    # Updated to handle space after R$ (Brazilian currency format)
    pattern = r"^(.*)<br\/>\n•••• (\d{4})<br\/>\n(.*)<br\/>\nR\$ (.*)<br\/>"
    
    try:
        # Read the HTML file
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Find all matches (using MULTILINE flag for ^ anchor)
        matches = re.findall(pattern, html_content, re.MULTILINE)
        
        if not matches:
            print(f"No matches found in {html_file_path}")
            return
        
        # Write to TSV file (tab-separated values)
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            
            # Write header (optional - you can remove this if not needed)
            writer.writerow(['Date', 'CardNumber', 'Description', 'Amount'])
            
            # Write each match as a row (keeping original comma format in amounts)
            for match in matches:
                writer.writerow(match)
        
        print(f"Successfully extracted {len(matches)} matches from {html_file_path}")
        print(f"Results written to {output_csv_path}")
        
    except FileNotFoundError:
        print(f"Error: File {html_file_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments and execute the extraction."""
    parser = argparse.ArgumentParser(
        description="Extract data from HTML file using regex and save to TSV"
    )
    parser.add_argument(
        'html_file', 
        help='Path to the input HTML file'
    )
    parser.add_argument(
        '-o', '--output', 
        default='output.csv',
        help='Path to the output TSV file (default: output.csv)'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not Path(args.html_file).exists():
        print(f"Error: Input file {args.html_file} does not exist.")
        sys.exit(1)
    
    # Extract data
    extract_data_from_html(args.html_file, args.output)


if __name__ == "__main__":
    main()