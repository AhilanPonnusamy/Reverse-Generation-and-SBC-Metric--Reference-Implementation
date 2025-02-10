import json
import subprocess
import sys

def process_json(file_path):
    try:
        # Load JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Ensure data is a list of objects
        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of objects.")

        for i in range(1, 4):  # Iterate 3 times
            results = []
            print(f"***** Codellama Iteration {i}/3 *****")

            for item in data:
                requirement = item.get("requirement")
                language = item.get("programming_language")
                questionid = item.get("question_id")
                print(f"Processing question: {questionid} in iteration {i}")

                if requirement:
                    # Call SBC_score_calculator.py with the requirement
                    result = subprocess.run(
                        [sys.executable, "SBC_score_calculator.py", language, requirement], 
                        capture_output=True, text=True, check=True
                    )
                    result_data = json.loads(result.stdout)
                    result_data["question_id"] = questionid
                    results.append(result_data)
                else:
                    print(f"Skipping entry {questionid}: missing 'requirement' field")

            # Write results to numbered SBC_scores.json file
            output_filename = f"{i}-SBC_scores-codestal.json"
            with open(output_filename, "w", encoding='utf-8') as output_file:
                json.dump(results, output_file, indent=4)

            print(f"Results for iteration {i} have been written to {output_filename}")

    except Exception as e:
        print(f"Error processing JSON file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <json_file_path>")
    else:
        process_json(sys.argv[1])
