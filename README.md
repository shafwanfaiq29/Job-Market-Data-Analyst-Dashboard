# Data Analyst Job Market Dashboard

An end-to-end data analysis project that explores the Data Analyst and Data Science job market using salary data, job posting skill data, and an interactive Streamlit dashboard.

This project analyzes role demand, salary patterns, experience level impact, remote work trends, country-based compensation, required skills, and career opportunity score. The goal is to provide clear and practical insights for students, beginners, and aspiring data professionals who want to understand the data job market more effectively.

---

## Project Overview

The Data Science and Data Analytics job market includes many different roles such as Data Analyst, Data Scientist, Data Engineer, Machine Learning Engineer, and other related positions. For students and beginners, it can be difficult to understand which role to target, what skills to learn, and what factors affect salary.

This project was created to answer questions such as:

- What data roles appear most frequently?
- How does Data Analyst salary compare with other data roles?
- How does experience level affect salary?
- Do fully remote jobs show higher compensation?
- Which countries offer the highest compensation?
- What skills are most required for Data Analyst roles?
- Which roles have the strongest career opportunity based on demand, salary, and remote availability?

The analysis was first conducted in Google Colab using Python, then the results were transformed into an interactive Streamlit dashboard for easier presentation and exploration.

---

## Live Dashboard

Add your deployed Streamlit link here:

```text
https://your-streamlit-app-link.streamlit.app/
```

---

## Repository

```text
https://github.com/your-username/job-market-data-analyst-dashboard
```

---

## Dataset

This project uses two main datasets.

### 1. Data Science Job Salaries Dataset

This dataset is used for salary and job market analysis.

Main columns used:

```text
work_year
experience_level
employment_type
job_title
salary
salary_currency
salary_in_usd
employee_residence
remote_ratio
company_location
company_size
```

Dataset size after preprocessing:

```text
607 records
No missing values
```

Additional columns were created during preprocessing:

```text
experience_label
employment_label
remote_label
company_size_label
role_group
company_country
employee_country
```

---

### 2. Data Jobs Dataset by Luke Barousse

This dataset is used for skill analysis from job postings.

Main columns used:

```text
job_title_short
job_title
job_location
job_work_from_home
job_country
salary_year_avg
company_name
job_skills
job_type_skills
```

Dataset summary:

```text
785,741 total job postings
668,704 job postings with skill data
252 unique skills
```

This dataset was used to answer the question:

```text
What skills are most required by companies?
```

---

## Analysis Workflow

The project analysis was conducted in Google Colab through the following steps.

### 1. Data Loading

The salary dataset was loaded using Pandas.

```python
import pandas as pd

df_salary = pd.read_csv("ds_salaries.csv")
```

The job posting skill dataset was loaded from Hugging Face.

```python
from datasets import load_dataset

ds = load_dataset("lukebarousse/data_jobs")
df_jobs = ds["train"].to_pandas()
```

---

### 2. Data Understanding

Initial exploration included:

- Checking dataset shape
- Checking column names
- Checking data types
- Checking missing values
- Checking unique values
- Previewing sample records
- Identifying important columns for analysis

Key findings:

```text
Salary dataset:
- 607 rows
- No missing values

Skill dataset:
- 785,741 job postings
- 668,704 job postings with skill data
- 252 unique skills
```

---

### 3. Data Cleaning and Preprocessing

For the salary dataset:

- Removed unnecessary index column
- Converted coded values into readable labels
- Created role groups from job titles
- Mapped country codes into readable country names
- Created labels for experience level, employment type, remote type, and company size

Experience level mapping:

```text
EN = Entry Level
MI = Mid Level
SE = Senior Level
EX = Executive Level
```

Remote work mapping:

```text
0 = On-site
50 = Hybrid
100 = Fully Remote
```

For the skill dataset:

