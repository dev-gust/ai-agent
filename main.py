import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    generate_content(client, messages, args.user_prompt, args.verbose)

def generate_content(client: genai.Client, messages: list[types.Content], prompt: str, verbose: bool = False) -> None:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
        )
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")

        user_prompt = prompt
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        print("Response:")
        print(response.text)
        
    except Exception as e:
        print(f"Request failed: {e}")
        raise

if __name__ == "__main__":
    main()