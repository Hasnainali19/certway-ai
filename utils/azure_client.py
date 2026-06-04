import os
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


def generate_ai_recommendation(prompt: str) -> str:
    """
    Placeholder function for Azure AI Foundry recommendation generation.

    Current behavior:
    - If Azure AI is disabled, returns a safe local fallback message.
    - Later, we will replace this with real Microsoft Foundry model calls.
    """

    if not azure_ai_enabled():
        return (
            "Azure AI Foundry mode is currently disabled. "
            "This response is generated using the local rule-based multi-agent prototype. "
            "Enable USE_AZURE_AI=true in a local .env file after configuring Azure AI Foundry."
        )

    config = get_azure_config()

    if not config["project_endpoint"]:
        return (
            "Azure AI Foundry is enabled, but AZURE_AI_PROJECT_ENDPOINT is missing. "
            "Please add the endpoint to your local .env file."
        )

    return (
        "Azure AI Foundry integration placeholder is active. "
        "The next version will connect this function to your deployed Foundry model."
    )