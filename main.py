import os

from dotenv import load_dotenv
from google import genai


def main() -> None:
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="How to get a random point in an area in Godot using GDScript? Use one paragraph maximum.",
        )
        print(response.text)

    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    main()