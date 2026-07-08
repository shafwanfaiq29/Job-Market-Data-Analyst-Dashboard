from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="Data Analyst Job Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SALARY_PATH = DATA_DIR / "ds_salaries.csv"

EXPERIENCE_ORDER = ["Entry Level", "Mid Level", "Senior Level", "Executive Level"]
REMOTE_ORDER = ["On-site", "Hybrid", "Fully Remote"]

COLOR_SEQUENCE = [
    "#38bdf8", "#60a5fa", "#34d399", "#f59e0b", "#f472b6",
    "#a78bfa", "#fb7185", "#22c55e", "#f97316", "#06b6d4"
]

# ============================================================
# Styling
# ============================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2.5rem;
            max-width: 1380px;
        }

        .hero {
            padding: 1.4rem 1.6rem;
            border-radius: 1.1rem;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.22), rgba(14, 165, 233, 0.06));
            border: 1px solid rgba(148, 163, 184, 0.22);
            margin-bottom: 1.2rem;
        }

        .hero-title {
            font-size: 2.35rem;
            font-weight: 850;
            letter-spacing: -0.04em;
            margin-bottom: 0.3rem;
        }

        .hero-subtitle {
            font-size: 1.02rem;
            color: #94a3b8;
            line-height: 1.65;
            max-width: 980px;
        }

        .mini-label {
            color: #94a3b8;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.25rem;
        }

        .insight-card {
            padding: 1rem 1.05rem;
            border-radius: 0.9rem;
            background: rgba(15, 23, 42, 0.62);
            border: 1px solid rgba(148, 163, 184, 0.22);
            margin-bottom: 0.75rem;
            line-height: 1.6;
        }

        .insight-card strong {
            color: #e2e8f0;
        }

        .note-card {
            padding: 1rem 1.05rem;
            border-radius: 0.9rem;
            background: rgba(30, 41, 59, 0.45);
            border: 1px solid rgba(148, 163, 184, 0.18);
            color: #cbd5e1;
            line-height: 1.55;
        }

        .section-caption {
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.55;
            margin-bottom: 0.6rem;
        }

        div[data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.22);
            padding: 1rem 1.05rem;
            border-radius: 0.95rem;
            box-shadow: 0 10px 28px rgba(2, 6, 23, 0.12);
        }

        div[data-testid="stMetricLabel"] {
            color: #94a3b8;
            font-size: 0.86rem;
        }

        div[data-testid="stMetricValue"] {
            color: #f8fafc;
            font-weight: 800;
        }

        div[data-testid="stTabs"] button {
            font-weight: 700;
        }

        .stPlotlyChart {
            border-radius: 0.9rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Helper functions
# ============================================================


def format_usd(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"${value:,.0f}"


def format_percent(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:.1f}%"


def group_role(title: str) -> str:
    title = str(title).lower()

    if "data analyst" in title or "product data analyst" in title:
        return "Data Analyst"
    if "data scientist" in title or "research scientist" in title:
        return "Data Scientist"
    if "data engineer" in title or "big data engineer" in title or "etl" in title:
        return "Data Engineer"
    if "machine learning" in title or "ml engineer" in title or "ai scientist" in title:
        return "Machine Learning / AI"
    if "analytics" in title or "bi" in title or "business analyst" in title:
        return "Analytics / BI"
    if "data architect" in title:
        return "Data Architect"
    if "data science" in title:
        return "Data Science Management"
    return "Other Data Role"


COUNTRY_MAP = {
    "US": "United States", "GB": "United Kingdom", "CA": "Canada", "DE": "Germany",
    "IN": "India", "FR": "France", "ES": "Spain", "GR": "Greece", "JP": "Japan",
    "NL": "Netherlands", "AT": "Austria", "PT": "Portugal", "PL": "Poland",
    "PK": "Pakistan", "BR": "Brazil", "AU": "Australia", "TR": "Turkey", "DK": "Denmark",
    "MX": "Mexico", "NG": "Nigeria", "CN": "China", "RU": "Russia", "IT": "Italy",
    "CH": "Switzerland", "AE": "United Arab Emirates", "SG": "Singapore", "BE": "Belgium",
    "LU": "Luxembourg", "SI": "Slovenia", "RO": "Romania", "VN": "Vietnam", "CL": "Chile",
    "HU": "Hungary", "EE": "Estonia", "CZ": "Czech Republic", "DZ": "Algeria", "MY": "Malaysia",
    "HN": "Honduras", "NZ": "New Zealand", "IE": "Ireland", "MT": "Malta", "UA": "Ukraine",
    "IQ": "Iraq", "IR": "Iran", "CO": "Colombia", "KE": "Kenya", "MD": "Moldova",
    "AS": "American Samoa",
}


@st.cache_data(show_spinner=False)
def load_salary_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    experience_map = {
        "EN": "Entry Level",
        "MI": "Mid Level",
        "SE": "Senior Level",
        "EX": "Executive Level",
    }

    employment_map = {
        "FT": "Full-time",
        "PT": "Part-time",
        "CT": "Contract",
        "FL": "Freelance",
    }

    remote_map = {
        0: "On-site",
        50: "Hybrid",
        100: "Fully Remote",
    }

    company_size_map = {
        "S": "Small",
        "M": "Medium",
        "L": "Large",
    }

    df["experience_label"] = df["experience_level"].map(experience_map)
    df["employment_label"] = df["employment_type"].map(employment_map)
    df["remote_label"] = df["remote_ratio"].map(remote_map)
    df["company_size_label"] = df["company_size"].map(company_size_map)
    df["role_group"] = df["job_title"].apply(group_role)
    df["company_country"] = df["company_location"].map(COUNTRY_MAP).fillna(df["company_location"])
    df["employee_country"] = df["employee_residence"].map(COUNTRY_MAP).fillna(df["employee_residence"])

    return df


@st.cache_data(show_spinner=False)
def load_skill_tables(data_dir: Path) -> dict[str, pd.DataFrame]:
    return {
        "skill_overall": pd.read_csv(data_dir / "skill_overall.csv"),
        "skill_data_analyst": pd.read_csv(data_dir / "skill_data_analyst.csv"),
        "skill_role_matrix": pd.read_csv(data_dir / "skill_role_matrix.csv"),
        "remote_skill_compare": pd.read_csv(data_dir / "remote_skill_compare.csv"),
        "skill_recommendation": pd.read_csv(data_dir / "skill_recommendation.csv"),
    }


def dark_layout(fig: go.Figure, height: int = 430) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.25)",
        font=dict(color="#e5e7eb"),
        title=dict(x=0.02, font=dict(size=18)),
        margin=dict(l=10, r=20, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.16)", zerolinecolor="rgba(148,163,184,0.24)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.10)", zerolinecolor="rgba(148,163,184,0.18)")
    return fig


