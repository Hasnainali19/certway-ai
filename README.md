# Certway AI

Certway AI is a Microsoft Foundry-ready multi-agent certification coach for enterprise learning and workforce readiness.

The project helps employees prepare for role-based certifications by recommending learning paths, generating workload-aware study plans, creating practice assessments, estimating readiness risk, and giving managers team-level insights.

## Hackathon Track

**Agents League Hackathon — Reasoning Agents Track**

This project is designed for the Reasoning Agents challenge and demonstrates:

- Multi-agent system design
- Role-based certification planning
- Workload-aware study scheduling
- Grounded practice assessment using synthetic knowledge documents
- Manager-level readiness insights
- Safe synthetic data usage
- Microsoft Foundry / Azure AI Foundry-ready architecture

## Problem

Organizations often struggle to manage internal certification programs because:

- Employees do not know what to study first.
- Study plans are not personalized to role or workload.
- Managers lack visibility into certification readiness.
- Practice questions may be generic or ungrounded.
- Learning progress is difficult to track across teams.

## Solution

Certway AI uses multiple specialized agents to support employees and managers throughout the certification preparation process.

## Multi-Agent Architecture

### 1. Orchestrator Agent
Receives learner or manager requests and coordinates the workflow across specialized agents.

### 2. Learning Path Curator Agent
Maps a learner's role and certification goal to relevant learning topics.

### 3. Study Plan Generator Agent
Creates a realistic study plan based on practice score, hours studied, focus time, and meeting load.

### 4. Assessment Agent
Generates practice questions and readiness recommendations based on approved synthetic certification content.

### 5. Engagement Agent
Suggests study timing and support strategies based on workload signals.

### 6. Manager Insights Agent
Summarizes team-level readiness, risk areas, and recommended manager actions.

## Microsoft IQ / Foundry Alignment

This prototype uses a synthetic certification guide as an approved knowledge source to demonstrate a Foundry IQ-style grounding pattern.

<!-- The file:

```text
docs/engineering_certification_guide.md -->


## Azure AI Foundry Integration

The project includes an Azure AI Foundry-ready placeholder client:

```text
utils/azure_client.py
```

Current mode:

* Local rule-based multi-agent prototype
* Azure AI Foundry placeholder
* Safe fallback if Azure is not configured
* Environment-based setup using `.env.example`

The environment template is provided in:

```text
.env.example
```

Real Azure values should be stored in a local `.env` file and should never be committed to GitHub.

## Synthetic Data

This project uses synthetic demo data only.

Datasets:

```text
data/learners.csv
data/workload_signals.csv
data/certifications.csv
```

No real employee data, customer data, credentials, confidential data, or personally identifiable information is used.

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* Azure AI Foundry-ready architecture
* GitHub
* GitHub Copilot
* VS Code

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Hasnainali19/certway-ai.git
cd certway-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

## Environment Variables

Copy `.env.example` to `.env` if using Azure AI Foundry.

On Windows:

```bash
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

Then update the `.env` file with your real Azure values.

Do not commit `.env`.

## Responsible AI and Safety

Certway AI follows these safety practices:

* Uses synthetic data only
* Avoids real employee or customer data
* Does not expose credentials or secrets
* Provides readiness recommendations, not guaranteed outcomes
* Encourages human review for important workforce decisions
* Clearly separates local prototype mode from Azure AI Foundry mode

## GitHub Copilot Usage

GitHub Copilot was used during development to support:

* Streamlit UI generation
* Python helper function creation
* Multi-agent workflow documentation
* Debugging and code explanation
* README drafting and refinement

## Demo Flow

A sample demo flow:

1. Open the Streamlit app.
2. View the overview dashboard.
3. Select a learner in the Learner Coach page.
4. Review the multi-agent workflow trace.
5. Review the readiness reasoning and study plan.
6. Open the Practice Assessment page.
7. View the grounded synthetic certification guide.
8. Review practice questions.
9. Open the Manager Dashboard.
10. Review team-level readiness and risk insights.

## Project Status

Current version:

* Working Streamlit MVP
* Synthetic datasets added
* Multi-agent reasoning trace added
* Grounded knowledge source added
* Azure AI Foundry placeholder added
* Ready for further Microsoft Foundry integration

## License

MIT License
