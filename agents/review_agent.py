"""
review_agent.py

Review Agent — QA Artifact Compression Workflow v1

Runtime behaviour:
- Model:       gpt-4o
- Temperature: 0
- Input:       Reads intake_output.json and risk_output.json from sample_output/
- Prompt:      Reads system prompt from prompts/review_prompt.md
- Output:      Saves rendered Markdown test plan to sample_output/

Note: File-based handoff is a testing convenience for v1, not a production
pattern. In a production system both inputs would be passed as a single
structured payload, not read from disk separately.

Usage:
    python agents/review_agent.py

Dependencies:
    pip install openai python-dotenv
"""

import json
import os
from datetime import date
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
PROMPT_PATH = Path("prompts/review_prompt.md")

# --- Input folder --- uncomment the one you want to run
# INPUT_FOLDER = Path("sample_output/prd_messy")
INPUT_FOLDER = Path("sample_output/prd_clean_agile")
# INPUT_FOLDER = Path("sample_output/raw_prd_notes")

INTAKE_PATH = INPUT_FOLDER / "intake_output.json"
RISK_PATH = INPUT_FOLDER / "risk_output.json"
OUTPUT_PATH = INPUT_FOLDER / "test_plan.md"

# --- Load system prompt ---
def load_system_prompt(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# --- Load intake and risk outputs ---
def load_inputs(intake_path: Path, risk_path: Path) -> tuple:
    with open(intake_path, "r") as f:
        intake = json.load(f)
    with open(risk_path, "r") as f:
        risk = json.load(f)
    return intake, risk

# --- Build user message ---
def build_user_message(intake: dict, risk: list, folder_name: str) -> str:
    artifact_id = f"aqab-v1-{folder_name}"
    prd_source = f"{folder_name}.md"
    generated = date.today().isoformat()

    return (
        f"Here are the two inputs to render:\n\n"
        f"INTAKE OUTPUT:\n{json.dumps(intake, indent=2, ensure_ascii=False)}\n\n"
        f"RISK OUTPUT:\n{json.dumps(risk, indent=2, ensure_ascii=False)}\n\n"
        f"Artifact ID: {artifact_id}\n"
        f"PRD Source: {prd_source}\n"
        f"Generated: {generated}"
    )

# --- Call the model ---
def run_review_agent(system_prompt: str, user_message: str) -> str:
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
    raw_output = raw_output.replace("\u00e2\u0080\u0094", "\u2014")
    return raw_output.strip()

# --- Save output ---
def save_output(content: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Output saved to {path}")

# --- Validate output ---
def validate_output(content: str) -> None:
    assert "# QA Test Plan" in content, "Missing: QA Test Plan header"
    assert "## Purpose" in content, "Missing: Purpose section"
    assert "## In Scope" in content, "Missing: In Scope section"
    assert "## Out of Scope" in content, "Missing: Out of Scope section"
    assert "## Review Decision" in content, "Missing: Review Decision section"
    print("Validation passed. Test plan rendered successfully.")

# --- Main ---
def main():
    print("Loading system prompt...")
    system_prompt = load_system_prompt(PROMPT_PATH)

    print(f"Loading inputs from {INPUT_FOLDER}...")
    intake, risk = load_inputs(INTAKE_PATH, RISK_PATH)

    print("Building user message...")
    folder_name = INPUT_FOLDER.name
    user_message = build_user_message(intake, risk, folder_name)

    print("Calling Review Agent...")
    output = run_review_agent(system_prompt, user_message)

    print("Validating output...")
    validate_output(output)

    print("Saving output...")
    save_output(output, OUTPUT_PATH)

if __name__ == "__main__":
    main()