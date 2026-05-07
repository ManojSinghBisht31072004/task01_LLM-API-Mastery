import os
from datetime import datetime, timezone
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def chat(user_message: str) -> dict:
    response = model.generate_content(user_message)

    input_tokens  = response.usage_metadata.prompt_token_count
    output_tokens = response.usage_metadata.candidates_token_count
    total_tokens  = response.usage_metadata.total_token_count

    timestamp = datetime.now(timezone.utc).isoformat()
    print("─" * 45)
    print(f"[TOKEN LOG] {timestamp}")
    print(f"  Prompt tokens    : {input_tokens}")
    print(f"  Completion tokens: {output_tokens}")
    print(f"  Total tokens     : {total_tokens}")
    print("─" * 45)

    return {
        "content": response.text,
        "tokens": {
            "prompt":     input_tokens,
            "completion": output_tokens,
            "total":      total_tokens,
        }
    }