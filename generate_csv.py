import json
import csv
import glob
import re

# Define the CSV filename
csv_filename = "SBC_scores_summary.csv"

# Collect all SBC score JSON files
json_files = glob.glob("[1-9]*-SBC_scores.json")  # Matches files like 1-SBC_scores_codellama.json

# Initialize CSV data storage
csv_data = []

# Read JSON files
for file in sorted(json_files, key=lambda x: int(x.split("-")[0])):  # Ensure files are processed in order
    batch_number = re.match(r"(\d+)-SBC_scores\.json", file)  # Extract batch number
    batch = int(batch_number.group(1)) if batch_number else 0  # Default to 0 if not found

    with open(file, "r", encoding="utf-8") as f:
        print(f"Processing {file}...")
        try:
            json_data = json.load(f)

            # Ensure the JSON is a list of dictionaries
            if isinstance(json_data, list):
                for item in json_data:
                    csv_data.append([
                        batch,  # Batch number extracted from filename
                        item.get("question_id", ""),
                        item.get("input_requirement", ""),
                        item.get("reverse_generated_requirement", ""),
                        round(item.get("final_accuracy_score", 0), 4),
                        round(item.get("semantic_similarity", 0), 4),
                        round(item.get("bleu_score", 0), 4),
                        round(item.get("completeness_score", 0), 4),
                        ", ".join(item.get("missing_elements", [])),  # Handle missing elements as comma-separated string
                        ", ".join(item.get("extra_elements", []))  # Handle extra elements as comma-separated string
                    ])
            else:
                print(f"Skipping {file}: JSON root is not a list.")

        except json.JSONDecodeError:
            print(f"Error reading {file}: Invalid JSON.")

# Define CSV headers
headers = [
    "batch", "question_id", "input_requirement", "reverse_generated_requirement",
    "final_accuracy_score", "semantic_similarity", "bleu_score", "completeness_score",
    "missing_elements", "extra_elements"
]

# Write to CSV file
with open(csv_filename, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)  # Write headers
    writer.writerows(csv_data)  # Write data

print(f"CSV file '{csv_filename}' has been created successfully!")
