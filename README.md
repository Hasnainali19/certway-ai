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

The file:

```text
docs/engineering_certification_guide.md