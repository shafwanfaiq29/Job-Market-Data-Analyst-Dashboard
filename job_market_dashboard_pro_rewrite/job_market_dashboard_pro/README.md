# Data Analyst Job Market Dashboard

Interactive dashboard for analyzing Data Analyst and Data Science job market trends, salary patterns, remote work impact, country compensation, required skills, and career opportunity score.

This project is designed as a Data Science portfolio project. The dashboard is simple enough for general audiences, but still includes meaningful analytical insights for career decision-making.

---

## Project Goals

This project answers several questions:

- What data roles appear most often in the job market?
- How does Data Analyst salary compare with other data roles?
- How does experience level affect salary?
- Do fully remote jobs offer higher compensation?
- Which countries offer the highest compensation?
- What skills are most required for Data Analyst roles?
- Which role has the strongest career opportunity based on demand, salary, and remote availability?

---

## Dashboard Sections

### 1. Executive Summary
Shows the key findings in a simple and presentation-friendly format.

### 2. Role & Salary
Compares role demand and median salary across different data roles, including:

- Data Analyst
- Data Scientist
- Data Engineer
- Machine Learning / AI
- Data Architect
- Data Science Management

### 3. Data Analyst Focus
Focuses specifically on Data Analyst salary, remote work, country compensation, and recommended skills.

### 4. Skills
Shows the most required skills in data job postings and compares skill requirements across roles.

Main Data Analyst skills include:

- SQL
- Excel
- Python
- Tableau
- Power BI

Premium skills include:

- AWS
- Azure
- GCP
- Snowflake
- Spark
- Databricks
- Airflow
- Kafka

### 5. Country & Remote
Analyzes country-based compensation and the relationship between remote work, experience level, and salary.

### 6. Opportunity Score
Creates a career opportunity score using:

```text
Opportunity Score = Demand Score + Salary Score + Remote Score
```

The default weight is:

```text
40% Demand + 40% Salary + 20% Remote
```

Users can adjust the weights directly from the dashboard.

---

## Key Insights

- Data Scientist, Data Engineer, and Data Analyst are among the most common roles in the salary dataset.
- Data Analyst is a good entry point into the data field because it has strong demand and clear skill requirements.
- Experience level has a strong impact on salary.
- Fully remote jobs tend to have higher median salary, but this should be interpreted together with experience level and company location.
- The United States dominates the dataset in both job count and compensation.
- SQL, Excel, Python, Tableau, and Power BI are the most important skills for Data Analyst roles.
- Premium skills such as cloud platforms, Snowflake, Spark, Databricks, Airflow, and Kafka can increase career value.

---

## Tech Stack

- Python
- Pandas
- NumPy
- Plotly
- Streamlit

---

## Dataset

This project uses two kinds of data:

1. `ds_salaries.csv`  
   Used for salary, role, country, remote work, and opportunity score analysis.

2. Precomputed skill summary tables  
   Based on the `lukebarousse/data_jobs` dataset and used for skill analysis.

The skill tables are stored locally inside the `data/` folder so the dashboard can run faster and does not need to download a large dataset every time.

---

## Project Structure

```text
job-market-data-analyst-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    ├── ds_salaries.csv
    ├── skill_overall.csv
    ├── skill_data_analyst.csv
    ├── skill_role_matrix.csv
    ├── remote_skill_compare.csv
    └── skill_recommendation.csv
```

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/job-market-data-analyst-dashboard.git
cd job-market-data-analyst-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
streamlit run app.py
```

---

## Recommended Repository Description

```text
Interactive Data Analyst job market dashboard with salary analysis, required skills, remote work trends, country compensation, and career opportunity scoring.
```

---

## Recommended GitHub Topics

```text
data-science, data-analysis, data-analyst, job-market-analysis, salary-analysis, streamlit, plotly, pandas, data-visualization, career-analytics
```

---

## Author

Created by **Muh. Shafwan Faiq R.**

This project was developed as a Data Science learning project and portfolio project.