def horizontal_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    text: str | None = None,
    height: int = 430,
    color: str | None = None,
) -> go.Figure:
    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        text=text,
        color=color,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(title=title, xaxis_title=None, yaxis_title=None, showlegend=bool(color))
    return dark_layout(fig, height=height)


def metric_row(df: pd.DataFrame) -> None:
    total_records = len(df)
    overall_median = df["salary_in_usd"].median()
    da_median = df.loc[df["role_group"] == "Data Analyst", "salary_in_usd"].median()
    fully_remote = df["remote_label"].eq("Fully Remote").mean() * 100
    top_role = df["role_group"].value_counts().idxmax() if not df.empty else "-"

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Salary Records", f"{total_records:,}")
    c2.metric("Overall Median", format_usd(overall_median))
    c3.metric("Data Analyst Median", format_usd(da_median))
    c4.metric("Fully Remote Share", format_percent(fully_remote))
    c5.metric("Top Role", top_role)


def insight_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="mini-label">{title}</div>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def note_card(body: str) -> None:
    st.markdown(f"<div class='note-card'>{body}</div>", unsafe_allow_html=True)


# ============================================================
# Data loading
# ============================================================

if not SALARY_PATH.exists():
    st.error("File `data/ds_salaries.csv` was not found. Make sure the dataset exists in the `data` folder.")
    st.stop()

