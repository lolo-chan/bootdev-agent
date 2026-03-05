import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()


def main():
    print("Hello from bootdev-agent!\nStarting LLM.")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt,
                                            temperature=0,
                                            tools=[available_functions]),
        )
        if  response.candidates:
            for i in response.candidates:
                messages.append(i.content)
        if response.usage_metadata is None:
            raise RuntimeError("API call likely failed.")
        
        if response.function_calls:
            function_results = []
            function_calls = response.function_calls
            for function_call in function_calls:
                function_call_result = call_function(function_call)
                if not function_call_result.parts:
                    raise Exception
                if function_call_result.parts[0].function_response is None:
                    raise Exception
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
        else:
            break

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
        print(response.text)
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
