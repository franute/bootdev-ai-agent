import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("Openrouter API key not found!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    print(f"User prompt: {args.user_prompt}")

    messages : List[dict[str, str]] = [
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if response.usage is not None:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print(f"Response:\n{response.choices[0].message.content}")

if __name__ == "__main__":
    main()
