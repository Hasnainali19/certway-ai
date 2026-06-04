import pandas as pd
import plotly.express as px
import streamlit as st

from utils.azure_client import azure_ai_enabled, generate_ai_recommendation


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Certway AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


RISK_COLORS = {
    "Low Risk": "#16a34a",
    "Medium Risk": "#f59e0b",
    "High Risk": "#dc2626",
}

RISK_ORDER = ["Low Risk", "Medium Risk", "High Risk"]


# -----------------------------
# UI Helpers
# -----------------------------
def inject_custom_css():
    st.markdown(
        """
        <style>
        :root {
            --certway-navy: #0f172a;
            --certway-blue: #2563eb;
            --certway-sky: #e0f2fe;
            --certway-soft: #f8fafc;
            --certway-border: #e2e8f0;
            --certway-muted: #64748b;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label {
            border-radius: 0.75rem;
            padding: 0.25rem 0.5rem;
        }

        .hero-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.25), transparent 35%),
                linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
            border-radius: 1.35rem;
            color: white;
            padding: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 20px 45px rgba(15, 23, 42, 0.18);
        }

        .hero-eyebrow {
            color: #bfdbfe;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }

        .hero-title {
            font-size: clamp(2rem, 4vw, 3.4rem);
            font-weight: 800;
            line-height: 1;
            margin-bottom: 0.75rem;
        }

        .hero-copy {
            color: #dbeafe;
            font-size: 1.05rem;
            max-width: 900px;
        }

        .section-card {
            background: white;
            border: 1px solid var(--certway-border);
            border-radius: 1rem;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        }

        .metric-card {
            background: white;
            border: 1px solid var(--certway-border);
            border-radius: 1rem;
            min-height: 118px;
            padding: 1rem;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        }

        .metric-label {
            color: var(--certway-muted);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--certway-navy);
            font-size: 1.9rem;
            font-weight: 800;
            line-height: 1.2;
            margin-top: 0.35rem;
        }

        .metric-caption {
            color: var(--certway-muted);
            font-size: 0.86rem;
            margin-top: 0.35rem;
        }

        .risk-badge {
            border-radius: 999px;
            color: white;
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.03em;
            padding: 0.3rem 0.7rem;
            text-transform: uppercase;
        }

        .topic-pill {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 999px;
            color: #1d4ed8;
            display: inline-block;
            font-weight: 700;
            margin: 0.2rem 0.25rem 0.2rem 0;
            padding: 0.42rem 0.75rem;
        }

        .agent-step {
            background: #f8fafc;
            border: 1px solid var(--certway-border);
            border-left: 5px solid var(--certway-blue);
            border-radius: 0.85rem;
            margin-bottom: 0.75rem;
            padding: 0.85rem 1rem;
        }

        .agent-step-title {
            color: var(--certway-navy);
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .agent-step-copy {
            color: #334155;
            font-size: 0.92rem;
        }

        .safety-note {
            background: #fff7ed;
            border: 1px solid #fed7aa;
            border-radius: 0.9rem;
            color: #9a3412;
            padding: 0.8rem 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-eyebrow">Microsoft Foundry-ready prototype</div>
            <div class="hero-title">Certway AI</div>
            <div class="hero-copy">
                A multi-agent certification coach that combines synthetic learner data,
                workload signals, grounded practice content, and manager-ready insights
                to make certification preparation easier to prioritize.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label, value, caption=None):
    caption_html = f'<div class="metric-caption">{caption}</div>' if caption else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_risk_badge(risk_level):
    color = RISK_COLORS.get(risk_level, "#64748b")
    st.markdown(
        f'<span class="risk-badge" style="background:{color};">{risk_level}</span>',
        unsafe_allow_html=True,
    )


def render_topics(topics):
    topic_html = "".join(f'<span class="topic-pill">{topic}</span>' for topic in topics)
    st.markdown(topic_html, unsafe_allow_html=True)


def render_agent_steps(workflow):
    for step in workflow:
        st.markdown(
            f"""
            <div class="agent-step">
                <div class="agent-step-title">{step["Agent"]}</div>
                <div class="agent-step-copy"><strong>Evidence:</strong> {step["Evidence"]}</div>
                <div class="agent-step-copy"><strong>Decision:</strong> {step["Decision"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
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
    score_gap = row["passing_practice_score"] - row["practice_score_avg"]
    high_meeting_load = row["meeting_hours_per_week"] > 20
    low_focus_time = row["focus_hours_per_week"] < 12

    if row["practice_score_avg"] < 70 or (score_gap > 0 and high_meeting_load):
        return "High Risk"

    if score_gap > 0 or high_meeting_load or low_focus_time:
        return "Medium Risk"

    return "Low Risk"


def learning_path_agent(row):
    skills = str(row["skills"]).split(";")
    return [skill.strip() for skill in skills if skill.strip()]


def readiness_signal_table(row):
    score_gap = row["practice_score_avg"] - row["passing_practice_score"]
    study_gap = row["hours_studied"] - row["recommended_hours"]

    return pd.DataFrame(
        [
            {
                "Signal": "Practice score",
                "Observed": f"{row['practice_score_avg']}%",
                "Target": f"{row['passing_practice_score']}%+",
                "Status": "On track" if score_gap >= 0 else "Needs attention",
                "Reasoning": (
                    "Practice score meets the local readiness threshold."
                    if score_gap >= 0
                    else f"Practice score is {abs(score_gap)} points below target."
                ),
            },
            {
                "Signal": "Study progress",
                "Observed": f"{row['hours_studied']} hours",
                "Target": f"{row['recommended_hours']} hours",
                "Status": "On track" if study_gap >= 0 else "Needs attention",
                "Reasoning": (
                    "Studied hours meet the synthetic certification guide recommendation."
                    if study_gap >= 0
                    else f"Study progress is {abs(study_gap)} hours below recommendation."
                ),
            },
            {
                "Signal": "Meeting load",
                "Observed": f"{row['meeting_hours_per_week']} hours/week",
                "Target": "20 or fewer",
                "Status": "On track" if row["meeting_hours_per_week"] <= 20 else "Needs attention",
                "Reasoning": (
                    "Meeting load leaves room for focused preparation."
                    if row["meeting_hours_per_week"] <= 20
                    else "Meeting load is above the workload rule and may fragment study time."
                ),
            },
            {
                "Signal": "Focus capacity",
                "Observed": f"{row['focus_hours_per_week']} hours/week",
                "Target": "12 or more",
                "Status": "On track" if row["focus_hours_per_week"] >= 12 else "Needs attention",
                "Reasoning": (
                    "Focus capacity supports consistent learning blocks."
                    if row["focus_hours_per_week"] >= 12
                    else "Focus capacity is constrained; the plan should use shorter study blocks."
                ),
            },
        ]
    )


def detailed_risk_reasoning(row):
    signal_df = readiness_signal_table(row)
    reasons = signal_df[signal_df["Status"] == "Needs attention"]["Reasoning"].tolist()

    if not reasons:
        reasons.append(
            "Learner meets the main readiness indicators based on practice score, study progress, workload, and focus capacity."
        )

    return reasons


def readiness_decision(row):
    reasons = detailed_risk_reasoning(row)

    if row["practice_score_avg"] < row["passing_practice_score"]:
        primary_constraint = "Practice score is below the readiness target."
    elif row["meeting_hours_per_week"] > 20:
        primary_constraint = "Meeting load may block consistent preparation."
    elif row["focus_hours_per_week"] < 12:
        primary_constraint = "Available focus time is limited."
    elif row["hours_studied"] < row["recommended_hours"]:
        primary_constraint = "Recommended study hours are not complete."
    else:
        primary_constraint = "No major local readiness constraint detected."

    if row["Risk Level"] == "High Risk":
        next_action = (
            "Pause exam scheduling, protect smaller study blocks, and review weak topics before another readiness check."
        )
    elif row["Risk Level"] == "Medium Risk":
        next_action = (
            "Continue targeted preparation, add a practice check, and focus first on the topics tied to missed readiness signals."
        )
    else:
        next_action = (
            "Complete a final practice assessment and keep the current study rhythm."
        )

    return {
        "Readiness stance": row["Risk Level"],
        "Primary constraint": primary_constraint,
        "Evidence count": f"{len(reasons)} active reasoning signal(s)",
        "Next best action": next_action,
        "Human review note": "Use this as coaching support, not a guarantee of exam outcome.",
    }


def study_plan_agent(row):
    skills = learning_path_agent(row)
    preferred_slot = row["preferred_learning_slot"]
    focus_hours = row["focus_hours_per_week"]

    if focus_hours < 12:
        daily_time = "30-45 minutes"
        pacing = "Short focus block"
    elif focus_hours < 16:
        daily_time = "45-60 minutes"
        pacing = "Balanced focus block"
    else:
        daily_time = "60-90 minutes"
        pacing = "Deep focus block"

    plan = []

    for index, skill in enumerate(skills, start=1):
        plan.append(
            {
                "Phase": f"Phase {1 if index <= 2 else 2}",
                "Focus Area": skill,
                "Suggested Time": daily_time,
                "Best Study Slot": preferred_slot,
                "Why This Matters": f"Builds readiness for {row['certification']} as a {row['role']}.",
                "Pacing": pacing,
            }
        )

    if row["practice_score_avg"] < row["passing_practice_score"]:
        plan.append(
            {
                "Phase": "Readiness Check",
                "Focus Area": "Practice assessment and weak-topic review",
                "Suggested Time": daily_time,
                "Best Study Slot": preferred_slot,
                "Why This Matters": "Closes the gap between current score and readiness target.",
                "Pacing": pacing,
            }
        )

    return pd.DataFrame(plan)


def engagement_agent(row):
    if row["meeting_hours_per_week"] > 20:
        reminder_strategy = "Use calendar-protected learning blocks around meeting-heavy periods."
    elif row["focus_hours_per_week"] < 12:
        reminder_strategy = "Use shorter reminders and avoid stacking study after context-heavy work."
    else:
        reminder_strategy = "Use a steady reminder cadence in the preferred learning slot."

    if row["Risk Level"] == "High Risk":
        support_suggestion = "Ask the manager to help protect focus time and defer non-essential learning distractions."
    elif row["Risk Level"] == "Medium Risk":
        support_suggestion = "Ask for a practice-review checkpoint and topic-specific support."
    else:
        support_suggestion = "Maintain the current schedule and confirm readiness with one final practice check."

    return {
        "Preferred timing": row["preferred_learning_slot"],
        "Reminder strategy": reminder_strategy,
        "Support suggestion": support_suggestion,
    }


def assessment_agent(row):
    certification = row["certification"]
    skills = learning_path_agent(row)

    questions = []

    for index, skill in enumerate(skills[:5], start=1):
        questions.append(
            {
                "Question": f"{index}. In the context of {certification}, explain why {skill} is important for this role.",
                "Answer Guide": (
                    f"A strong answer connects {skill} to real-world {row['role']} tasks, "
                    "mentions tradeoffs or operational impact, and references approved certification topics."
                ),
                "Grounding": "Synthetic engineering certification guide",
            }
        )

    return pd.DataFrame(questions)


def agent_workflow_trace(row):
    decision = readiness_decision(row)
    topics = ", ".join(learning_path_agent(row))

    return [
        {
            "Agent": "Orchestrator Agent",
            "Evidence": f"{row['name']} is preparing for {row['certification']} as a {row['role']}.",
            "Decision": "Route the profile through learning path, study planning, assessment, engagement, and manager insight agents.",
        },
        {
            "Agent": "Learning Path Curator Agent",
            "Evidence": f"Role-to-certification mapping produced these grounded topics: {topics}.",
            "Decision": "Prioritize certification topics from the approved synthetic guide before generic advice.",
        },
        {
            "Agent": "Readiness Reasoning Agent",
            "Evidence": (
                f"Practice score {row['practice_score_avg']}% vs target {row['passing_practice_score']}%; "
                f"{row['hours_studied']} of {row['recommended_hours']} recommended study hours complete."
            ),
            "Decision": f"Classify current stance as {row['Risk Level']} because {decision['Primary constraint'].lower()}",
        },
        {
            "Agent": "Study Plan Generator Agent",
            "Evidence": (
                f"{row['focus_hours_per_week']} focus hours/week, "
                f"{row['meeting_hours_per_week']} meeting hours/week, preferred slot: {row['preferred_learning_slot']}."
            ),
            "Decision": "Adjust pacing and study block size to match workload capacity.",
        },
        {
            "Agent": "Engagement Agent",
            "Evidence": f"Risk level is {row['Risk Level']} with workload and focus constraints included.",
            "Decision": engagement_agent(row)["Support suggestion"],
        },
    ]


def manager_insights_agent(team_df):
    total = len(team_df)
    high_risk = len(team_df[team_df["Risk Level"] == "High Risk"])
    medium_risk = len(team_df[team_df["Risk Level"] == "Medium Risk"])
    low_risk = len(team_df[team_df["Risk Level"] == "Low Risk"])
    avg_score = round(team_df["practice_score_avg"].mean(), 1)
    avg_focus = round(team_df["focus_hours_per_week"].mean(), 1)

    insight = (
        f"The team has {total} synthetic learners: {low_risk} low risk, "
        f"{medium_risk} medium risk, and {high_risk} high risk. "
        f"Average practice score is {avg_score}% and average focus capacity is {avg_focus} hours/week. "
    )

    if high_risk > 0:
        insight += (
            "Manager attention should start with high-risk profiles, especially where low practice scores overlap "
            "with high meeting load or low focus time."
        )
    else:
        insight += (
            "No high-risk profiles are currently flagged, so the manager can focus on final practice checks and continuity."
        )

    return insight


def manager_action_plan(team_df):
    high_risk_roles = sorted(
        team_df.loc[team_df["Risk Level"] == "High Risk", "role"].dropna().unique()
    )

    actions = [
        {
            "Priority": "High",
            "Action": "Protect study blocks for high-risk learners",
            "Rationale": "High-risk status is driven by readiness gaps, high meeting load, or limited focus capacity.",
        },
        {
            "Priority": "Medium",
            "Action": "Schedule practice assessment review",
            "Rationale": "Practice scores provide the clearest local signal for certification readiness.",
        },
        {
            "Priority": "Medium",
            "Action": "Use role-specific topic review",
            "Rationale": "Learning paths are grounded in the approved synthetic certification guide.",
        },
    ]

    if high_risk_roles:
        roles = ", ".join(high_risk_roles)
        actions[0]["Rationale"] += f" Current high-risk roles: {roles}."

    return pd.DataFrame(actions)


def build_foundry_prompt(row):
    decision = readiness_decision(row)
    reasons = "; ".join(detailed_risk_reasoning(row))

    return f"""
Learner: {row['name']}
Role: {row['role']}
Certification: {row['certification']}
Practice Score: {row['practice_score_avg']}%
Passing Practice Score: {row['passing_practice_score']}%
Hours Studied: {row['hours_studied']}
Recommended Hours: {row['recommended_hours']}
Meeting Hours/Week: {row['meeting_hours_per_week']}
Focus Hours/Week: {row['focus_hours_per_week']}
Preferred Learning Slot: {row['preferred_learning_slot']}
Risk Level: {row['Risk Level']}
Primary Constraint: {decision['Primary constraint']}
Reasoning Evidence: {reasons}

Generate a concise certification coaching recommendation using only these synthetic signals.
"""


# Add risk level and derived columns to dataframe
df["Risk Level"] = df.apply(calculate_risk, axis=1)
df["Practice Gap"] = df["passing_practice_score"] - df["practice_score_avg"]
df["Study Hours Gap"] = df["recommended_hours"] - df["hours_studied"]


inject_custom_css()


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
    ["Overview", "Learner Coach", "Practice Assessment", "Manager Dashboard"],
)

st.sidebar.divider()
st.sidebar.caption(
    "Synthetic demo data only. Keep real credentials in a local .env file and never commit them."
)


# -----------------------------
# Header
# -----------------------------
render_hero()

st.markdown(
    """
    <div class="safety-note">
        <strong>Demo safety notice:</strong> This application uses synthetic learner,
        workload, and certification data only. No real employee data, customer data,
        credentials, or personally identifiable information is used.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# -----------------------------
# Page 1: Overview
# -----------------------------
if page == "Overview":
    st.header("Project Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card("Total Learners", len(df), "Synthetic employee profiles")
    with col2:
        render_metric_card(
            "Average Practice Score",
            f"{round(df['practice_score_avg'].mean(), 1)}%",
            "Across all certifications",
        )
    with col3:
        render_metric_card(
            "High Risk Learners",
            len(df[df["Risk Level"] == "High Risk"]),
            "Needs manager attention",
        )
    with col4:
        render_metric_card(
            "Certifications",
            df["certification"].nunique(),
            "Role-based goals",
        )

    st.divider()

    chart_col1, chart_col2 = st.columns([1, 1.25])

    with chart_col1:
        st.subheader("Risk Level Distribution")
        risk_chart = px.pie(
            df,
            names="Risk Level",
            title="Certification Readiness Risk Distribution",
            color="Risk Level",
            color_discrete_map=RISK_COLORS,
            category_orders={"Risk Level": RISK_ORDER},
            hole=0.45,
        )
        risk_chart.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(risk_chart, use_container_width=True)

    with chart_col2:
        st.subheader("Practice Score by Learner")
        score_chart = px.bar(
            df,
            x="learner_id",
            y="practice_score_avg",
            color="Risk Level",
            hover_data=["name", "role", "certification", "focus_hours_per_week"],
            title="Practice Score by Learner",
            color_discrete_map=RISK_COLORS,
            category_orders={"Risk Level": RISK_ORDER},
        )
        score_chart.add_hline(
            y=75,
            line_dash="dot",
            annotation_text="Readiness target",
            annotation_position="top left",
        )
        st.plotly_chart(score_chart, use_container_width=True)

    st.subheader("Learner Dataset")
    st.dataframe(
        df[
            [
                "learner_id",
                "name",
                "role",
                "certification",
                "practice_score_avg",
                "hours_studied",
                "meeting_hours_per_week",
                "focus_hours_per_week",
                "Risk Level",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# -----------------------------
# Page 2: Learner Coach
# -----------------------------
elif page == "Learner Coach":
    st.header("🧠 Learner Coach Agent")

    learner_options = df["learner_id"] + " - " + df["name"] + " (" + df["role"] + ")"
    selected = st.selectbox("Select a learner", learner_options)

    selected_id = selected.split(" - ")[0]
    learner = df[df["learner_id"] == selected_id].iloc[0]
    decision = readiness_decision(learner)

    profile_col, reasoning_col = st.columns([1, 1])

    with profile_col:
        st.subheader("Learner Profile")
        card_col1, card_col2 = st.columns(2)
        with card_col1:
            render_metric_card("Role", learner["role"], learner["certification"])
        with card_col2:
            render_metric_card("Practice Score", f"{learner['practice_score_avg']}%", "Readiness target: 75%")

        card_col3, card_col4 = st.columns(2)
        with card_col3:
            render_metric_card("Meetings", f"{learner['meeting_hours_per_week']} hrs/wk", "Workload signal")
        with card_col4:
            render_metric_card("Focus Time", f"{learner['focus_hours_per_week']} hrs/wk", "Capacity signal")

    with reasoning_col:
        st.subheader("Readiness Stance")
        render_risk_badge(learner["Risk Level"])
        st.write("")
        st.info(decision["Primary constraint"])
        st.write(decision["Next best action"])
        st.caption(decision["Human review note"])

    st.divider()

    st.subheader("Learning Path Curator Agent")
    path = learning_path_agent(learner)
    render_topics(path)

    reasoning_tab, plan_tab, foundry_tab = st.tabs(
        ["Reasoning Trace", "Study & Engagement Plan", "Foundry Recommendation"]
    )

    with reasoning_tab:
        st.subheader("Readiness Signals")
        st.dataframe(readiness_signal_table(learner), use_container_width=True, hide_index=True)

        st.subheader("Multi-Agent Workflow Trace")
        render_agent_steps(agent_workflow_trace(learner))

        st.subheader("Decision Summary")
        st.json(decision)

    with plan_tab:
        st.subheader("Study Plan Generator Agent")
        study_plan = study_plan_agent(learner)
        st.dataframe(study_plan, use_container_width=True, hide_index=True)

        st.subheader("Engagement Agent")
        engagement = engagement_agent(learner)
        eng_col1, eng_col2, eng_col3 = st.columns(3)
        with eng_col1:
            render_metric_card("Preferred Timing", engagement["Preferred timing"])
        with eng_col2:
            render_metric_card("Reminder Strategy", "Workload-aware", engagement["Reminder strategy"])
        with eng_col3:
            render_metric_card("Support", "Manager-ready", engagement["Support suggestion"])

    with foundry_tab:
        st.subheader("Microsoft Foundry AI Recommendation")
        st.caption(
            "Uses the safe local rule-based fallback unless USE_AZURE_AI=true is configured in a private .env file."
        )

        foundry_prompt = build_foundry_prompt(learner)
        st.write(generate_ai_recommendation(foundry_prompt))

        with st.expander("View synthetic prompt sent to the recommendation helper"):
            st.code(foundry_prompt, language="text")


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
    st.dataframe(questions, use_container_width=True, hide_index=True)

    st.subheader("Readiness Recommendation")

    if learner["practice_score_avg"] >= learner["passing_practice_score"]:
        st.success(
            "This learner is close to ready. Recommend one final practice assessment before exam attempt."
        )
    else:
        st.warning(
            "This learner should continue studying before attempting the certification exam."
        )

    st.subheader("Assessment Reasoning")
    st.dataframe(readiness_signal_table(learner), use_container_width=True, hide_index=True)


# -----------------------------
# Page 4: Manager Dashboard
# -----------------------------
elif page == "Manager Dashboard":
    st.header("📊 Manager Insights Agent")

    col1, col2, col3 = st.columns(3)

    with col1:
        render_metric_card("Low Risk", len(df[df["Risk Level"] == "Low Risk"]), "Ready or close to ready")
    with col2:
        render_metric_card("Medium Risk", len(df[df["Risk Level"] == "Medium Risk"]), "Needs targeted support")
    with col3:
        render_metric_card("High Risk", len(df[df["Risk Level"] == "High Risk"]), "Needs manager attention")

    st.subheader("Manager Summary")
    st.info(manager_insights_agent(df))

    dashboard_col1, dashboard_col2 = st.columns([1.1, 1])

    with dashboard_col1:
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
                    "Risk Level",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    with dashboard_col2:
        st.subheader("Risk by Role")
        role_chart = px.histogram(
            df,
            x="role",
            color="Risk Level",
            title="Risk Level by Role",
            color_discrete_map=RISK_COLORS,
            category_orders={"Risk Level": RISK_ORDER},
        )
        st.plotly_chart(role_chart, use_container_width=True)

    st.subheader("Manager Action Plan")
    st.dataframe(manager_action_plan(df), use_container_width=True, hide_index=True)