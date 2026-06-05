# Certway AI

Certway AI is a local Streamlit prototype for a Microsoft Foundry-ready multi-agent certification coach. It demonstrates grounded, synthetic-data reasoning for enterprise learning and workforce readiness.

> **Azure AI Foundry status:** this project is currently a local prototype / Foundry-ready placeholder. It does **not** make live Azure model calls yet. No API keys, credentials, paid services, confidential data, or real employee data are required for the demo.

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
- Microsoft Foundry / Azure AI Foundry-ready placeholder architecture

## Problem

Organizations often struggle to manage internal certification programs because:

- Employees do not know what to study first.
- Study plans are not personalized to role or workload.
- Managers lack visibility into certification readiness.
- Practice questions may be generic or ungrounded.
- Learning progress is difficult to track across teams.

## Solution

Certway AI uses multiple specialized agents to support employees and managers throughout the certification preparation process.

## Project Architecture

| Layer | Files | Purpose |
| --- | --- | --- |
| Streamlit app and UI pages | `app.py` | Provides Overview, Learner Coach, Practice Assessment, and Manager Dashboard pages. |
| Synthetic learner data | `data/learners.csv` | Provides synthetic learner profiles, certification goals, practice scores, and study progress. |
| Synthetic workload data | `data/workload_signals.csv` | Adds meeting load, focus capacity, and preferred learning slot signals. |
| Certification metadata | `data/certifications.csv` | Stores role-to-certification mappings, recommended study hours, and readiness thresholds. |
| Foundry IQ-style grounding source | `docs/engineering_certification_guide.md` | Acts as the approved synthetic guide used to extract grounded topics and source sections. |
| Agent logic | Agent helper functions in `app.py` | Implements local Orchestrator, Learning Path, Readiness, Assessment, Study Plan, Engagement, and Manager Insights behavior. |
| Agent prompt documentation | `prompts/agent_prompts.md` | Documents intended agent roles, responsibilities, and safety rules. |
| Azure placeholder client | `utils/azure_client.py` | Provides local recommendation fallback and honest Foundry placeholder/config status. It does not call Azure models. |

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

```text
docs/engineering_certification_guide.md
```

The Streamlit app parses this guide by role and certification, then shows grounded topics and source sections in the learning path and practice assessment.


## Azure AI Foundry Integration

The project includes an Azure AI Foundry-ready placeholder client:

```text
utils/azure_client.py
```

Current mode:

* Local rule-based multi-agent prototype
* Azure AI Foundry / Microsoft Foundry placeholder only
* Safe fallback if Azure is not configured
* Environment-based setup using `.env.example`
* No live Azure model calls are made

The environment template is provided in:

```text
.env.example
```

Real Azure values should be stored in a local `.env` file and should never be committed to GitHub.

## Reasoning Flow

1. Load synthetic learner, workload, and certification metadata from CSV files.
2. Parse the approved synthetic certification guide by role and certification.
3. Select grounded learning topics and source sections for the learner's target certification.
4. Compute readiness signals from practice score, study progress, meeting load, and focus capacity.
5. Route the profile through the local multi-agent workflow:
   - Orchestrator Agent
   - Learning Path Curator Agent
   - Readiness Reasoning Agent
   - Assessment Agent
   - Study Plan Generator Agent
   - Engagement Agent
   - Manager Insights Agent
6. Present a judge-facing final recommendation that combines readiness stance, key evidence, grounded topics, learner action, and manager handoff.
7. Keep all recommendations framed as coaching support, not a guarantee of certification success.

## Judging Criteria Mapping

| Hackathon criterion | How Certway AI addresses it |
| --- | --- |
| Accuracy & Relevance | Uses role, certification, practice score, study progress, workload signals, and certification-specific readiness thresholds. |
| Reasoning & Multi-step Thinking | Shows readiness signals, agent responsibilities, evidence, decisions, and a final recommendation summary. |
| Creativity & Originality | Combines certification coaching with workload-aware study planning and manager-ready support guidance. |
| User Experience & Presentation | Provides a polished Streamlit UI with Overview, Learner Coach, Practice Assessment, and Manager Dashboard pages. |
| Reliability & Safety | Uses synthetic data only, avoids secrets, includes human review language, and keeps Azure status honest. |
| Foundry IQ-style grounding | Parses an approved synthetic guide and displays grounded topics and source sections for practice questions. |
| Clear demo readiness | Includes a simple local setup path and a demo script for judges. |

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
* Azure AI Foundry-ready placeholder architecture
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

## Demo Script

A sample judge demo flow:

1. Open the Streamlit app.
2. View the overview dashboard.
3. Open **Learner Coach** and select a learner such as Taylor Kim or Alex Morgan.
4. Review the readiness stance and the judge-facing final recommendation card.
5. Open the **Reasoning Trace** tab and review each agent's responsibility, evidence, and decision.
6. Open the **Study & Engagement Plan** tab to see workload-aware study guidance.
7. Open the **Foundry Recommendation** tab and note that it is a local / Foundry-ready placeholder, not a live Azure call.
8. Open **Practice Assessment** and review grounded questions with source sections from the synthetic guide.
9. Open **Manager Dashboard** and review team-level readiness and manager action guidance.

## Project Status

Current version:

* Working Streamlit MVP
* Synthetic datasets added
* Multi-agent reasoning trace with responsibilities, evidence, and decisions
* Grounded knowledge source parsing and visible source sections
* Azure AI Foundry placeholder status with no live Azure model calls
* Ready for further Microsoft Foundry integration

## License

MIT License
