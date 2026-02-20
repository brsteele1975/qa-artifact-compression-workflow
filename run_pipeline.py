"""
run_pipeline.py

Phase 1 Pipeline Runner — QRAFT v1

Chains the three Phase 1 agents in sequence:
    Intake Agent → Risk Agent → Review Agent → test_plan.md

A failure in any agent stops the pipeline immediately and reports
the error with context. No partial outputs are treated as success.

Usage:
    python run_pipeline.py <path-to-prd>

Example:
    python run_pipeline.py sample_input/prd_clean_agile.md

Dependencies:
    pip install openai python-dotenv
"""

import json
import os
import sys
from datetime import date
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------

def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        _fail("OPENAI_API_KEY is not set. Add it to your .env file.")
    return OpenAI(api_key=api_key)


def load_prompt(path: Path) -> str:
    if not path.exists():
        _fail(f"Prompt file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_json_output(raw: str, agent_name: str):
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        _fail(
            f"{agent_name} returned output that could not be parsed as JSON.\n\n"
            f"Parse error: {e}\n\n"
            f"Raw output:\n{cleaned}"
        )


def save_json(data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def save_text(content: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _fail(message: str) -> None:
    print(f"\n❌  Pipeline failed.\n\n{message}\n", file=sys.stderr)
    sys.exit(1)


def _step(message: str) -> None:
    print(f"   {message}")


def _header(title: str) -> None:
    print(f"\n── {title}")


# ---------------------------------------------------------------------------
# Intake Agent
# ---------------------------------------------------------------------------

def run_intake_agent(client: OpenAI, prd_path: Path, output_path: Path) -> dict:
    _header("Intake Agent")

    _step("Loading prompt...")
    system_prompt = load_prompt(Path("prompts/intake_prompt.md"))

    _step(f"Loading PRD from {prd_path}...")
    if not prd_path.exists():
        _fail(f"PRD file not found: {prd_path}")
    with open(prd_path, "r", encoding="utf-8") as f:
        prd_content = f.read()

    _step("Calling model...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the PRD to parse:\n\n{prd_content}"},
            ],
        )
    except Exception as e:
        _fail(f"Intake Agent API call failed.\n\nError: {e}")

    raw = response.choices[0].message.content or ""
    output = parse_json_output(raw, "Intake Agent")

    _step("Validating output...")
    _validate_intake(output)

    _step(f"Saving output to {output_path}...")
    save_json(output, output_path)

    req_count = len(output.get("requirements", []))
    print(f"   ✓  Intake complete. {req_count} requirements parsed.")
    return output


def _validate_intake(data: dict) -> None:
    missing = []
    if "plan_context" not in data:
        missing.append("plan_context")
    else:
        for field in ["purpose", "in_scope", "out_of_scope"]:
            if field not in data["plan_context"]:
                missing.append(f"plan_context.{field}")
    if "requirements" not in data:
        missing.append("requirements")
    else:
        for req in data["requirements"]:
            for field in ["req_id", "prd_ref", "ambiguity_flags"]:
                if field not in req:
                    missing.append(f"{req.get('req_id', 'unknown')}.{field}")

    if missing:
        _fail(f"Intake Agent output failed validation.\n\nMissing fields: {', '.join(missing)}")


# ---------------------------------------------------------------------------
# Risk Agent
# ---------------------------------------------------------------------------

def run_risk_agent(client: OpenAI, intake_output: dict, output_path: Path) -> list:
    _header("Risk Agent")

    _step("Loading prompt...")
    system_prompt = load_prompt(Path("prompts/risk_prompt.md"))

    requirements = intake_output.get("requirements", [])
    project_context = intake_output.get("project_context", None)

    _step("Building user message...")
    user_message = (
        f"Here are the inputs to process:\n\n"
        f"PROJECT CONTEXT:\n{json.dumps(project_context, indent=2)}\n\n"
        f"REQUIREMENTS:\n{json.dumps(requirements, indent=2)}"
    )

    _step("Calling model...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
    except Exception as e:
        _fail(f"Risk Agent API call failed.\n\nError: {e}")

    raw = response.choices[0].message.content or ""
    output = parse_json_output(raw, "Risk Agent")

    _step("Validating output...")
    _validate_risk(output)

    _step(f"Saving output to {output_path}...")
    save_json(output, output_path)

    tc_count = sum(len(entry.get("test_cases", [])) for entry in output)
    print(f"   ✓  Risk complete. {len(output)} requirements processed, {tc_count} test cases generated.")
    return output


def _validate_risk(data: list) -> None:
    if not isinstance(data, list):
        _fail("Risk Agent output failed validation.\n\nExpected a JSON array but got something else.")

    errors = []
    valid_types = {"unit", "integration", "e2e", "exploratory", "non_functional"}
    valid_surfaces = {"ui", "api", "service", "workflow"}

    for entry in data:
        req_id = entry.get("req_id", "unknown")
        for field in ["req_id", "risk", "severity", "severity_locked", "test_cases"]:
            if field not in entry:
                errors.append(f"{req_id}: missing field '{field}'")
        for tc in entry.get("test_cases", []):
            tc_id = tc.get("tc_id", "unknown")
            if "type" not in tc:
                errors.append(f"{tc_id}: missing field 'type'")
            elif tc["type"] not in valid_types:
                errors.append(f"{tc_id}: invalid type '{tc['type']}'")
            if "surface" not in tc:
                errors.append(f"{tc_id}: missing field 'surface'")
            elif tc["surface"] not in valid_surfaces:
                errors.append(f"{tc_id}: invalid surface '{tc['surface']}'")

    if errors:
        _fail(f"Risk Agent output failed validation.\n\n" + "\n".join(errors))


# ---------------------------------------------------------------------------
# Review Agent
# ---------------------------------------------------------------------------

def run_review_agent(client: OpenAI, intake_output: dict, risk_output: list, folder_name: str, output_path: Path) -> None:
    _header("Review Agent")

    _step("Loading prompt...")
    system_prompt = load_prompt(Path("prompts/review_prompt.md"))

    _step("Building user message...")
    user_message = (
        f"Here are the two inputs to render:\n\n"
        f"INTAKE OUTPUT:\n{json.dumps(intake_output, indent=2, ensure_ascii=False)}\n\n"
        f"RISK OUTPUT:\n{json.dumps(risk_output, indent=2, ensure_ascii=False)}\n\n"
        f"Artifact ID: qraft-v1-{folder_name}\n"
        f"PRD Source: {folder_name}.md\n"
        f"Generated: {date.today().isoformat()}"
    )

    _step("Calling model...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
    except Exception as e:
        _fail(f"Review Agent API call failed.\n\nError: {e}")

    raw = response.choices[0].message.content or ""
    output = raw.replace("\u00e2\u0080\u0094", "\u2014").strip()

    _step("Validating output...")
    _validate_review(output)

    _step(f"Saving output to {output_path}...")
    save_text(output, output_path)

    print(f"   ✓  Review complete. Test plan saved to {output_path}.")


def _validate_review(content: str) -> None:
    required_sections = [
        "## Purpose",
        "## In Scope",
        "## Out of Scope",
        "## Review Decision",
    ]
    missing = [s for s in required_sections if s not in content]
    if missing:
        _fail(f"Review Agent output failed validation.\n\nMissing sections: {', '.join(missing)}")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_pipeline.py <path-to-prd>", file=sys.stderr)
        print("Example: python run_pipeline.py sample_input/prd_clean_agile.md", file=sys.stderr)
        sys.exit(1)

    prd_path = Path(sys.argv[1])
    folder_name = prd_path.stem
    output_dir = Path(f"output/{folder_name}")

    intake_output_path = output_dir / "intake_output.json"
    risk_output_path = output_dir / "risk_output.json"
    test_plan_path = output_dir / "test_plan.md"

    print(f"\nQRAFT — Phase 1 Pipeline")
    print(f"Input:  {prd_path}")
    print(f"Output: {output_dir}/")

    client = get_openai_client()

    intake_output = run_intake_agent(client, prd_path, intake_output_path)
    risk_output = run_risk_agent(client, intake_output, risk_output_path)
    run_review_agent(client, intake_output, risk_output, folder_name, test_plan_path)

    print(f"\n✓  Pipeline complete. Test plan ready for human review at {test_plan_path}\n")


if __name__ == "__main__":
    main()