- Cleaned the `job_skills` column
- Converted skill strings into Python lists
- Removed duplicate skills within the same job posting
- Exploded skill lists into individual rows
- Created a skill-level dataframe for analysis

Final skill format:

```text
One row = one skill mention in one job posting
```

---

## Main Questions

This project focuses on answering the following questions:

1. What roles appear most frequently in the data job market?
2. How does Data Analyst salary compare with other data roles?
3. How does experience level affect salary?
4. Do fully remote jobs show higher salary?
5. Which countries offer the highest compensation?
6. What skills are most required by companies?
7. What skills are most important for Data Analyst roles?
8. Which skills are associated with higher salary?
9. Which role has the best career opportunity score?

---

## Key Findings

### 1. Most Common Roles

Top job titles in the salary dataset:

| Job Title | Total |
|---|---:|
| Data Scientist | 143 |
| Data Engineer | 132 |
| Data Analyst | 97 |
| Machine Learning Engineer | 41 |
| Research Scientist | 16 |

After grouping similar roles:

| Role Group | Total | Percentage |
|---|---:|---:|
| Data Scientist | 175 | 28.83% |
| Data Engineer | 160 | 26.36% |
| Data Analyst | 119 | 19.60% |
| Machine Learning / AI | 75 | 12.36% |
| Data Science Management | 33 | 5.44% |

Insight:

```text
Data Scientist, Data Engineer, and Data Analyst are the three most dominant role groups in the dataset. Data Analyst represents 19.60% of the salary dataset, making it a strong role to analyze as a career entry point.
```

---

### 2. Salary Comparison by Role

Median salary by role group:

| Role Group | Median Salary |
|---|---:|
| Data Architect | $180,000 |
| Data Science Management | $141,846 |
| Analytics / BI | $120,000 |
| Data Engineer | $107,400 |
| Data Scientist | $104,890 |
| Data Analyst | $90,320 |
| Machine Learning / AI | $87,425 |
| Other Data Role | $70,000 |

Insight:

```text
Data Analyst has a median salary of $90,320. It is lower than Data Engineer and Data Scientist, but still competitive and suitable as an entry point into the data field.
```

Important note:

```text
Data Architect has the highest median salary, but the sample size is only 11 records. Therefore, the result should be interpreted carefully.
```

---

### 3. Experience Level Impact on Salary

Median salary by experience level:

| Experience Level | Median Salary |
|---|---:|
| Entry Level | $56,500 |
| Mid Level | $76,940 |
| Senior Level | $135,500 |
| Executive Level | $171,438 |

Salary increase between levels:

| Transition | Increase |
|---|---:|
| Entry Level to Mid Level | 36.18% |
| Mid Level to Senior Level | 76.11% |
| Senior Level to Executive Level | 26.52% |

Insight:

```text
Experience level has a strong impact on salary. The biggest salary increase happens from Mid Level to Senior Level, with a 76.11% increase in median salary.
```

For Data Analyst roles:

| Experience Level | Median Salary |
|---|---:|
| Entry Level | $59,102 |
| Mid Level | $65,438 |
| Senior Level | $111,912 |
| Executive Level | $130,000 |

Important note:

```text
Executive Level Data Analyst only has 3 records, so the result should be interpreted carefully.
```

---

### 4. Remote Work and Salary

Median salary by work type:

| Work Type | Median Salary |
|---|---:|
| On-site | $99,000 |
| Hybrid | $69,999 |
| Fully Remote | $115,000 |

For Data Analyst roles:

| Work Type | Median Salary |
|---|---:|
| On-site | $81,666 |
| Hybrid | $55,000 |
| Fully Remote | $99,050 |

Insight:

```text
Fully Remote roles show the highest median salary both overall and specifically for Data Analyst roles.
```

Important note:

```text
This should not be interpreted as remote work alone causing higher salary. Experience level, company location, and role composition may also influence compensation.
```

---

### 5. Country Compensation Analysis

Countries with the highest median salary, using a minimum of 5 records:

