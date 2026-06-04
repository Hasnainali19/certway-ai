import streamlit as st
import pandas as pd
import plotly.express as px
from utils.azure_client import azure_ai_enabled, generate_ai_recommendation

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Certway AI",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    learners = pd.read_csv("data/learners.csv")
    workload = pd.read_csv("data/workload_signals.csv")
    certifications = pd.read_csv("data/certifications.csv")

    merged = learners.merge(workload, on="learner_id", how="left")
    merged = merged.merge(certifications, on=["role", "certification"], how="left")

    return merged, certifications


df, certifications_df = load_data()

# -----------------------------
# Helper Functions / Agent Logic
# -----------------------------
def load_knowledge_document():
    with open("docs/engineering_certification_guide.md", "r", encoding="utf-8") as file:
        return file.read()
    
def calculate_risk(row):
    score = row["practice_score_avg"]
    meetings = row["meeting_hours_per_week"]
    focus = row["focus_hours_per_week"]

    if score >= 75 and focus >= 15:
        return "Low Risk"
    elif score >= 70 and focus >= 12:
        return "Medium Risk"
    elif meetings > 20 or focus < 10 or score < 70:
        return "High Risk"
    else:
        return "Medium Risk"


def readiness_summary(row):
    score = row["practice_score_avg"]
    passing_score = row["passing_practice_score"]
    meetings = row["meeting_hours_per_week"]
    focus = row["focus_hours_per_week"]

    reasons = []

    if score < passing_score:
        reasons.append(
            f"practice score is {score}%, below the recommended {passing_score}% readiness target"
        )

    if meetings > 20:
        reasons.append(
            f"meeting load is high at {meetings} hours per week"
        )

    if focus < 12:
        reasons.append(
            f"focus time is limited at {focus} hours per week"
        )

    if not reasons:
        return "This learner appears close to certification readiness based on current score and available focus time."

    return "This learner needs support because " + ", and ".join(reasons) + "."


def learning_path_agent(row):
    skills = str(row["skills"]).split(";")
    return [skill.strip() for skill in skills]


def study_plan_agent(row):
    skills = learning_path_agent(row)
    preferred_slot = row["preferred_learning_slot"]
    focus_hours = row["focus_hours_per_week"]
    score = row["practice_score_avg"]

    if focus_hours < 12:
        daily_time = "30-45 minutes"
    else:
        daily_time = "60-90 minutes"

    plan = []

    for index, skill in enumerate(skills, start=1):
        plan.append(
            {
                "Week": f"Week {1 if index <= 2 else 2}",
                "Focus Area": skill,
                "Suggested Time": daily_time,
                "Best Study Slot": preferred_slot
            }
        )

    if score < 75:
        plan.append(
            {
                "Week": "Week 2",
                "Focus Area": "Practice assessment and weak-topic review",
                "Suggested Time": daily_time,
                "Best Study Slot": preferred_slot
            }
        )

    return pd.DataFrame(plan)


def assessment_agent(row):
    certification = row["certification"]
    skills = learning_path_agent(row)

    questions = []

    for index, skill in enumerate(skills[:5], start=1):
        questions.append(
            {
                "Question": f"{index}. In the context of {certification}, explain why {skill} is important for this role.",
                "Answer Guide": f"A strong answer should describe how {skill} supports real-world tasks for a {row['role']} preparing for {certification}."
            }
        )

    return pd.DataFrame(questions)

def agent_workflow_trace(row):
    return [
        {
            "Agent": "Orchestrator Agent",
            "Action": f"Received learner profile for {row['name']} preparing for {row['certification']}."
        },
        {
            "Agent": "Learning Path Curator Agent",
            "Action": f"Mapped the {row['role']} role to certification topics: {row['skills']}."
        },
        {
            "Agent": "Study Plan Generator Agent",
            "Action": f"Created a study plan using {row['focus_hours_per_week']} focus hours/week and preferred slot: {row['preferred_learning_slot']}."
        },
        {
            "Agent": "Assessment Agent",
            "Action": f"Checked readiness using practice score {row['practice_score_avg']}% against target {row['passing_practice_score']}%."
        },
        {
            "Agent": "Manager Insights Agent",
            "Action": f"Generated support recommendation based on risk level: {row['Risk Level']}."
        }
    ]


