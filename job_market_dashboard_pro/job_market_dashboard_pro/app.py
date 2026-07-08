from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# Page setup
# ============================================================

st.set_page_config(
    page_title="Data Analyst Job Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SALARY_PATH = DATA_DIR / "ds_salaries.csv"

COLOR_SEQUENCE = [
    "#2563eb", "#16a34a", "#f97316", "#9333ea", "#dc2626",
    "#0891b2", "#ca8a04", "#4f46e5", "#059669", "#be123c"
]


# ============================================================
# Styling
# ============================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        .main-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            font-size: 1rem;
            color: #64748b;
            margin-bottom: 1rem;
        }
        .insight-box {
            padding: 1rem 1.1rem;
            border-radius: 0.8rem;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
        }
        .insight-box b {
            color: #0f172a;
        }
        .section-note {
            color: #475569;
            font-size: 0.95rem;
        }
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 1rem;
            border-radius: 0.8rem;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
        }
        div[data-testid="stMetricLabel"] {
            color: #64748b;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# Helper functions
# ============================================================


def format_usd(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"${value:,.0f}"


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
    "AS": "American Samoa"
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
        "EX": "Executive Level"
    }

    employment_map = {
        "FT": "Full-time",
        "PT": "Part-time",
        "CT": "Contract",
        "FL": "Freelance"
    }

    remote_map = {
        0: "On-site",
        50: "Hybrid",
        100: "Fully Remote"
    }

    company_size_map = {
        "S": "Small",
        "M": "Medium",
        "L": "Large"
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
def load_skill_tables(data_dir: Path) -> dict:
    skill_overall = pd.read_csv(data_dir / "skill_overall.csv")
    skill_data_analyst = pd.read_csv(data_dir / "skill_data_analyst.csv")
    skill_role_matrix = pd.read_csv(data_dir / "skill_role_matrix.csv").set_index("skill")
    remote_skill_compare = pd.read_csv(data_dir / "remote_skill_compare.csv")
    skill_recommendation = pd.read_csv(data_dir / "skill_recommendation.csv")

    return {
        "skill_overall": skill_overall,
        "skill_data_analyst": skill_data_analyst,
        "skill_role_matrix": skill_role_matrix,
        "remote_skill_compare": remote_skill_compare,
        "skill_recommendation": skill_recommendation,
    }


def make_horizontal_bar(df: pd.DataFrame, x: str, y: str, title: str, text: str | None = None) -> go.Figure:
    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        text=text,
        title=title,
        color_discrete_sequence=COLOR_SEQUENCE,
        template="plotly_white"
    )
    fig.update_layout(
        height=450,
        title_x=0.02,
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=10, r=20, t=70, b=40)
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    return fig


def section_insight(text: str) -> None:
    st.markdown(f"<div class='insight-box'>{text}</div>", unsafe_allow_html=True)


# ============================================================
# Load data
# ============================================================

if not SALARY_PATH.exists():
    st.error("File `data/ds_salaries.csv` belum ditemukan. Pastikan file dataset salary ada di folder data.")
    st.stop()

salary_data = load_salary_data(SALARY_PATH)
skill_tables = load_skill_tables(DATA_DIR)


# ============================================================
# Sidebar filters
# ============================================================

st.sidebar.title("Filter Dashboard")
st.sidebar.caption("Gunakan filter ini untuk melihat insight berdasarkan tahun, role, negara, experience, dan tipe kerja.")

all_years = sorted(salary_data["work_year"].unique().tolist())
selected_years = st.sidebar.multiselect("Tahun", all_years, default=all_years)

all_roles = sorted(salary_data["role_group"].unique().tolist())
selected_roles = st.sidebar.multiselect("Role group", all_roles, default=all_roles)

experience_order = ["Entry Level", "Mid Level", "Senior Level", "Executive Level"]
selected_experience = st.sidebar.multiselect("Experience level", experience_order, default=experience_order)

remote_order = ["On-site", "Hybrid", "Fully Remote"]
selected_remote = st.sidebar.multiselect("Tipe kerja", remote_order, default=remote_order)

all_countries = sorted(salary_data["company_country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect("Negara perusahaan", all_countries, default=all_countries)

st.sidebar.divider()
st.sidebar.markdown("**Catatan data**")
st.sidebar.write("Dataset salary berisi 607 data dari tahun 2020-2022. Bagian skill memakai ringkasan dari dataset job posting `lukebarousse/data_jobs`.")

filtered_salary = salary_data[
    salary_data["work_year"].isin(selected_years)
    & salary_data["role_group"].isin(selected_roles)
    & salary_data["experience_label"].isin(selected_experience)
    & salary_data["remote_label"].isin(selected_remote)
    & salary_data["company_country"].isin(selected_countries)
].copy()

if filtered_salary.empty:
    st.warning("Tidak ada data yang sesuai dengan filter. Coba longgarkan filter di sidebar.")
    st.stop()


# ============================================================
# Header
# ============================================================

st.markdown("<div class='main-title'>Data Analyst Job Market Dashboard</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Dashboard untuk membaca demand role, salary, remote work, negara kompensasi, skill yang dicari, dan rekomendasi karier di bidang Data Science.</div>",
    unsafe_allow_html=True
)

# KPI cards
total_jobs = len(filtered_salary)
median_salary = filtered_salary["salary_in_usd"].median()
avg_salary = filtered_salary["salary_in_usd"].mean()
remote_percentage = filtered_salary["remote_label"].eq("Fully Remote").mean() * 100
top_role = filtered_salary["role_group"].value_counts().index[0]
top_country = filtered_salary["company_country"].value_counts().index[0]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total data", f"{total_jobs:,}")
col2.metric("Median salary", format_usd(median_salary))
col3.metric("Average salary", format_usd(avg_salary))
col4.metric("Fully remote", f"{remote_percentage:.1f}%")
col5.metric("Top role", top_role)


# ============================================================
# Tabs
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Executive Summary",
    "Role & Salary",
    "Data Analyst Focus",
    "Skills",
    "Country & Remote",
    "Opportunity Score"
])


# ============================================================
# Executive Summary
# ============================================================

with tab1:
    st.subheader("Ringkasan Insight")

    left, right = st.columns([1.1, 0.9])

    with left:
        role_summary = (
            filtered_salary["role_group"].value_counts()
            .reset_index()
        )
        role_summary.columns = ["role_group", "total"]
        role_summary["percentage"] = role_summary["total"] / len(filtered_salary) * 100

        fig = make_horizontal_bar(
            role_summary.sort_values("total"),
            x="total",
            y="role_group",
            title="Role paling banyak muncul",
            text="total"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### Pesan utama")
        section_insight(
            "<b>Data Scientist, Data Engineer, dan Data Analyst</b> adalah role yang paling dominan. "
            "Data Analyst tetap menarik sebagai jalur awal karena demand-nya cukup tinggi dan skill dasarnya jelas."
        )
        section_insight(
            "<b>Experience level</b> punya dampak besar terhadap salary. Kenaikan paling terasa biasanya terjadi saat masuk ke level senior."
        )
        section_insight(
            "Skill dasar Data Analyst adalah <b>SQL, Excel, Python, Tableau, dan Power BI</b>. Skill premium seperti cloud, Snowflake, Spark, dan Databricks bisa meningkatkan value."
        )

    st.divider()

    salary_by_exp = (
        filtered_salary.groupby("experience_label")
        .agg(median_salary=("salary_in_usd", "median"), total_data=("salary_in_usd", "count"))
        .reindex(experience_order)
        .reset_index()
        .dropna()
    )

    salary_by_remote = (
        filtered_salary.groupby("remote_label")
        .agg(median_salary=("salary_in_usd", "median"), total_data=("salary_in_usd", "count"))
        .reindex(remote_order)
        .reset_index()
        .dropna()
    )

    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.bar(
            salary_by_exp,
            x="experience_label",
            y="median_salary",
            text="median_salary",
            title="Median salary berdasarkan experience",
            color_discrete_sequence=COLOR_SEQUENCE,
            template="plotly_white"
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(height=420, title_x=0.02, xaxis_title=None, yaxis_title="Median salary USD")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig = px.bar(
            salary_by_remote,
            x="remote_label",
            y="median_salary",
            text="median_salary",
            title="Median salary berdasarkan tipe kerja",
            color_discrete_sequence=COLOR_SEQUENCE,
            template="plotly_white"
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(height=420, title_x=0.02, xaxis_title=None, yaxis_title="Median salary USD")
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# Role & Salary
# ============================================================

with tab2:
    st.subheader("Role demand dan benchmark salary")
    st.markdown("<div class='section-note'>Bagian ini menunjukkan role mana yang paling banyak muncul dan bagaimana salary-nya dibandingkan antar role.</div>", unsafe_allow_html=True)

    salary_by_role = (
        filtered_salary.groupby("role_group")
        .agg(
            total_data=("salary_in_usd", "count"),
            median_salary=("salary_in_usd", "median"),
            average_salary=("salary_in_usd", "mean"),
            min_salary=("salary_in_usd", "min"),
            max_salary=("salary_in_usd", "max")
        )
        .reset_index()
        .sort_values("median_salary", ascending=False)
    )

    left, right = st.columns(2)

    with left:
        fig = make_horizontal_bar(
            salary_by_role.sort_values("median_salary"),
            x="median_salary",
            y="role_group",
            title="Median salary berdasarkan role",
            text="median_salary"
        )
        fig.update_traces(texttemplate="$%{text:,.0f}")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.box(
            filtered_salary,
            x="salary_in_usd",
            y="role_group",
            title="Distribusi salary berdasarkan role",
            color="role_group",
            color_discrete_sequence=COLOR_SEQUENCE,
            template="plotly_white"
        )
        fig.update_layout(height=450, title_x=0.02, xaxis_title="Salary USD", yaxis_title=None, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    display_salary_by_role = salary_by_role.copy()
    for column in ["median_salary", "average_salary", "min_salary", "max_salary"]:
        display_salary_by_role[column] = display_salary_by_role[column].round(0)

    with st.expander("Lihat tabel salary berdasarkan role"):
        st.dataframe(display_salary_by_role, use_container_width=True)

    section_insight(
        "<b>Insight:</b> Data Analyst memiliki salary yang kompetitif sebagai role awal, tetapi Data Engineer dan Data Scientist cenderung memiliki median salary lebih tinggi. "
        "Ini bisa menjadi arah pengembangan karier setelah skill dasar Data Analyst kuat."
    )

    st.divider()

    top_titles = filtered_salary["job_title"].value_counts().head(15).reset_index()
    top_titles.columns = ["job_title", "total"]
    fig = make_horizontal_bar(
        top_titles.sort_values("total"),
        x="total",
        y="job_title",
        title="Top 15 job title paling banyak muncul",
        text="total"
    )
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# Data Analyst Focus
# ============================================================

with tab3:
    st.subheader("Fokus Data Analyst")

    da_data = filtered_salary[filtered_salary["role_group"] == "Data Analyst"].copy()

    if da_data.empty:
        st.warning("Tidak ada data Data Analyst pada filter saat ini.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Data Analyst data", f"{len(da_data):,}")
        c2.metric("Median salary DA", format_usd(da_data["salary_in_usd"].median()))
        c3.metric("Fully remote DA", f"{da_data['remote_label'].eq('Fully Remote').mean() * 100:.1f}%")
        c4.metric("Top country DA", da_data["company_country"].value_counts().index[0])

        da_exp = (
            da_data.groupby("experience_label")
            .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
            .reindex(experience_order)
            .reset_index()
            .dropna()
        )
        da_remote = (
            da_data.groupby("remote_label")
            .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
            .reindex(remote_order)
            .reset_index()
            .dropna()
        )

        left, right = st.columns(2)

        with left:
            fig = px.bar(
                da_exp,
                x="experience_label",
                y="median_salary",
                text="median_salary",
                title="Median salary Data Analyst berdasarkan experience",
                color_discrete_sequence=COLOR_SEQUENCE,
                template="plotly_white"
            )
            fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            fig.update_layout(height=420, title_x=0.02, xaxis_title=None, yaxis_title="Median salary USD")
            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.bar(
                da_remote,
                x="remote_label",
                y="median_salary",
                text="median_salary",
                title="Median salary Data Analyst berdasarkan tipe kerja",
                color_discrete_sequence=COLOR_SEQUENCE,
                template="plotly_white"
            )
            fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            fig.update_layout(height=420, title_x=0.02, xaxis_title=None, yaxis_title="Median salary USD")
            st.plotly_chart(fig, use_container_width=True)

        da_country = (
            da_data.groupby("company_country")
            .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
            .reset_index()
        )
        da_country = da_country[da_country["total_data"] >= 3].sort_values("median_salary", ascending=False)

        if not da_country.empty:
            fig = make_horizontal_bar(
                da_country.head(10).sort_values("median_salary"),
                x="median_salary",
                y="company_country",
                title="Median salary Data Analyst berdasarkan negara perusahaan",
                text="median_salary"
            )
            fig.update_traces(texttemplate="$%{text:,.0f}")
            st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("Skill rekomendasi untuk Data Analyst")

        rec = skill_tables["skill_recommendation"].copy()
        selected_skill_rows = rec[rec["skill"].isin([
            "sql", "excel", "python", "tableau", "power bi", "looker",
            "aws", "azure", "snowflake", "spark", "hadoop", "gcp", "databricks"
        ])].sort_values("demand_percentage")

        fig = px.bar(
            selected_skill_rows,
            x="demand_percentage",
            y="skill",
            orientation="h",
            text="median_salary",
            color="learning_priority",
            title="Skill Data Analyst: demand dan median salary",
            color_discrete_sequence=COLOR_SEQUENCE,
            template="plotly_white"
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(height=520, title_x=0.02, xaxis_title="Persentase muncul di job posting Data Analyst", yaxis_title=None, legend_title="Prioritas")
        st.plotly_chart(fig, use_container_width=True)

        section_insight(
            "<b>Rekomendasi:</b> mulai dari SQL, Excel, dan Python. Setelah itu kuasai Tableau atau Power BI. "
            "Untuk menaikkan daya saing, tambahkan cloud tools, Snowflake, Spark, Databricks, Airflow, dan Kafka."
        )


# ============================================================
# Skills
# ============================================================

with tab4:
    st.subheader("Skill yang dicari perusahaan")
    st.markdown("<div class='section-note'>Bagian ini memakai ringkasan dataset job posting untuk menjawab skill apa yang paling sering diminta.</div>", unsafe_allow_html=True)

    skill_overall = skill_tables["skill_overall"]
    skill_da = skill_tables["skill_data_analyst"]
    matrix = skill_tables["skill_role_matrix"]
    remote_compare = skill_tables["remote_skill_compare"]

    left, right = st.columns(2)

    with left:
        fig = make_horizontal_bar(
            skill_overall.head(15).sort_values("total_mentions"),
            x="total_mentions",
            y="skill",
            title="Top skill paling banyak dicari secara umum",
            text="percentage"
        )
        fig.update_traces(texttemplate="%{text:.1f}%")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = make_horizontal_bar(
            skill_da.head(15).sort_values("total_mentions"),
            x="total_mentions",
            y="skill",
            title="Top skill paling banyak dicari untuk Data Analyst",
            text="percentage"
        )
        fig.update_traces(texttemplate="%{text:.1f}%")
        st.plotly_chart(fig, use_container_width=True)

    section_insight(
        "<b>Insight:</b> SQL dan Python adalah skill paling dominan secara umum. Untuk Data Analyst, skill utama bergeser menjadi SQL, Excel, Python, Tableau, dan Power BI."
    )

    st.divider()

    st.subheader("Perbedaan skill antar role")
    fig = px.imshow(
        matrix,
        text_auto=".1f",
        aspect="auto",
        title="Persentase skill utama pada setiap role",
        color_continuous_scale="Blues",
        template="plotly_white"
    )
    fig.update_layout(height=560, title_x=0.02, xaxis_title="Role", yaxis_title="Skill")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Skill yang lebih menonjol pada remote job")
    remote_long = remote_compare.melt(
        id_vars="skill",
        value_vars=["remote_percentage", "non_remote_percentage"],
        var_name="work_type",
        value_name="percentage"
    )
    remote_long["work_type"] = remote_long["work_type"].replace({
        "remote_percentage": "Work From Home",
        "non_remote_percentage": "On-site / Not Mentioned"
    })

    fig = px.bar(
        remote_long,
        x="percentage",
        y="skill",
        color="work_type",
        orientation="h",
        barmode="group",
        title="Remote vs non-remote skill requirement",
        color_discrete_sequence=COLOR_SEQUENCE,
        template="plotly_white"
    )
    fig.update_layout(height=600, title_x=0.02, xaxis_title="Persentase job posting", yaxis_title=None, legend_title="Tipe kerja")
    st.plotly_chart(fig, use_container_width=True)

    section_insight(
        "<b>Insight:</b> remote job lebih kuat pada Python, SQL, AWS, Snowflake, Spark, dan Databricks. Ini menunjukkan bahwa remote role cenderung lebih teknis dan kompetitif."
    )


# ============================================================
# Country & Remote
# ============================================================

with tab5:
    st.subheader("Negara kompensasi dan remote work")

    min_country_data = st.slider("Minimal data per negara", 1, 30, 5, key="country_min_slider")

    country_salary = (
        filtered_salary.groupby("company_country")
        .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"), average_salary=("salary_in_usd", "mean"))
        .reset_index()
    )

    country_filtered = country_salary[country_salary["total_data"] >= min_country_data].sort_values("median_salary", ascending=False)
    country_count = (
        filtered_salary.groupby("company_country")
        .size()
        .reset_index(name="total_data")
        .sort_values("total_data", ascending=False)
    )

    left, right = st.columns(2)

    with left:
        fig = make_horizontal_bar(
            country_filtered.head(10).sort_values("median_salary"),
            x="median_salary",
            y="company_country",
            title="Negara dengan median salary tertinggi",
            text="median_salary"
        )
        fig.update_traces(texttemplate="$%{text:,.0f}")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = make_horizontal_bar(
            country_count.head(10).sort_values("total_data"),
            x="total_data",
            y="company_country",
            title="Negara berdasarkan jumlah data job",
            text="total_data"
        )
        st.plotly_chart(fig, use_container_width=True)

    remote_exp = (
        filtered_salary.groupby(["experience_label", "remote_label"])
        .agg(total_data=("salary_in_usd", "count"), median_salary=("salary_in_usd", "median"))
        .reset_index()
    )
    remote_exp["experience_label"] = pd.Categorical(remote_exp["experience_label"], categories=experience_order, ordered=True)
    remote_exp["remote_label"] = pd.Categorical(remote_exp["remote_label"], categories=remote_order, ordered=True)
    remote_exp = remote_exp.sort_values(["experience_label", "remote_label"])

    fig = px.bar(
        remote_exp,
        x="experience_label",
        y="median_salary",
        color="remote_label",
        barmode="group",
        text="median_salary",
        title="Median salary tipe kerja berdasarkan experience level",
        color_discrete_sequence=COLOR_SEQUENCE,
        template="plotly_white"
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(height=520, title_x=0.02, xaxis_title="Experience level", yaxis_title="Median salary USD", legend_title="Tipe kerja")
    st.plotly_chart(fig, use_container_width=True)

    section_insight(
        "<b>Insight:</b> United States menjadi negara paling dominan dalam dataset salary. Fully remote terlihat memiliki median salary lebih tinggi, tetapi hasil ini perlu dibaca bersama experience level dan lokasi perusahaan."
    )


# ============================================================
# Opportunity Score
# ============================================================

with tab6:
    st.subheader("Opportunity Score untuk rekomendasi karier")
    st.write("Skor ini membantu membaca role mana yang menarik dari sisi demand, salary, dan peluang remote.")

    weight_col1, weight_col2, weight_col3 = st.columns(3)
    demand_weight = weight_col1.slider("Bobot demand", 0.0, 1.0, 0.4, 0.05)
    salary_weight = weight_col2.slider("Bobot salary", 0.0, 1.0, 0.4, 0.05)
    remote_weight = weight_col3.slider("Bobot remote", 0.0, 1.0, 0.2, 0.05)

    total_weight = demand_weight + salary_weight + remote_weight
    if total_weight == 0:
        st.warning("Minimal satu bobot harus lebih dari 0.")
        st.stop()

    demand_weight = demand_weight / total_weight
    salary_weight = salary_weight / total_weight
    remote_weight = remote_weight / total_weight

    min_role_data = st.slider("Minimal data per role", 1, 30, 10, key="role_min_slider")

    role_opportunity = (
        filtered_salary.groupby("role_group")
        .agg(
            total_data=("salary_in_usd", "count"),
            median_salary=("salary_in_usd", "median"),
            fully_remote_jobs=("remote_label", lambda x: (x == "Fully Remote").sum())
        )
        .reset_index()
    )

    role_opportunity = role_opportunity[role_opportunity["total_data"] >= min_role_data].copy()

    if role_opportunity.empty:
        st.warning("Tidak ada role yang memenuhi minimal data.")
    else:
        role_opportunity["remote_percentage"] = role_opportunity["fully_remote_jobs"] / role_opportunity["total_data"] * 100
        role_opportunity["demand_score"] = role_opportunity["total_data"] / role_opportunity["total_data"].max() * 100
        role_opportunity["salary_score"] = role_opportunity["median_salary"] / role_opportunity["median_salary"].max() * 100
        role_opportunity["remote_score"] = role_opportunity["remote_percentage"] / role_opportunity["remote_percentage"].max() * 100
        role_opportunity["opportunity_score"] = (
            demand_weight * role_opportunity["demand_score"]
            + salary_weight * role_opportunity["salary_score"]
            + remote_weight * role_opportunity["remote_score"]
        )
        role_opportunity = role_opportunity.round(2).sort_values("opportunity_score", ascending=False)

        left, right = st.columns(2)

        with left:
            fig = make_horizontal_bar(
                role_opportunity.sort_values("opportunity_score"),
                x="opportunity_score",
                y="role_group",
                title="Ranking Opportunity Score",
                text="opportunity_score"
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.scatter(
                role_opportunity,
                x="total_data",
                y="median_salary",
                size="remote_percentage",
                text="role_group",
                hover_name="role_group",
                title="Demand vs salary, ukuran bubble = remote",
                color="role_group",
                color_discrete_sequence=COLOR_SEQUENCE,
                template="plotly_white"
            )
            fig.update_traces(textposition="top center")
            fig.update_layout(height=450, title_x=0.02, xaxis_title="Jumlah data role", yaxis_title="Median salary USD", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(role_opportunity, use_container_width=True)

        top = role_opportunity.iloc[0]
        section_insight(
            f"<b>Role teratas:</b> {top['role_group']} dengan Opportunity Score <b>{top['opportunity_score']:.2f}</b>. "
            f"Median salary: <b>{format_usd(top['median_salary'])}</b>, fully remote: <b>{top['remote_percentage']:.2f}%</b>."
        )

        st.markdown(
            """
            **Cara membaca skor:**
            - Demand tinggi berarti role sering muncul dalam dataset.
            - Salary tinggi berarti potensi kompensasi lebih besar.
            - Remote tinggi berarti peluang kerja fleksibel lebih besar.
            - Data Analyst cocok sebagai jalur awal, lalu bisa berkembang ke Data Scientist, Data Engineer, Analytics Engineer, atau Data Architect.
            """
        )


# ============================================================
# Footer
# ============================================================

st.divider()
st.caption("Created by Muh. Shafwan Faiq R. | Data Science portfolio project")
