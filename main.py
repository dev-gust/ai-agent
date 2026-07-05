import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "user", "content": args.user_prompt},
    ]
    generate_content(client, messages, args.user_prompt, args.verbose)

def generate_content(client: OpenAI, messages: list, prompt: str, verbose: bool = False) -> None:
    try:
        response =  client.chat.completions.create(
            model="openrouter/free", # https://openrouter.ai/models?max_price=0
            messages=messages,
        )
        if not response.usage:
            raise RuntimeError("API response appears to be malformed")

        if verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        print("Response:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Request failed: {e}")
        raise

if __name__ == "__main__":
    main()