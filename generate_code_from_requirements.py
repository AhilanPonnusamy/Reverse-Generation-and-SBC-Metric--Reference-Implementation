import sys
import requests

# Define API URL and API Key
#API_URL = "https://granite-8b-code-instruct-maas-apicast-production.apps.llmaas.llmaas.redhatworkshops.iom:443"
API_URL = "http://127.0.0.1:8000"
API_KEY = "078ebebf8e287869d30fd5e9b02c7190"  # Replace with your actual API key


def query_llm(prompt):
    """Send a prompt to the LLM server and return the response."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "granite-8b-code-instruct-128k",
        "prompt": prompt,
        "max_tokens": 6144,
        "temperature": 0
    }
    try:
        response = requests.post(f"{API_URL}/v1/completions", json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        return response_data["choices"][0]["text"].strip() if "choices" in response_data else "No response content received."
    except requests.RequestException as e:
        print(f"Error communicating with LLM server: {e}")
        return "ERROR: Failed to fetch response"


def generate_app_code(language, requirements):
    """Generate application code based on user requirements and programming language."""
    if not requirements.strip():
        return "ERROR: Requirements input is empty."

    # Define language-specific instructions
    if language.lower() == "react":
        framework_details = (
            "Generate a complete React application based on the following requirements. "
            "Use functional components, hooks, and Material-UI for styling. "
            "Ensure state management, API integration, and responsive design."
            "Only return the full source code without any additional explanation or comments."
        )
    elif language.lower() == "angular":
        framework_details = (
            "Generate a complete Angular application based on the following requirements. "
            "Use Angular components, services, and Angular Material for styling. "
            "Ensure routing, state management with NgRx, and API integration."
            "Only return the full source code without any additional explanation or comments."
        )
    else:
        return "ERROR: Unsupported programming language. Use 'React' or 'Angular'."

    # Construct the prompt
    prompt = f"{framework_details}\n\nRequirements:\n{requirements}"

    return query_llm(prompt)


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_app_code.py <LANGUAGE> '<REQUIREMENTS>'")
        sys.exit(1)

    language = sys.argv[1]
    requirements = sys.argv[2]

    print(f"Generating {language} application code...")
    result = generate_app_code(language, requirements)

    if result.startswith("ERROR"):
        print(result)
        sys.exit(1)

    print("\nGenerated Code:")
    print(result)


if __name__ == "__main__":
    main()
