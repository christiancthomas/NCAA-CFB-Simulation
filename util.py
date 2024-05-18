import csv
import json
import re

# Function to remove brackets and characters within brackets
def remove_brackets(text):
    return re.sub(r'\[.*?\]', '', text)

# Load the CSV file and clean the data
csv_file_path = 'cfb - Sheet1 (1).csv'  # Update with your local file path
cleaned_data = []

with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        cleaned_row = {key: remove_brackets(value) for key, value in row.items()}
        cleaned_data.append(cleaned_row)

# Save the cleaned data to a JSON file
json_file_path = 'cfb_cleaned.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(cleaned_data, json_file, indent=4)

print(f"Cleaned JSON file saved as {json_file_path}")
