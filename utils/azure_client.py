import os
import re
from dotenv import load_dotenv

load_dotenv()


def azure_ai_enabled():
    """
    Checks whether Azure AI mode is enabled.
    Keep USE_AZURE_AI=false while developing locally.
    """
    return os.getenv("USE_AZURE_AI", "false").lower() == "true"


def get_azure_config():
    """
    Returns Azure AI Foundry configuration from environment variables.
    This avoids hardcoding secrets or endpoints in app.py.
    """
    return {
        "project_endpoint": os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        "model_deployment": os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "gpt-4o"),
        "subscription_id": os.getenv("AZURE_SUBSCRIPTION_ID"),
        "resource_group": os.getenv("AZURE_RESOURCE_GROUP"),
        "project_name": os.getenv("AZURE_AI_PROJECT_NAME"),
    }


def _has_configured_endpoint(project_endpoint: str | None) -> bool:
    return bool(project_endpoint) and project_endpoint != "your_project_endpoint_here"


def azure_foundry_status():
    """
    Reports the current Foundry integration state honestly.

    This app does not make live Azure model calls yet, so a configured endpoint is
    shown as a Foundry-ready placeholder instead of an enabled integration.
    """
    if not azure_ai_enabled():
        return {
            "state": "local",
            "label": "Local Prototype",
            "detail": "Using safe local rule-based recommendations only.",
        }

    config = get_azure_config()

    if not _has_configured_endpoint(config["project_endpoint"]):
        return {
            "state": "missing_config",
            "label": "Foundry Config Missing",
            "detail": "USE_AZURE_AI=true, but no usable AZURE_AI_PROJECT_ENDPOINT is configured.",
        }

    return {
        "state": "placeholder",
        "label": "Foundry-Ready Placeholder",
        "detail": "Foundry configuration is present, but no live Azure model call is implemented.",
    }


def _extract_prompt_fields(prompt: str) -> dict:
    """
    Pulls simple key-value fields from the synthetic prompt.
    This keeps local mode useful without calling external services.
    """
    fields = {}

    for line in prompt.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

    return fields


def _extract_number(value: str, default: int = 0) -> int:
    match = re.search(r"-?\d+", value or "")

    if not match:
        return default

    return int(match.group())


def _build_local_recommendation(prompt: str) -> str:
    fields = _extract_prompt_fields(prompt)

    learner = fields.get("Learner", "This learner")
    certification = fields.get("Certification", "the target certification")
    risk_level = fields.get("Risk Level", "Unknown Risk")
    primary_constraint = fields.get(
        "Primary Constraint",
        "Use the local readiness signals to decide the next step.",
    )
    preferred_slot = fields.get("Preferred Learning Slot", "the preferred learning slot")
    score = _extract_number(fields.get("Practice Score", "0"))
    target = _extract_number(fields.get("Passing Practice Score", "75"), 75)
    focus_hours = _extract_number(fields.get("Focus Hours/Week", "0"))
    meeting_hours = _extract_number(fields.get("Meeting Hours/Week", "0"))

    if score < target:
        coaching_action = (
            f"prioritize weak-topic review until the practice score closes the {target - score}-point readiness gap"
        )
    elif risk_level == "Low Risk":
        coaching_action = "complete a final practice assessment and preserve the current study rhythm"
    else:
        coaching_action = "continue targeted review and confirm readiness with another practice check"

    if meeting_hours > 20 or focus_hours < 12:
        workload_action = (
            f"use shorter protected study blocks in the {preferred_slot.lower()} slot because workload capacity is constrained"
        )
    else:
        workload_action = (
            f"use the {preferred_slot.lower()} slot for deeper certification practice and scenario review"
        )

    return (
        "Local rule-based recommendation: "
        f"{learner} is currently classified as {risk_level} for {certification}. "
        f"Primary reasoning signal: {primary_constraint} "
        f"Recommended next step: {coaching_action}; {workload_action}. "
        "This is a synthetic coaching recommendation and does not guarantee exam outcome."
    )


def generate_ai_recommendation(prompt: str) -> str:
    """
    Placeholder function for Azure AI Foundry recommendation generation.

    Current behavior:
    - If Azure AI is disabled, returns a safe local rule-based recommendation.
    - Later, we will replace this with real Microsoft Foundry model calls.
    """

    if not azure_ai_enabled():
        return _build_local_recommendation(prompt)

    config = get_azure_config()

    if not _has_configured_endpoint(config["project_endpoint"]):
        return (
            "Foundry Config Missing: USE_AZURE_AI is true, but no usable "
            "AZURE_AI_PROJECT_ENDPOINT is configured. No Azure model call was made."
        )

    return (
        "Foundry-ready placeholder: configuration was detected, but this demo does not "
        "make a live Azure model call yet. The recommendation remains local and synthetic."
    )