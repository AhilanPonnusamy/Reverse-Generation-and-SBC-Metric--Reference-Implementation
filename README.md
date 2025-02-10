# Setup and Execution Guide

## Prerequisites
- Ensure you have **Python 3.11** installed.
- Install `git` if it is not already set up.

## Steps to Run the Code

### 1. Install Required Packages
Create a virtual environment and install all necessary dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 2. Download the Code Repository
Clone the repository using Git:

```bash
git clone <repository-url>
cd <repository-name>
```

Alternatively, you can download the ZIP file directly from the repository's main page under the **Code** option.

### 3. Configure LLM Endpoint (If Required)
Update the **LLM endpoint URL** and **API Key** in `reverse_generation.py`:

- Modify the following variables:
  ```
  API_URL = "your_llm_endpoint_url"
  API_KEY = "your_api_key"
  ```

### 4. Run `invoker.py`
Execute the following command to start the process:

```bash
python invoker.py
```

> **Note:** Depending on your device configuration and the hosted LLM, this step may take a few hours to complete. It will generate **three `SBC_scores.json` files**.

### 5. Generate Summary CSV
Run the following command to generate a summary file:

```bash
python generate_csv.py
```

This will create an output file named **`SBC_scores_summary.csv`**, which contains the results for analysis.

---

You are now ready to analyze the generated SBC scores!
