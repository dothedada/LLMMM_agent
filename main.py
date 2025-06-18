from typing import List
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentResponse
import sys
from app.prompts import system_prompt
from app.function_declarations import available_functions


def main() -> None:
    load_dotenv()
    args: List[str] = sys.argv[1:]

    if not args:
        print("LLMMM code assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    prompt: str = " ".join([arg for arg in args if not arg.startswith("--")])
    flags: List[str] = [arg for arg in args if arg.startswith("--")]

    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    client: genai.Client = genai.Client(api_key=api_key)

    if "--verbose" in flags:
        print(f"User prompt: {prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    generate_content(client, messages, flags)


def generate_content(
    client: genai.Client, messages: List[types.Content], flags: List[str]
) -> None:
    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if response and response.usage_metadata:
        if "--verbose" in flags:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print("Response:")

        if response.function_calls:
            for call in response.function_calls:
                print(f"Calling function: {call.name}({call.args})")
        else:
            print(response.text)

    else:
        print("Cannot get a response from the server.")
        sys.exit(1)


if __name__ == "__main__":
    main()
