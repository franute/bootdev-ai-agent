import argparse
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("Openrouter API key not found!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    messages : List[dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    final_response: bool = False

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            #temperature=0
        )

        if response.usage is not None:
            if args.verbose:
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")

        print(f"Response:\n{response.choices[0].message.content}")

        response_message = response.choices[0].message
        messages.append(response_message)

        if not response_message.tool_calls:
            final_response = True
            print(f"-> {response_message}")
            break
        else:
            for tool_call in response_message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")
                result_message = call_function(tool_call, function_args)

                if result_message["content"] is None:
                    raise Exception("Empty content returned by function")

                messages.append(result_message)

                if args.verbose:
                    print(f"-> {result_message['content']}")

    if not final_response:
        print("We couldn't reach a final answer to your prompt")
        return 1

    return 0

if __name__ == "__main__":
    main()
