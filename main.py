import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentResponse
import sys
from app.config import MAX_ITERATIONS
from app.prompts import system_prompt
from app.function_declarations import available_functions
from functions.call_function import call_function


def main() -> None:
    load_dotenv()
    args: list[str] = sys.argv[1:]

    if not args:
        print("LLMMM code assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    prompt: str = " ".join([arg for arg in args if not arg.startswith("--")])
    flags: list[str] = [arg for arg in args if arg.startswith("--")]

    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    client: genai.Client = genai.Client(api_key=api_key)

    if "--verbose" in flags:
        print(f"User prompt: {prompt}")

    messages: list[types.ContentUnion] = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    for i in range(MAX_ITERATIONS):
        if i == MAX_ITERATIONS - 1:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, flags)

            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as err:
            print(f"Error in generate_content: {err}")


def generate_content(
    client: genai.Client, messages: list[types.ContentUnion], flags: list[str]
) -> str | None:

    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    verbose = "--verbose" in flags
    if verbose and response.usage_metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response:")

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content is None:
                continue
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_calls: types.ContentListUnion = []
    for call in response.function_calls:
        result = call_function(call, verbose=verbose)

        if (
            not result
            or not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise Exception("Unable to execute the code")

        if verbose:
            print(f"-> {result.parts[0].function_response.response}")

        function_calls.append(result)

    if not function_calls:
        print("Cannot get a response from the server.")
        sys.exit(1)


if __name__ == "__main__":
    main()