| Company Country | Total Data | Median Salary |
|---|---:|---:|
| United States | 355 | $135,000 |
| Canada | 30 | $81,896 |
| United Kingdom | 47 | $78,526 |
| Germany | 28 | $78,015 |
| Japan | 6 | $75,682 |
| France | 15 | $56,738 |
| Greece | 11 | $49,461 |
| Spain | 14 | $48,372 |
| India | 24 | $22,124 |

For Data Analyst roles:

| Company Country | Total Data | Median Salary |
|---|---:|---:|
| United States | 83 | $105,000 |
| Canada | 11 | $71,786 |
| United Kingdom | 6 | $51,935 |
| Greece | 3 | $32,974 |
| Spain | 3 | $32,974 |
| India | 4 | $12,257 |

Insight:

```text
The United States dominates the dataset in both job count and compensation. It has the highest median salary overall and also the highest median salary for Data Analyst roles.
```

Important note:

```text
The country analysis should be interpreted carefully because the dataset is heavily dominated by United States records.
```

---

## Skill Analysis

### 1. Most Required Skills Overall

Top skills across all data-related job postings:

| Skill | Total Mentions | Percentage |
|---|---:|---:|
| SQL | 384,849 | 57.55% |
| Python | 380,909 | 56.96% |
| AWS | 145,381 | 21.74% |
| Azure | 132,527 | 19.82% |
| R | 130,892 | 19.57% |
| Tableau | 127,213 | 19.02% |
| Excel | 127,018 | 18.99% |
| Spark | 114,609 | 17.14% |
| Power BI | 98,147 | 14.68% |
| Java | 85,612 | 12.80% |

Insight:

```text
SQL and Python are the two most dominant skills in data-related job postings. Both appear in more than half of job postings that contain skill information.
```

---

### 2. Most Required Skills for Data Analyst

Top skills for Data Analyst roles:

| Skill | Total Mentions | Percentage |
|---|---:|---:|
| SQL | 92,428 | 57.99% |
| Excel | 66,860 | 41.95% |
| Python | 57,190 | 35.88% |
| Tableau | 46,455 | 29.14% |
| Power BI | 39,380 | 24.71% |
| R | 29,996 | 18.82% |
| SAS | 13,999 | 8.78% |
| PowerPoint | 13,822 | 8.67% |
| Word | 13,562 | 8.51% |
| SAP | 11,280 | 7.08% |

Insight:

```text
For Data Analyst roles, SQL, Excel, Python, Tableau, and Power BI are the most important core skills. These skills represent database querying, spreadsheet analysis, programming, and dashboard/reporting capability.
```

---

### 3. Skill Comparison Across Roles

Dominant skills by role:

| Role | Dominant Skills |
|---|---|
| Data Analyst | SQL, Excel, Python, Tableau, Power BI |
| Data Scientist | Python, SQL, R, Tableau, AWS |
| Data Engineer | SQL, Python, AWS, Azure, Spark |
| Machine Learning Engineer | Python, PyTorch, TensorFlow, AWS, SQL |

Insight:

```text
Data Analyst roles focus more on analytics and reporting tools, while Data Engineer and Machine Learning Engineer roles require more technical and infrastructure-related skills.
```

---

### 4. Remote Job Skill Analysis

Remote job postings represent:

```text
9.55% of job postings with skill data
```

Top skills for Work From Home roles:

| Skill | Percentage |
|---|---:|
| Python | 63.42% |
| SQL | 63.04% |
| AWS | 28.62% |
| Azure | 21.78% |
| Spark | 20.44% |
| Tableau | 18.62% |
| R | 16.74% |
| Excel | 14.63% |

Skills with higher presence in remote jobs compared to non-remote jobs:

