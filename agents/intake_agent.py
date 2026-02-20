"""
intake_agent.py

Intake Agent — QA Artifact Compression Workflow v1

Runtime behaviour:
- Model:       gpt-4o
- Temperature: 0
- Input:       Reads PRD from sample_input/prd.md
- Prompt:      Reads system prompt from prompts/intake_prompt.md
- Output:      Saves structured JSON to sample_output/intake_output.json

Usage:
    python agents/intake_agent.py

Dependencies:
    pip install openai python-dotenv
"""

import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
# The paths below were used for isolated agent testing during development
# PROMPT_PATH = Path("prompts/intake_prompt.md")
# --- Input file --- uncomment the one you want to run
# INPUT_PATH = Path("sample_input/prd_messy.md")
# INPUT_PATH = Path("sample_input/prd_clean_agile.md")
# INPUT_PATH = Path("sample_input/raw_prd_notes.md")
# OUTPUT_PATH = Path(f"sample_output/{INPUT_PATH.stem}/intake_output.json")

# --- Load system prompt ---
def load_system_prompt(path: Path) -> str:
    with open(path, "r") as f:
        return f.read()

# --- Load PRD ---
def load_prd(path: Path) -> str:
    with open(path, "r") as f:
        return f.read()

# --- Build user message ---
def build_user_message(prd_content: str) -> str:
    return f"Here is the PRD to parse:\n\n{prd_content}"

# --- Call the model ---
def run_intake_agent(system_prompt: str, user_message: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    raw_output = response.choices[0].message.content or ""
    raw_output = raw_output.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model output was not valid JSON.\n\nRaw output:\n{raw_output}") from e

# --- Save output ---
def save_output(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Output saved to {path}")

# --- Validate output structure ---
def validate_output(data: dict) -> None:
    assert "plan_context" in data, "Missing: plan_context"
    assert "purpose" in data["plan_context"], "Missing: plan_context.purpose"
    assert "in_scope" in data["plan_context"], "Missing: plan_context.in_scope"
    assert "out_of_scope" in data["plan_context"], "Missing: plan_context.out_of_scope"
    assert "requirements" in data, "Missing: requirements"

    for req in data["requirements"]:
        assert "req_id" in req, f"Missing req_id in: {req}"
        assert "prd_ref" in req, f"Missing prd_ref in: {req}"
        assert "ambiguity_flags" in req, f"Missing ambiguity_flags in: {req}"

    print(f"Validation passed. {len(data['requirements'])} requirements parsed.")


# # --- Main ---
# Preserved for reference. Use run_pipeline.py to run the full pipeline.
# def main():
#     print("Loading system prompt...")
#     system_prompt = load_system_prompt(PROMPT_PATH)

#     print("Loading PRD...")
#     prd_content = load_prd(INPUT_PATH)

#     print("Building user message...")
#     user_message = build_user_message(prd_content)

#     print("Calling Intake Agent...")
#     output = run_intake_agent(system_prompt, user_message)

#     print("Validating output...")
#     validate_output(output)

#     print("Saving output...")
#     save_output(output, OUTPUT_PATH)

# if __name__ == "__main__":
#     main()
