#!/usr/bin/env python3
"""
HTML Regex Extractor Script

This script reads an HTML file and searches for a specific regex pattern,
extracting capture groups and writing them to a TSV file.
"""

import re
import csv
import argparse
import sys
from pathlib import Path
from datetime import datetime

# Portuguese month abbreviations mapping
PORTUGUESE_MONTHS = {
    'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6,
    'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12
}

def parse_portuguese_date(date_str, current_year, is_december_first_row):
    """
    Parse Portuguese date format like '21 JAN' and convert to ISO format.
    
    Args:
        date_str (str): Date string in format 'DD MMM' with Portuguese month
        current_year (int): Current year to use as default
        is_december_first_row (bool): Whether the first row was December
    
    Returns:
        str: Date in ISO format (YYYY-MM-DD)
    """
    
    # Split day and month
    parts = date_str.strip().split()
    if len(parts) != 2:
        raise ValueError(f"Invalid date format: {date_str}")
    
    day_str, month_str = parts
    day = int(day_str)
    month_str = month_str.upper()
    
    if month_str not in PORTUGUESE_MONTHS:
        raise ValueError(f"Unknown Portuguese month: {month_str}")
    
    month = PORTUGUESE_MONTHS[month_str]
    
    # Determine year based on logic:
    # If first row is DEZ, then all DEZ entries are previous year, JAN entries are current year
    # Otherwise, all entries are current year
    if is_december_first_row:
        if month_str == 'DEZ':
            year = current_year - 1
        else:
            year = current_year
    else:
        year = current_year
    
    return f"{year:04d}-{month:02d}-{day:02d}"


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
        
        # Get current year
        current_year = datetime.now().year
        
        # Check if first row is December to determine year logic
        first_date = matches[0][0].strip().upper()
        is_december_first_row = first_date.endswith('DEZ')
        
        # Process matches and convert dates
        processed_matches = []
        for match in matches:
            date_str, card_number, description, amount_text = match
            amount = -float(amount_text.replace('.', '').replace(',', '.'))
            
            # Parse and convert the date
            iso_date = parse_portuguese_date(date_str, current_year, is_december_first_row)
            processed_matches.append([iso_date, card_number, description, -amount])
        
        # Write to TSV file (tab-separated values)
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            
            # Write header (optional - you can remove this if not needed)
            writer.writerow(['Date', 'CardNumber', 'Description', 'Amount'])
            
            # Write each processed match as a row
            for match in processed_matches:
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