try:
    salary_data = load_salary_data(SALARY_PATH)
    skill_tables = load_skill_tables(DATA_DIR)
except FileNotFoundError as error:
    st.error(f"Missing data file: {error}")
    st.stop()

# ============================================================
# Sidebar filters
# ============================================================

st.sidebar.title("Dashboard Filters")
st.sidebar.caption("Keep filters on **All** for the full project view. Adjust them only when exploring a specific segment.")

selected_year = st.sidebar.selectbox("Year", ["All"] + sorted(salary_data["work_year"].unique().tolist()))
selected_role = st.sidebar.selectbox("Role Group", ["All"] + sorted(salary_data["role_group"].unique().tolist()))
selected_experience = st.sidebar.selectbox("Experience Level", ["All"] + EXPERIENCE_ORDER)
selected_remote = st.sidebar.selectbox("Work Type", ["All"] + REMOTE_ORDER)
selected_country = st.sidebar.selectbox("Company Country", ["All"] + sorted(salary_data["company_country"].dropna().unique().tolist()))

filtered_salary = salary_data.copy()

if selected_year != "All":
    filtered_salary = filtered_salary[filtered_salary["work_year"] == selected_year]
if selected_role != "All":
    filtered_salary = filtered_salary[filtered_salary["role_group"] == selected_role]
if selected_experience != "All":
    filtered_salary = filtered_salary[filtered_salary["experience_label"] == selected_experience]
if selected_remote != "All":
    filtered_salary = filtered_salary[filtered_salary["remote_label"] == selected_remote]
if selected_country != "All":
    filtered_salary = filtered_salary[filtered_salary["company_country"] == selected_country]

st.sidebar.divider()
st.sidebar.subheader("Data Scope")
st.sidebar.write("Salary data: **607 records** from 2020–2022.")
st.sidebar.write("Skill data: **668,704 job postings** with skill information.")
st.sidebar.write("Skill analysis uses prepared summary files for faster dashboard loading.")

if filtered_salary.empty:
    st.warning("No data matches the selected filters. Please choose a broader filter combination.")
    st.stop()

# ============================================================
# Header
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Data Analyst Job Market Dashboard</div>
        <div class="hero-subtitle">
            A clean portfolio dashboard analyzing salary trends, role demand, remote work, required skills, country compensation, and career opportunities across Data Analyst and broader data roles.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_row(filtered_salary)

st.write("")

# ============================================================
# Tabs
# ============================================================

overview_tab, salary_tab, skills_tab, opportunity_tab = st.tabs(
    ["Overview", "Salary Insights", "Skills", "Career Opportunity"]
)

# ============================================================
# Overview
# ============================================================