| Skill | Remote | Non-Remote | Gap |
|---|---:|---:|---:|
| AWS | 28.62% | 21.01% | +7.61% |
| Python | 63.42% | 56.28% | +7.14% |
| SQL | 63.04% | 56.97% | +6.06% |
| Snowflake | 12.43% | 7.78% | +4.65% |
| Spark | 20.44% | 16.79% | +3.65% |

Insight:

```text
Remote jobs tend to emphasize technical skills such as Python, SQL, cloud platforms, and big data tools more strongly than non-remote jobs.
```

---

### 5. Skills Associated with Higher Salary

For all roles, several skills with high median salary include:

| Skill | Median Salary |
|---|---:|
| Mongo | $173,500 |
| Cassandra | $150,000 |
| Golang | $147,500 |
| Neo4j | $147,500 |
| Kafka | $147,500 |
| PyTorch | $147,500 |
| Scala | $147,500 |
| Airflow | $147,090 |
| TensorFlow | $145,000 |

For Data Analyst roles, skills with high median salary include:

| Skill | Median Salary |
|---|---:|
| Shell | $119,575 |
| Kafka | $115,095 |
| Linux | $112,150 |
| GCP | $111,175 |
| Scala | $111,175 |
| Spark | $111,175 |
| Hadoop | $111,175 |
| Airflow | $111,175 |
| Snowflake | $110,240 |
| Databricks | $110,000 |

Insight:

```text
The most frequently required skills are not always the highest-paying skills. For Data Analyst roles, core skills such as SQL, Excel, Python, Tableau, and Power BI are highly demanded, while technical skills such as Spark, Hadoop, GCP, Snowflake, Databricks, Airflow, and Kafka are associated with higher salary potential.
```

Important note:

```text
Salary-skill analysis only uses job postings that include salary information, so the result should be interpreted as an indication, not an absolute conclusion.
```

---

## Data Analyst Skill Recommendation

Based on demand and salary, Data Analyst skills were grouped into learning priorities.

### Required Core Skills

| Skill | Demand | Median Salary |
|---|---:|---:|
| SQL | 57.99% | $92,500 |
| Excel | 41.95% | $84,479 |
| Python | 35.88% | $98,500 |

---

### BI and Reporting Tools

| Skill | Demand | Median Salary |
|---|---:|---:|
| Tableau | 29.14% | $95,000 |
| Power BI | 24.71% | $90,000 |
| Looker | 3.93% | $104,000 |
| Qlik | 3.56% | $100,000 |

---

### Premium Skills

| Skill | Demand | Median Salary |
|---|---:|---:|
| Azure | 6.85% | $100,000 |
| AWS | 5.68% | $100,500 |
| Snowflake | 3.88% | $110,240 |
| Spark | 3.16% | $111,175 |
| Hadoop | 2.62% | $111,175 |
| BigQuery | 2.15% | $105,000 |
| GCP | 2.13% | $111,175 |
| Databricks | 1.98% | $110,000 |
| Airflow | 1.26% | $111,175 |
| Kafka | 0.75% | $115,095 |

Insight:

```text
SQL, Excel, and Python should be treated as core skills for Data Analyst. After that, Tableau and Power BI are important for dashboard and reporting. Premium skills such as cloud platforms, big data tools, and workflow tools can help increase career competitiveness.
```

---

## Opportunity Score

Opportunity Score was created to rank career opportunities based on three factors:

```text
Demand Score = number of role records
Salary Score = median salary
Remote Score = fully remote availability
```

Formula:

```text
Opportunity Score = 40% Demand Score + 40% Salary Score + 20% Remote Score
```

Opportunity Score ranking:

| Rank | Role Group | Opportunity Score | Median Salary | Remote Percentage |
|---:|---|---:|---:|---:|
| 1 | Data Scientist | 74.05 | $104,890 | 53.71% |
| 2 | Data Engineer | 73.94 | $107,400 | 67.50% |
| 3 | Data Architect | 62.51 | $180,000 | 100.00% |
| 4 | Data Analyst | 61.56 | $90,320 | 71.43% |
| 5 | Data Science Management | 50.58 | $141,846 | 57.58% |
| 6 | Machine Learning / AI | 47.50 | $87,425 | 54.67% |
| 7 | Analytics / BI | 44.67 | $120,000 | 70.59% |
| 8 | Other Data Role | 32.38 | $70,000 | 64.71% |

