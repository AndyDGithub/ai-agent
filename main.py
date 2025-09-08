import os
from dotenv import load_dotenv
from google import genai
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def main():
    print("Hello from ai-agent!")
    verbose = False

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Write to files
    - Run Python files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    question = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    if len(sys.argv) > 1:
        question = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            verbose = True
    else:
        print("Error: a question needs to be asked")
        sys.exit(1)

    # Initialize message history
    messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=question)])]

    try:
        for i in range(20):
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=genai.types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )

            if verbose:
                print(f"\nIteration {i+1}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            # Add model response to messages
            for candidate in response.candidates:
                messages.append(candidate.content)

            # Handle function calls
            if response.function_calls:
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call, verbose=verbose)

                    result_data = function_call_result.parts[0].function_response.response
                    if not result_data:
                        raise RuntimeError("Fatal: No function response returned.")

                    if verbose:
                        print(f"-> {result_data}")

                    # Add tool result to messages as if user responded
                    messages.append(function_call_result)
            else:
                # No function calls - model is done
                if response.text:
                    print("\nFinal response:\n" + response.text)
                else:
                    print("\nFinal response: (no text returned)")
                break
        else:
            print("Max iterations reached without final response.")

    except Exception as e:
        print(f"Agent crashed: {str(e)}")

if __name__ == "__main__":
    main()