with overview_tab:
    st.subheader("Executive Summary")
    st.markdown(
        "<div class='section-caption'>This section gives the fastest reading of the project: which roles dominate, what the main findings are, and what limitations should be considered.</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.35, 1])

    with left:
        role_summary = filtered_salary["role_group"].value_counts().reset_index()
        role_summary.columns = ["role_group", "total"]
        role_summary = role_summary.sort_values("total", ascending=True)

        fig = horizontal_bar(
            role_summary,
            x="total",
            y="role_group",
            title="Most Common Role Groups",
            text="total",
            height=480,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Data Scientist, Data Engineer, and Data Analyst are the largest role groups in the salary dataset.")

    with right:
        insight_card(
            "Main finding",
            "<strong>Data Scientist, Data Engineer, and Data Analyst</strong> are the most dominant role groups in the salary dataset.",
        )
        insight_card(
            "Data Analyst position",
            "Data Analyst remains a realistic entry point with <strong>$90,320 median salary</strong> in the full salary dataset and strong remote availability.",
        )
        insight_card(
            "Skills priority",
            "The core Data Analyst stack is <strong>SQL, Excel, Python, Tableau, and Power BI</strong>. Cloud and big data tools are valuable premium skills.",
        )
        insight_card(
            "Career direction",
            "Data Scientist and Data Engineer score highest in career opportunity, while Data Analyst is a strong starting point for students and beginners.",
        )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        exp_summary = (
            filtered_salary.groupby("experience_label")
            .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
            .reindex(EXPERIENCE_ORDER)
            .reset_index()
            .dropna()
        )
        fig = px.bar(
            exp_summary,
            x="experience_label",
            y="median_salary",
            text="median_salary",
            color_discrete_sequence=COLOR_SEQUENCE,
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(title="Median Salary by Experience Level", xaxis_title=None, yaxis_title="Median salary USD")
        st.plotly_chart(dark_layout(fig, height=420), use_container_width=True)
        st.caption("Experience level is one of the strongest salary differentiators in the dataset.")

    with c2:
        remote_summary = (
            filtered_salary.groupby("remote_label")
            .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
            .reindex(REMOTE_ORDER)
            .reset_index()
            .dropna()
        )
        fig = px.bar(
            remote_summary,
            x="remote_label",
            y="median_salary",
            text="median_salary",
            color_discrete_sequence=COLOR_SEQUENCE,
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(title="Median Salary by Work Type", xaxis_title=None, yaxis_title="Median salary USD")
        st.plotly_chart(dark_layout(fig, height=420), use_container_width=True)
        st.caption("Fully Remote roles show the highest median salary in the dataset, but this should not be read as direct causation.")

    st.divider()

    note_card(
        "<strong>Methodology notes:</strong> The salary dataset contains 607 records. Some categories have small sample sizes, such as Data Architect and Executive Level Data Analyst. Country salary results are strongly influenced by the large number of United States records. Salary-skill analysis is based only on job postings that include salary information."
    )

# ============================================================
# Salary Insights
# ============================================================

with salary_tab:
    st.subheader("Salary Insights")
    st.markdown(
        "<div class='section-caption'>This section compares salary by role, experience level, work type, and company country. Median salary is emphasized because salary data often contains outliers.</div>",
        unsafe_allow_html=True,
    )

    salary_by_role = (
        filtered_salary.groupby("role_group")
        .agg(
            total_data=("salary_in_usd", "count"),
            median_salary=("salary_in_usd", "median"),
            average_salary=("salary_in_usd", "mean"),
            min_salary=("salary_in_usd", "min"),
            max_salary=("salary_in_usd", "max"),
        )
        .reset_index()
        .sort_values("median_salary", ascending=False)
    )

    left, right = st.columns([1.05, 1])

    with left:
        fig = horizontal_bar(
            salary_by_role.sort_values("median_salary"),
            x="median_salary",
            y="role_group",
            title="Median Salary by Role Group",
            text="median_salary",
            height=500,
        )
        fig.update_traces(texttemplate="$%{text:,.0f}")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Data Analyst salary is competitive for an entry path, while Data Engineer and Data Scientist show higher median salaries.")

    with right:
        fig = px.box(
            filtered_salary,
            x="salary_in_usd",
            y="role_group",
            color="role_group",
            color_discrete_sequence=COLOR_SEQUENCE,
            points="outliers",
        )
        fig.update_layout(title="Salary Distribution by Role Group", xaxis_title="Salary USD", yaxis_title=None, showlegend=False)
        st.plotly_chart(dark_layout(fig, height=500), use_container_width=True)
        st.caption("The boxplot shows outliers and salary spread across different role groups.")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        exp_salary = (
            filtered_salary.groupby("experience_label")
            .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
            .reindex(EXPERIENCE_ORDER)
            .reset_index()
            .dropna()
        )
        fig = px.bar(exp_salary, x="experience_label", y="median_salary", text="median_salary", color_discrete_sequence=COLOR_SEQUENCE)
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(title="Experience Level Impact", xaxis_title=None, yaxis_title="Median salary USD")
        st.plotly_chart(dark_layout(fig, height=420), use_container_width=True)

    with c2:
        remote_salary = (
            filtered_salary.groupby("remote_label")
            .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
            .reindex(REMOTE_ORDER)
            .reset_index()
            .dropna()
        )
        fig = px.bar(remote_salary, x="remote_label", y="median_salary", text="median_salary", color_discrete_sequence=COLOR_SEQUENCE)
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(title="Remote Work Salary Comparison", xaxis_title=None, yaxis_title="Median salary USD")
        st.plotly_chart(dark_layout(fig, height=420), use_container_width=True)

    st.divider()

    st.subheader("Data Analyst Focus")
    da_data = filtered_salary[filtered_salary["role_group"] == "Data Analyst"].copy()

    if da_data.empty:
        st.info("No Data Analyst records are available for the selected filters.")
    else:
        da1, da2, da3, da4 = st.columns(4)
        da1.metric("Data Analyst Records", f"{len(da_data):,}")
        da2.metric("Median Salary", format_usd(da_data["salary_in_usd"].median()))
        da3.metric("Fully Remote Share", format_percent(da_data["remote_label"].eq("Fully Remote").mean() * 100))
        da4.metric("Top Country", da_data["company_country"].value_counts().idxmax())

        da_exp = (
            da_data.groupby("experience_label")
            .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
            .reindex(EXPERIENCE_ORDER)
            .reset_index()
            .dropna()
        )
        da_remote = (
            da_data.groupby("remote_label")
            .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
            .reindex(REMOTE_ORDER)
            .reset_index()
            .dropna()
        )

        a, b = st.columns(2)
        with a:
            fig = px.bar(da_exp, x="experience_label", y="median_salary", text="median_salary", color_discrete_sequence=COLOR_SEQUENCE)
            fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            fig.update_layout(title="Data Analyst Salary by Experience", xaxis_title=None, yaxis_title="Median salary USD")
            st.plotly_chart(dark_layout(fig, height=420), use_container_width=True)
        with b:
            fig = px.bar(da_remote, x="remote_label", y="median_salary", text="median_salary", color_discrete_sequence=COLOR_SEQUENCE)
            fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            fig.update_layout(title="Data Analyst Salary by Work Type", xaxis_title=None, yaxis_title="Median salary USD")
            st.plotly_chart(dark_layout(fig, height=420), use_container_width=True)

    st.divider()

    country_salary = (
        filtered_salary.groupby("company_country")
        .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
        .reset_index()
    )
    country_salary = country_salary[country_salary["total_data"] >= 5].sort_values("median_salary", ascending=False).head(10)

    fig = horizontal_bar(
        country_salary.sort_values("median_salary"),
        x="median_salary",
        y="company_country",
        title="Top Countries by Median Salary (minimum 5 records)",
        text="median_salary",
        height=470,
    )
    fig.update_traces(texttemplate="$%{text:,.0f}")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("United States has the highest median salary among countries with sufficient records in this dataset.")

    with st.expander("View salary summary table"):
        table = salary_by_role.copy()
        for col in ["median_salary", "average_salary", "min_salary", "max_salary"]:
            table[col] = table[col].round(0)
        st.dataframe(table, use_container_width=True, hide_index=True)

# ============================================================
# Skills
# ============================================================

with skills_tab:
    st.subheader("Skill Demand Analysis")
    st.markdown(
        "<div class='section-caption'>Skill analysis uses prepared summaries from job postings with skill information. It answers what companies ask for and what Data Analyst candidates should prioritize.</div>",
        unsafe_allow_html=True,
    )

    skill_overall = skill_tables["skill_overall"].copy()
    skill_da = skill_tables["skill_data_analyst"].copy()
    skill_matrix = skill_tables["skill_role_matrix"].copy().set_index("skill")
    remote_compare = skill_tables["remote_skill_compare"].copy()
    skill_recommendation = skill_tables["skill_recommendation"].copy()

    left, right = st.columns(2)

    with left:
        fig = horizontal_bar(
            skill_overall.head(15).sort_values("total_mentions"),
            x="total_mentions",
            y="skill",
            title="Most Required Skills Overall",
            text="percentage",
            height=520,
        )
        fig.update_traces(texttemplate="%{text:.1f}%")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("SQL and Python are the top skills overall, both appearing in more than half of job postings with skill data.")

    with right:
        fig = horizontal_bar(
            skill_da.head(15).sort_values("total_mentions"),
            x="total_mentions",
            y="skill",
            title="Most Required Skills for Data Analyst",
            text="percentage",
            height=520,
        )
        fig.update_traces(texttemplate="%{text:.1f}%")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("For Data Analyst roles, SQL, Excel, Python, Tableau, and Power BI form the core skill stack.")

    st.divider()

    st.subheader("Skill Difference Across Roles")
    fig = px.imshow(
        skill_matrix,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale="Blues",
    )
    fig.update_layout(title="Skill Percentage by Role", xaxis_title="Role", yaxis_title="Skill")
    st.plotly_chart(dark_layout(fig, height=560), use_container_width=True)
    st.caption("Data Analyst roles lean toward analytics and reporting, while Data Engineer and Machine Learning roles require more technical infrastructure and modeling tools.")

    st.divider()

    st.subheader("Remote Job Skills")
    remote_long = remote_compare.melt(
        id_vars="skill",
        value_vars=["remote_percentage", "non_remote_percentage"],
        var_name="work_type",
        value_name="percentage",
    )
    remote_long["work_type"] = remote_long["work_type"].replace({
        "remote_percentage": "Work From Home",
        "non_remote_percentage": "On-site / Not Mentioned",
    })

    fig = px.bar(
        remote_long,
        x="percentage",
        y="skill",
        color="work_type",
        orientation="h",
        barmode="group",
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(title="Remote vs Non-Remote Skill Requirement", xaxis_title="Percentage of job postings", yaxis_title=None, legend_title="Work type")
    st.plotly_chart(dark_layout(fig, height=620), use_container_width=True)
    st.caption("Remote jobs show stronger emphasis on Python, SQL, AWS, Snowflake, Spark, and Databricks.")

    st.divider()

    st.subheader("Data Analyst Learning Priority")
    priority_order = ["Wajib dipelajari", "BI & reporting tools", "Skill premium", "Skill pendukung utama", "Skill tambahan"]
    selected_skills = [
        "sql", "excel", "python", "tableau", "power bi", "looker",
        "aws", "azure", "snowflake", "spark", "hadoop", "gcp", "databricks", "airflow", "kafka",
    ]
    rec = skill_recommendation[skill_recommendation["skill"].isin(selected_skills)].copy()
    rec["learning_priority"] = pd.Categorical(rec["learning_priority"], categories=priority_order, ordered=True)
    rec = rec.sort_values(["learning_priority", "demand_percentage"], ascending=[True, False])

    fig = px.bar(
        rec.sort_values("demand_percentage"),
        x="demand_percentage",
        y="skill",
        color="learning_priority",
        text="median_salary",
        orientation="h",
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside", cliponaxis=False)
    fig.update_layout(title="Recommended Data Analyst Skills by Demand and Salary", xaxis_title="Demand in Data Analyst postings (%)", yaxis_title=None, legend_title="Learning priority")
    st.plotly_chart(dark_layout(fig, height=620), use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        insight_card("Core skills", "Start with <strong>SQL, Excel, and Python</strong>. These are the highest-demand Data Analyst skills.")
    with c2:
        insight_card("Reporting tools", "Add <strong>Tableau</strong> or <strong>Power BI</strong> to support dashboards, reporting, and business communication.")
    with c3:
        insight_card("Premium skills", "Cloud and big data tools such as <strong>AWS, Azure, GCP, Snowflake, Spark, Databricks, Airflow, and Kafka</strong> can improve competitiveness.")

# ============================================================
# Career Opportunity
# ============================================================

with opportunity_tab:
    st.subheader("Career Opportunity Score")
    st.markdown(
        "<div class='section-caption'>Opportunity Score ranks roles using a simple weighted formula: 40% demand, 40% median salary, and 20% fully remote availability.</div>",
        unsafe_allow_html=True,
    )

    role_opportunity = (
        filtered_salary.groupby("role_group")
        .agg(
            total_data=("salary_in_usd", "count"),
            median_salary=("salary_in_usd", "median"),
            fully_remote_jobs=("remote_label", lambda x: (x == "Fully Remote").sum()),
        )
        .reset_index()
    )

    role_opportunity = role_opportunity[role_opportunity["total_data"] >= 10].copy()

    if role_opportunity.empty:
        st.info("No role has at least 10 records under the selected filters. Broaden the filters to view Opportunity Score.")
    else:
        role_opportunity["remote_percentage"] = role_opportunity["fully_remote_jobs"] / role_opportunity["total_data"] * 100
        role_opportunity["demand_score"] = role_opportunity["total_data"] / role_opportunity["total_data"].max() * 100
        role_opportunity["salary_score"] = role_opportunity["median_salary"] / role_opportunity["median_salary"].max() * 100
        role_opportunity["remote_score"] = role_opportunity["remote_percentage"] / role_opportunity["remote_percentage"].max() * 100
        role_opportunity["opportunity_score"] = (
            0.4 * role_opportunity["demand_score"]
            + 0.4 * role_opportunity["salary_score"]
            + 0.2 * role_opportunity["remote_score"]
        )
        role_opportunity = role_opportunity.round(2).sort_values("opportunity_score", ascending=False)

        left, right = st.columns([1, 1])

        with left:
            fig = horizontal_bar(
                role_opportunity.sort_values("opportunity_score"),
                x="opportunity_score",
                y="role_group",
                title="Opportunity Score Ranking",
                text="opportunity_score",
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.scatter(
                role_opportunity,
                x="total_data",
                y="median_salary",
                size="remote_percentage",
                text="role_group",
                color="role_group",
                color_discrete_sequence=COLOR_SEQUENCE,
                hover_data=["opportunity_score", "remote_percentage"],
            )
            fig.update_traces(textposition="top center")
            fig.update_layout(title="Demand vs Salary", xaxis_title="Number of records", yaxis_title="Median salary USD", showlegend=False)
            st.plotly_chart(dark_layout(fig, height=500), use_container_width=True)

        top_role = role_opportunity.iloc[0]
        insight_card(
            "Top opportunity role",
            f"<strong>{top_role['role_group']}</strong> has the highest Opportunity Score under the current filters. Median salary: <strong>{format_usd(top_role['median_salary'])}</strong>. Fully remote share: <strong>{top_role['remote_percentage']:.2f}%</strong>.",
        )

        with st.expander("View Opportunity Score table"):
            st.dataframe(role_opportunity, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("Recommended Career Roadmap for Aspiring Data Analysts")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        insight_card("Step 1", "Build a foundation with <strong>SQL, Excel, basic statistics, and Python</strong>.")
    with r2:
        insight_card("Step 2", "Create dashboards using <strong>Tableau or Power BI</strong> and practice business storytelling.")
    with r3:
        insight_card("Step 3", "Add premium tools such as <strong>Snowflake, BigQuery, AWS, Azure, GCP, Spark, and Databricks</strong>.")
    with r4:
        insight_card("Step 4", "Grow toward <strong>Data Scientist, Data Engineer, Analytics Engineer, or Data Architect</strong> roles.")

    note_card(
        "<strong>Final takeaway:</strong> Data Analyst is a strong entry point for students and beginners. To increase career competitiveness, core analytics skills should be combined with cloud, big data, and data engineering fundamentals."
    )

# ============================================================
# Footer
# ============================================================

st.divider()
st.caption("Created by Muh. Shafwan Faiq R. · Data Science portfolio project · Built with Python and Streamlit")