Insight:

```text
Data Scientist and Data Engineer have the highest Opportunity Scores because they combine strong demand, competitive salary, and remote availability. Data Analyst remains a strong career entry point because it has good demand and high remote availability, but its median salary is lower than Data Scientist and Data Engineer.
```

---

## Dashboard

The results of the analysis were transformed into an interactive Streamlit dashboard.

The dashboard includes:

- Executive summary
- Role demand analysis
- Salary comparison by role
- Data Analyst salary focus
- Experience level impact
- Remote work analysis
- Country compensation analysis
- Skill analysis
- Skill recommendation
- Opportunity Score
- Career recommendation

The dashboard was created to make the analysis easier to understand for general users, students, and aspiring data professionals.

---

## Project Output

This project produces several outputs:

### 1. Google Colab Analysis Notebook

Contains the full analysis process:

- Data loading
- Data understanding
- Data cleaning
- Exploratory data analysis
- Salary analysis
- Skill analysis
- Remote work analysis
- Opportunity Score
- Insight generation

### 2. Streamlit Dashboard

An interactive dashboard for presenting insights in a clean and readable format.

### 3. Static HTML Dashboard

A static version of the dashboard for easy sharing and presentation.

### 4. GitHub Repository

Contains source code, prepared datasets, documentation, and instructions to run the project.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical operations |
| Matplotlib | Visualization in Colab |
| Streamlit | Interactive dashboard |
| Hugging Face Datasets | Loading job posting dataset |
| Google Colab | Data analysis environment |
| GitHub | Version control and portfolio repository |

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

## How to Run Locally

Clone this repository:

```bash
git clone https://github.com/your-username/job-market-data-analyst-dashboard.git
cd job-market-data-analyst-dashboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

---

## Requirements

```text
streamlit
pandas
numpy
matplotlib
```

---

## Notes and Limitations

Several results should be interpreted carefully:

- The salary dataset contains 607 records, so some categories have limited sample sizes.
- Data Architect has the highest median salary, but only has 11 records.
- Executive Level Data Analyst only has 3 records.
- Salary-skill analysis only uses job postings that include salary information.
- Country analysis is heavily dominated by United States records.
- Remote salary differences should not be interpreted as direct causation because experience level, company location, and role type may also influence salary.

---

## Final Conclusion

Data Analyst is a strong entry point for students and beginners who want to start a career in the data field. The role has solid demand, good remote availability, and requires a practical combination of SQL, Excel, Python, Tableau, and Power BI.

However, to improve career competitiveness and salary potential, aspiring Data Analysts should not stop at core skills. Premium skills such as cloud platforms, big data tools, data warehouse tools, workflow orchestration tools, and data engineering fundamentals can provide additional value.

Overall, the analysis shows that:

- Data Analyst remains a relevant and realistic career path.
- Experience level strongly affects salary.
- Fully remote roles tend to show higher median salary in the dataset.
- The United States dominates compensation in the salary dataset.
- SQL and Python are the most dominant skills overall.
- SQL, Excel, Python, Tableau, and Power BI are core Data Analyst skills.
- Premium skills such as Snowflake, Spark, GCP, AWS, Azure, Databricks, Airflow, and Kafka are associated with higher salary potential.
- Data Scientist and Data Engineer have the highest Opportunity Scores.
- Data Analyst is a strong career entry point, especially for students in Data Science.

---

## Author

Created by **Muh. Shafwan Faiq R.**

This project was developed as a Data Science learning project and explore real-world job market trends through data analysis and dashboard development.