def detailed_risk_reasoning(row):
    reasons = []

    if row["practice_score_avg"] < row["passing_practice_score"]:
        reasons.append(
            f"Practice score is {row['practice_score_avg']}%, which is below the {row['passing_practice_score']}% readiness target."
        )

    if row["meeting_hours_per_week"] > 20:
        reasons.append(
            f"Meeting load is high at {row['meeting_hours_per_week']} hours per week."
        )

    if row["focus_hours_per_week"] < 12:
        reasons.append(
            f"Focus time is limited at {row['focus_hours_per_week']} hours per week."
        )

    if row["hours_studied"] < row["recommended_hours"]:
        reasons.append(
            f"Studied hours are {row['hours_studied']}, below the recommended {row['recommended_hours']} hours for {row['certification']}."
        )

    if not reasons:
        reasons.append(
            "Learner meets the main readiness indicators based on practice score, focus time, and recommended study hours."
        )

    return reasons

def manager_insights_agent(team_df):
    total = len(team_df)
    high_risk = len(team_df[team_df["Risk Level"] == "High Risk"])
    medium_risk = len(team_df[team_df["Risk Level"] == "Medium Risk"])
    low_risk = len(team_df[team_df["Risk Level"] == "Low Risk"])
    avg_score = round(team_df["practice_score_avg"].mean(), 1)

    insight = (
        f"The team has {total} learners. "
        f"{low_risk} learners are low risk, {medium_risk} are medium risk, "
        f"and {high_risk} are high risk. "
        f"The average practice score is {avg_score}%. "
    )

    if high_risk > 0:
        insight += (
            "Managers should prioritize support for high-risk learners by reducing workload pressure, "
            "adding focused study blocks, and encouraging practice assessment review."
        )
    else:
        insight += (
            "The team appears to be progressing well, but weekly assessments should continue."
        )

    return insight


# Add risk level to dataframe
df["Risk Level"] = df.apply(calculate_risk, axis=1)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🎓 Certway AI")
st.sidebar.write("Multi-Agent Certification Coach")

if azure_ai_enabled():
    st.sidebar.success("Azure AI Foundry Mode: Enabled")
else:
    st.sidebar.info("Azure AI Foundry Mode: Local Prototype")

page = st.sidebar.radio(
    "Choose a page",
    ["Overview", "Learner Coach", "Practice Assessment", "Manager Dashboard"]
)

# -----------------------------
# Header
# -----------------------------
st.title("🎓 Certway AI")
st.subheader("Microsoft Foundry Multi-Agent Certification Coach")

st.markdown(
    """
Certway AI helps enterprise teams prepare employees for certifications using
multi-agent reasoning, synthetic workload signals, role-based learning paths,
practice assessments, and manager readiness insights.
"""
)

st.warning(
    "Demo Safety Notice: This application uses synthetic learner, workload, and certification data only. "
    "No real employee data, customer data, credentials, or personally identifiable information is used."
)

# -----------------------------
# Page 1: Overview
# -----------------------------
if page == "Overview":
    st.header("Project Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Learners", len(df))
    col2.metric("Average Practice Score", f"{round(df['practice_score_avg'].mean(), 1)}%")
    col3.metric("High Risk Learners", len(df[df["Risk Level"] == "High Risk"]))
    col4.metric("Certifications", df["certification"].nunique())

    st.divider()

    st.subheader("Learner Dataset")
    st.dataframe(df, use_container_width=True)

    st.subheader("Risk Level Distribution")
    risk_chart = px.pie(
        df,
        names="Risk Level",
        title="Certification Readiness Risk Distribution"
    )
    st.plotly_chart(risk_chart, use_container_width=True)

    st.subheader("Practice Score by Learner")
    score_chart = px.bar(
        df,
        x="learner_id",
        y="practice_score_avg",
        color="Risk Level",
        hover_data=["role", "certification"],
        title="Practice Score by Learner"
    )
    st.plotly_chart(score_chart, use_container_width=True)

