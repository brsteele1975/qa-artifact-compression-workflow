"""
risk_agent.py

Risk Agent — QA Artifact Compression Workflow v1

Runtime behaviour:
- Model:       gpt-4o
- Temperature: 0
- Input:       Reads Intake Agent output from sample_output/
- Prompt:      Reads system prompt from prompts/risk_prompt.md
- Output:      Saves risk-annotated test plan to sample_output/

Note: File-based handoff is a testing convenience for v1, not a production
pattern. In a production system the requirements array would be passed
explicitly as a structured payload, not read from disk.

Usage:
    python agents/risk_agent.py

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
PROMPT_PATH = Path("prompts/risk_prompt.md")

# --- Input file --- uncomment the one you want to run
# INPUT_PATH = Path("sample_output/prd_messy/intake_output.json")
INPUT_PATH = Path("sample_output/prd_clean_agile/intake_output.json")
# INPUT_PATH = Path("sample_output/raw_prd_notes/intake_output.json")

# Derive output filename from input
OUTPUT_PATH = Path(f"sample_output/{INPUT_PATH.parent.name}/risk_output.json")

# --- Load system prompt ---
def load_system_prompt(path: Path) -> str:
    with open(path, "r") as f:
        return f.read()

# --- Load and extract requirements and project_context from Intake Agent output ---
def load_requirements(path: Path) -> tuple:
    with open(path, "r") as f:
        intake_output = json.load(f)
    return intake_output["requirements"], intake_output.get("project_context", None)

# --- Build user message ---
def build_user_message(requirements: list, project_context: dict) -> str:
    return (
        f"Here are the inputs to process:\n\n"
        f"PROJECT CONTEXT:\n{json.dumps(project_context, indent=2)}\n\n"
        f"REQUIREMENTS:\n{json.dumps(requirements, indent=2)}"
    )

# --- Call the model ---
def run_risk_agent(system_prompt: str, user_message: str) -> list:
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
def save_output(data: list, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Output saved to {path}")

# --- Validate output structure ---
def validate_output(data: list) -> None:
    assert isinstance(data, list), "Output must be a JSON array"

    all_tc_ids = []

    for entry in data:
        assert "req_id" in entry, f"Missing req_id in: {entry}"
        assert "risk" in entry, f"Missing risk in: {entry}"
        assert "severity" in entry, f"Missing severity in: {entry}"
        assert "severity_locked" in entry, f"Missing severity_locked in: {entry}"
        assert "test_cases" in entry, f"Missing test_cases in: {entry}"

        for tc in entry["test_cases"]:
            assert "tc_id" in tc, f"Missing tc_id in: {tc}"
            assert "type" in tc, f"Missing type in: {tc}"
            assert "surface" in tc, f"Missing surface in: {tc}"
            assert tc["type"] in ["unit", "integration", "e2e", "exploratory", "non_functional"], \
                f"Invalid type value: {tc['type']}"
            assert tc["surface"] in ["ui", "api", "service", "workflow"], \
                f"Invalid surface value: {tc['surface']}"
            all_tc_ids.append(tc["tc_id"])

    tc_count = len(all_tc_ids)
    req_count = len(data)
    print(f"Validation passed. {req_count} requirements processed, {tc_count} test cases generated.")

# --- Main ---
def main():
    print("Loading system prompt...")
    system_prompt = load_system_prompt(PROMPT_PATH)

    print(f"Loading requirements from {INPUT_PATH}...")
    requirements, project_context = load_requirements(INPUT_PATH)

    print("Building user message...")
    user_message = build_user_message(requirements, project_context)

    print("Calling Risk Agent...")
    output = run_risk_agent(system_prompt, user_message)

    print("Validating output...")
    validate_output(output)

    print("Saving output...")
    save_output(output, OUTPUT_PATH)

if __name__ == "__main__":
    main()