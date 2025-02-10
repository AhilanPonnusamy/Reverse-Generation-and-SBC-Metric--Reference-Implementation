import sys
import requests
import json
import re
# Define API URL and API Key
API_URL = "http://localhost:11434/api/generate"
API_KEY = "xxxxxxxxxxxxxxxx"

def query_llm(prompt):
    """Send a prompt to the LLM server and return the response."""
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            url=API_URL,
            json={
                "model": "codestral:22b",
                "prompt": prompt,
                "max_tokens": 4096,
                "temperature": 0
            },
            headers=headers,
            stream=True
        )
        full_response = ""

        for line in response.iter_lines():
            if line:
                try:
                    json_line = json.loads(line.decode("utf-8"))
                    if "response" in json_line:
                        full_response += json_line["response"]
                except json.JSONDecodeError:
                    continue  # Ignore malformed JSON lines in streaming

        return full_response.strip()

    except requests.RequestException as e:
        return f"ERROR: Failed to fetch response - {e}"


def clean_requirements(text):
    """Remove any unwanted code snippets or formatting from the response."""
    # Remove markdown code blocks (```) and other code-like patterns
    text = re.sub(r'```[a-zA-Z]*\n.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'<.*?>', '', text)  # Remove any HTML/JSX tags
    text = re.sub(r'\{.*?\}', '', text)  # Remove JavaScript/React curly braces content
    text = re.sub(r'\n+', ' ', text).strip()  # Normalize newlines to spaces
    return text

def generate_app_code(language, requirements):
    """Generate application code based on user requirements and programming language."""
    if not requirements.strip():
        return "ERROR: Requirements input is empty."

    # Define language-specific instructions
    if language.lower() == "react":
        framework_details = (
            "Generate a complete React application based on the following requirements. "
            "Use functional components, hooks, and Material-UI for styling. "
            "Ensure state management, API integration, and responsive design. "
            "Only return the full source code without any additional explanation or comments and do not include the requirements themselves."
        )
    elif language.lower() == "angular":
        framework_details = (
            "Generate a complete Angular application based on the following requirements. "
            "Use Angular components, services, and Angular Material for styling. "
            "Ensure routing, state management with NgRx, and API integration. "
            "Only return the full source code without any additional explanation or comments and do not include the requirements themselves.."
        )
    elif language.lower() == "sql":
        framework_details = (
            "Generate a complete SQL schema based on the following requirements. "
            "Ensure proper table structures, relationships (one-to-one, one-to-many, or many-to-many as needed), and constraints such as primary keys, foreign keys, and data types. "
            "Only return the full SQL code without any additional explanation, comments, functions, or triggers and do not include the requirements themselves.."
        )
    elif language.lower() == "springboot":
        framework_details = (
            "Generate complete Java classes using Spring Boot for the following data model. "
            "Ensure the appropriate use of annotations such as @Entity, @Id, @OneToMany, @ManyToOne, @ManyToMany, @JoinColumn, and @Table as needed. "
            "Include necessary fields, getters, setters, constructors, and relationships between entities (one-to-one, one-to-many, or many-to-many). "
            "The class should also include basic validation annotations like @NotNull or @Size where applicable. "
            "Return only the Java class code without any extra explanation or comments, and ensure that the classes are structured to be used in a Quarkus application."
        )
    elif language.lower() == ".net":
        framework_details = (
            "Generate complete C# classes for .NET based on the following data model. "
            "Ensure the appropriate use of annotations such as [Table], [Key], [Required], [MaxLength], [ForeignKey], and [InverseProperty] as needed. "
            "Include the necessary fields, constructors, getters, setters, and relationships between entities (one-to-one, one-to-many, or many-to-many). "
            "Ensure the classes are compatible with Entity Framework Core, including the correct use of navigation properties and data annotations for validation. "
            "Return only the C# class code without any extra explanation or comments, and ensure the structure is suitable for use in a .NET application."
        )
    elif language.lower() == "node":
        framework_details = (
            "Generate complete Node.js script(classes) for .NET based on the following data model. "
            "Ensure the appropriate use of annotations such as [Table], [Key], [Required], [MaxLength], [ForeignKey], and [InverseProperty] as needed. "
            "Include the necessary fields, constructors, getters, setters, and relationships between entities (one-to-one, one-to-many, or many-to-many). "
            "Ensure the classes are compatible with Entity Framework Core, including the correct use of navigation properties and data annotations for validation. "
            "Return only the JavaScript code without any extra explanation or comments, and ensure the structure is suitable for use in a Node.js application."
        ) 
    elif language.lower() == "quarkus":       
        framework_details = (
            "Generate complete Java classes using Quarkus for the following data model. "
            "Ensure the appropriate use of annotations such as @Entity, @Id, @OneToMany, @ManyToOne, @ManyToMany, @JoinColumn, and @Table as needed. "
            "Include necessary fields, getters, setters, constructors, and relationships between entities (one-to-one, one-to-many, or many-to-many). "
            "The class should also include basic validation annotations like @NotNull or @Size where applicable. "
            "Return only the Java class code without any extra explanation or comments, and ensure that the classes are structured to be used in a Quarkus application."
        )
    elif language.lower() == "node-api":
        framework_details = (
            "Generate complete Node.js script(s) based on the following API requirements. "
            "Ensure that the appropriate HTTP methods (GET, POST, etc.) are used for each operation, and that proper validation is implemented for input parameters where applicable. "
            "Include the necessary routes, controller logic, and any required business logic for the mathematical or data-processing operations described. "
            "Ensure that the Node.js script(s) use relevant libraries for HTTP requests, and handle errors appropriately. "
            "Return only the JavaScript code for the Node.js script(s) without any extra explanation or comments, ensuring the structure is suitable for use in a production-grade Node.js application."
        )
    elif language.lower() == ".net-api":
        framework_details = (
            "Generate complete C# class(s) based on the following API requirements. "
            "Ensure that the appropriate HTTP methods (GET, POST, etc.) are used for each operation, and that proper validation is implemented for input parameters where applicable. "
            "Include the necessary controllers, action methods, and any required business logic for the mathematical or data-processing operations described. "
            "Ensure that the .NET class(s) use relevant libraries for handling HTTP requests and responses, and handle errors appropriately. "
            "Return only the C# code for the .NET class(s) without any extra explanation or comments, ensuring the structure is suitable for use in a production-grade .NET application."
        ) 
    elif language.lower() == "springboot-api":
        framework_details = (
            "Generate complete Spring Boot Java class(s) based on the following API requirements. "
            "Ensure that the appropriate HTTP methods (GET, POST, etc.) are used for each operation, and that proper validation is implemented for input parameters where applicable. "
            "Include the necessary controllers, service classes, and any required business logic for the mathematical or data-processing operations described. "
            "Ensure that the Spring Boot class(s) use relevant libraries for handling HTTP requests, validation, and error handling. "
            "Return only the Java code for the Spring Boot clss(s) without any extra explanation or comments, ensuring the structure is suitable for use in a production-grade Spring Boot application."
        ) 
    elif language.lower() == "quarkus-api":
        framework_details = (
            "Generate complete Quarkus Java class(s) based on the following API requirements. "
            "Ensure that the appropriate HTTP methods (GET, POST, etc.) are used for each operation, and that proper validation is implemented for input parameters where applicable. "
            "Include the necessary REST controllers, service classes, and any required business logic for the mathematical or data-processing operations described. "
            "Ensure that the Quarkus class(s) use relevant libraries for handling HTTP requests, validation, and error handling, leveraging Quarkus' features like dependency injection and reactive programming. "
            "Return only the Java code for the Quarkus class(s) without any extra explanation or comments, ensuring the structure is suitable for use in a production-grade Quarkus application."
        )           
    else:
        return "ERROR: Unsupported programming language."

    # Construct the prompt
    prompt = f"{framework_details}\n\nRequirements:\n{requirements}"

    return query_llm(prompt)

def generate_requirements_from_code(language, code):
    """Generate requirements from the given application code."""
    if not code.strip():
        return "ERROR: Code input is empty."
    # remove API from the language if present
    #language = language.split("-")[0]
    # Define the reverse prompt
    # Define language-specific instructions
    if language.lower() == "react":
        reverse_prompt = (
            f"Analyze the following {language} application code and generate a consolidated list of UI-based system requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Ensure the requirements detail the UI components, state management, API interactions, and user actions."
            f"Do NOT include implementation details, technology, or framework-specific information.\n\n"
            f"Now analyze the following {language} code and generate a similar consolidated paragraph of UI-based system requirements.\n\n"
            f"Code:\n{code}"
        )

    elif language.lower() == "angular":
        reverse_prompt = (
            f"Analyze the following {language} application code and generate a consolidated list of UI-based system requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Ensure the requirements detail the UI components, routing behavior, API interactions, and user actions."
            f"Do NOT include implementation details, technology, or framework-specific information.\n\n"
            f"Now analyze the following {language} code and generate a similar consolidated paragraph of UI-based system requirements.\n\n"
            f"Code:\n{code}"
        )

    elif language.lower() == "sql":
        reverse_prompt = (
            f"Analyze the following {language} schema and generate a consolidated list of database design requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Ensure the requirements describe the tables, fields, data types, constraints, and relationships between tables (one-to-one, one-to-many, or many-to-many)."
            f"Do NOT describe queries, stored procedures, or functions—only focus on the data model.\n\n"
            f"Now analyze the following {language} schema and generate a similar consolidated paragraph of database design requirements.\n\n"
            f"Schema:\n{code}"
        )

    elif language.lower() == "springboot":
        reverse_prompt = (
            f"Analyze the following {language} entity classes and generate a consolidated list of system requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Ensure the requirements describe entity structures, attributes, relationships (one-to-one, one-to-many, many-to-many), and validation constraints."
            f"Do NOT describe implementation details, business logic, or API functionality—only focus on the data model.\n\n"
            f"Now analyze the following {language} entity classes and generate a similar consolidated paragraph of data model requirements.\n\n"
            f"Code:\n{code}"
        )

    elif language.lower() == ".net":
        reverse_prompt = (
            f"Analyze the following {language} entity classes and generate a consolidated list of system requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Ensure the requirements describe entity structures, attributes, relationships (one-to-one, one-to-many, many-to-many), and validation constraints."
            f"Do NOT describe implementation details, business logic, or API functionality—only focus on the data model.\n\n"
            f"Now analyze the following {language} entity classes and generate a similar consolidated paragraph of data model requirements.\n\n"
            f"Code:\n{code}"
        )

    elif language.lower() == "node":
        reverse_prompt = (
            f"Analyze the following {language} entity classes and generate a consolidated list of system requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Ensure the requirements describe entity structures, attributes, relationships (one-to-one, one-to-many, many-to-many), and validation constraints."
            f"Do NOT describe implementation details, business logic, or API functionality—only focus on the data model.\n\n"
            f"Now analyze the following {language} entity classes and generate a similar consolidated paragraph of data model requirements.\n\n"
            f"Code:\n{code}"
        )
    elif language.lower() == "quarkus":       
        reverse_prompt = (
            f"Analyze the following {language} entity classes and generate a consolidated list of system requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Ensure the requirements describe entity structures, attributes, relationships (one-to-one, one-to-many, many-to-many), and validation constraints."
            f"Do NOT describe implementation details, business logic, or API functionality—only focus on the data model.\n\n"
            f"Now analyze the following {language} entity classes and generate a similar consolidated paragraph of data model requirements.\n\n"
            f"Code:\n{code}"
        )
    elif language.lower() == "node-api":
        reverse_prompt = (
            f"Analyze the following {language} application code and generate a consolidated list of system requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Focus entirely on user actions and expected system behavior while **avoiding all technical details**. "
            f"DO NOT mention API, endpoints, HTTP methods, JSON, validation frameworks, database operations, libraries, or specific classes. "
            f"DO NOT describe implementation details like middleware, routing, or error handling mechanisms. "
            f"Instead, describe the system in terms of how users interact with it and what functionality is available to them.\n\n"
            f"Example:\n"
            f"**BAD**: 'The system shall provide a REST API with a /convert endpoint accepting GET and POST requests.'\n"
            f"**GOOD**: 'The system shall allow users to enter an amount and choose a currency to convert it into another currency.'\n\n"
            f"Now analyze the following {language} code and generate a similar consolidated paragraph of system requirements, ensuring that no programming-related terms, frameworks, or implementation details are included in the output.\n\n"
            f"Code:\n{code}"
        )
    elif language.lower() == ".net-api":
        reverse_prompt = (
            f"Analyze the following {language} application code and generate a consolidated list of system requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Focus entirely on user actions and expected system behavior while **avoiding all technical details**. "
            f"DO NOT mention API, endpoints, HTTP methods, JSON, validation frameworks, database operations, libraries, or specific classes. "
            f"DO NOT describe implementation details like middleware, routing, or error handling mechanisms. "
            f"Instead, describe the system in terms of how users interact with it and what functionality is available to them.\n\n"
            f"Example:\n"
            f"**BAD**: 'The system shall provide a REST API with a /convert endpoint accepting GET and POST requests.'\n"
            f"**GOOD**: 'The system shall allow users to enter an amount and choose a currency to convert it into another currency.'\n\n"
            f"Now analyze the following {language} code and generate a similar consolidated paragraph of system requirements, ensuring that no programming-related terms, frameworks, or implementation details are included in the output.\n\n"
            f"Code:\n{code}"
        )


    elif language.lower() == "springboot-api":
        reverse_prompt = (
            f"Analyze the following {language} application code and generate a consolidated list of system requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Focus entirely on user actions and expected system behavior while **avoiding all technical details**. "
            f"DO NOT mention API, endpoints, HTTP methods, JSON, validation frameworks, database operations, libraries, or specific classes. "
            f"DO NOT describe implementation details like middleware, routing, or error handling mechanisms. "
            f"Instead, describe the system in terms of how users interact with it and what functionality is available to them.\n\n"
            f"Example:\n"
            f"**BAD**: 'The system shall provide a REST API with a /convert endpoint accepting GET and POST requests.'\n"
            f"**GOOD**: 'The system shall allow users to enter an amount and choose a currency to convert it into another currency.'\n\n"
            f"Now analyze the following {language} code and generate a similar consolidated paragraph of system requirements, ensuring that no programming-related terms, frameworks, or implementation details are included in the output.\n\n"
            f"Code:\n{code}"
        )


    elif language.lower() == "quarkus-api":
        reverse_prompt = (
            f"Analyze the following {language} application code and generate a consolidated list of system requirements. "
            f"Return all requirements in a **single paragraph**, without line breaks or bullet points, starting each with 'The system shall'. "
            f"Focus entirely on user actions and expected system behavior while **avoiding all technical details**. "
            f"DO NOT mention API, endpoints, HTTP methods, JSON, database, frameworks, deployment platforms, logging tools, or testing strategies. "
            f"DO NOT include any references to specific programming languages, technologies, libraries, or development practices. "
            f"DO NOT describe implementation details like stored procedures, middleware, or system architecture. "
            f"Instead, describe the system in terms of how users interact with it and what functionality is available to them.\n\n"
            f"Example:\n"
            f"**BAD**: 'The system shall provide a REST API with a /convert endpoint accepting GET and POST requests.'\n"
            f"**GOOD**: 'The system shall allow users to enter an amount and choose a currency to convert it into another currency.'\n\n"
            f"Now analyze the following {language} code and generate a similar consolidated paragraph of system requirements, ensuring that no programming-related terms, frameworks, or implementation details are included in the output.\n\n"
            f"Code:\n{code}"
        )

    else:
        return "ERROR: Unsupported programming language."    

    return query_llm(reverse_prompt)

def generate_json_output(language, requirements):
    """Generate JSON output with the required information."""
    generated_code = generate_app_code(language, requirements)

    if generated_code.startswith("ERROR"):
        return {"error": generated_code}
    extracted_requirements = ""
    extracted_requirements = generate_requirements_from_code(language, generated_code)

    if extracted_requirements.startswith("ERROR"):
        return {"error": extracted_requirements}

    # Create a dictionary to hold the results
    result = {
        "input_requirements": requirements,
        "generated_code": generated_code,
        "reverse_generated_requirements": extracted_requirements
    }

    return result


# The following lines are for invoking this script from another script
if __name__ == "__main__":
    # For testing: To simulate calling from another script
    language = sys.argv[1] if len(sys.argv) > 1 else "react"
    requirements = sys.argv[2] if len(sys.argv) > 2 else "The system shall allow users to log in using their email and password."
    #print(f"******* Inside reverse generation :: {language} :: {requirements}\n\n")   
    # Generate JSON output
    json_output = generate_json_output(language, requirements)
    
    # Print the result as JSON for use by another script
    print(json.dumps(json_output, indent=4))