# -----------------------------
# Page 2: Learner Coach
# -----------------------------
elif page == "Learner Coach":
    st.header("🧠 Learner Coach Agent")

    learner_options = df["learner_id"] + " - " + df["name"] + " (" + df["role"] + ")"
    selected = st.selectbox("Select a learner", learner_options)

    selected_id = selected.split(" - ")[0]
    learner = df[df["learner_id"] == selected_id].iloc[0]

    st.subheader("Learner Profile")

    col1, col2, col3 = st.columns(3)

    col1.metric("Role", learner["role"])
    col2.metric("Certification", learner["certification"])
    col3.metric("Risk Level", learner["Risk Level"])

    col4, col5, col6 = st.columns(3)

    col4.metric("Practice Score", f"{learner['practice_score_avg']}%")
    col5.metric("Meeting Hours/Week", learner["meeting_hours_per_week"])
    col6.metric("Focus Hours/Week", learner["focus_hours_per_week"])

    st.divider()

    st.subheader("Learning Path Curator Agent")
    path = learning_path_agent(learner)

    for topic in path:
        st.write(f"✅ {topic}")

    st.subheader("Multi-Agent Workflow Trace")

    workflow = agent_workflow_trace(learner)

    for step in workflow:
        st.markdown(f"**{step['Agent']}**")
        st.write(step["Action"])
        st.write("⬇️")

    st.divider()

    st.subheader("Readiness Reasoning")

    risk_reasons = detailed_risk_reasoning(learner)

    st.info(f"Risk Level: {learner['Risk Level']}")

    for reason in risk_reasons:
        st.write(f"- {reason}")

    if learner["Risk Level"] == "High Risk":
        st.error(
            "Recommendation: Delay exam attempt, reduce workload pressure if possible, "
            "and schedule shorter daily study blocks."
        )
    elif learner["Risk Level"] == "Medium Risk":
        st.warning(
            "Recommendation: Continue preparation with weekly practice checks and targeted review of weak topics."
        )
    else:
        st.success(
            "Recommendation: Learner is close to ready. Complete one final practice assessment before the exam."
        )

    st.divider()

    st.subheader("Microsoft Foundry AI Recommendation")

    foundry_prompt = f"""
    Learner: {learner['name']}
    Role: {learner['role']}
    Certification: {learner['certification']}
    Practice Score: {learner['practice_score_avg']}%
    Hours Studied: {learner['hours_studied']}
    Meeting Hours/Week: {learner['meeting_hours_per_week']}
    Focus Hours/Week: {learner['focus_hours_per_week']}
    Risk Level: {learner['Risk Level']}

    Generate a concise certification coaching recommendation.
    """

    st.write(generate_ai_recommendation(foundry_prompt))

    st.subheader("Study Plan Generator Agent")
    study_plan = study_plan_agent(learner)
    st.dataframe(study_plan, use_container_width=True)

# -----------------------------
# Page 3: Practice Assessment
# -----------------------------
elif page == "Practice Assessment":
    st.header("📝 Assessment Agent")

    learner_options = df["learner_id"] + " - " + df["name"] + " (" + df["certification"] + ")"
    selected = st.selectbox("Select learner for practice assessment", learner_options)

    selected_id = selected.split(" - ")[0]
    learner = df[df["learner_id"] == selected_id].iloc[0]

    st.subheader("Grounded Knowledge Source")

    knowledge_doc = load_knowledge_document()

    with st.expander("View approved synthetic certification guide"):
        st.markdown(knowledge_doc)

    st.caption(
        "Source: Engineering Certification Enablement Guide Synthetic Document. "
        "This prototype uses synthetic approved content to demonstrate Foundry IQ-style grounded retrieval."
    )

    st.subheader(f"Practice Questions for {learner['certification']}")

    questions = assessment_agent(learner)
    st.dataframe(questions, use_container_width=True)

    st.subheader("Readiness Recommendation")

    if learner["practice_score_avg"] >= learner["passing_practice_score"]:
        st.success(
            "This learner is close to ready. Recommend one final practice assessment before exam attempt."
        )
    else:
        st.warning(
            "This learner should continue studying before attempting the certification exam."
        )

# -----------------------------
# Page 4: Manager Dashboard
# -----------------------------
elif page == "Manager Dashboard":
    st.header("📊 Manager Insights Agent")

    col1, col2, col3 = st.columns(3)

    col1.metric("Low Risk", len(df[df["Risk Level"] == "Low Risk"]))
    col2.metric("Medium Risk", len(df[df["Risk Level"] == "Medium Risk"]))
    col3.metric("High Risk", len(df[df["Risk Level"] == "High Risk"]))

    st.subheader("Team Readiness Table")
    st.dataframe(
        df[
            [
                "learner_id",
                "name",
                "role",
                "certification",
                "practice_score_avg",
                "meeting_hours_per_week",
                "focus_hours_per_week",
                "Risk Level"
            ]
        ],
        use_container_width=True
    )

    st.subheader("Manager Summary")
    st.info(manager_insights_agent(df))

    st.subheader("Risk by Role")
    role_chart = px.histogram(
        df,
        x="role",
        color="Risk Level",
        title="Risk Level by Role"
    )
    st.plotly_chart(role_chart, use_container_width=True)