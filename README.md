# 🛡️ Global Cyber Threat Intelligence Dashboard (2015–2024)

An end-to-end **data analytics & visualization project** focused on exploring global cybersecurity incidents from 2015 to 2024.  
This project demonstrates **data preprocessing, exploratory data analysis (EDA), dashboard development, and iterative design thinking**, with an optional machine learning extension.

---

## 📌 Project Overview

Cybersecurity incidents have become increasingly frequent and costly across industries and countries. This project analyzes a global cybersecurity threats dataset to:

- Understand **attack patterns and trends over time**
- Identify **most affected countries and industries**
- Analyze **financial impact of cyber incidents**
- Build an **interactive dashboard** for threat intelligence exploration
- Demonstrate **iterative improvement** through multiple dashboard versions

The project is intentionally structured as a **portfolio-ready analytics workflow**, emphasizing both **technical foundations** and **analyst-friendly usability**.

---

## 📊 Dataset

- **Source:** Kaggle – Global Cybersecurity Threats (2015–2024)
- **Records:** ~3,000 incidents
- **Key Attributes:**
  - Country  
  - Year  
  - Attack Type  
  - Target Industry  
  - Financial Loss (in Million $)  
  - Number of Affected Users  
  - Attack Source  
  - Security Vulnerability Type  
  - Defense Mechanism Used  
  - Incident Resolution Time (Hours)  

The dataset was cleaned and standardized before analysis to ensure consistency across visualizations.

---

## 🔁 Project Evolution: From v1 to v2

This project evolved through **two intentional dashboard iterations**, each serving a distinct purpose.

---

### 🔹 Version 1 – Foundation & Capabilities

**Focus:** Architecture-first, system-oriented design

Version 1 was built to establish a strong analytical and technical foundation. The primary goal was to explore how a cybersecurity dashboard could be structured as a scalable analytics system.

Key characteristics of v1:

- Structured data preprocessing pipeline
- Multiple analytical summary outputs
- Modular dashboard logic
- Initial integration of machine learning for severity prediction
- Emphasis on **technical breadth and capability demonstration**

This version serves as a **proof-of-concept**, showcasing how data engineering, analytics, and ML components can coexist in a single project.

---

### 🔹 Version 2 – Usability & Analytical Depth (Main Dashboard)

**Focus:** Analyst-first design, insight-driven exploration

Version 2 represents a refinement of the dashboard based on learnings from v1. The focus shifted from architectural complexity to **clarity, usability, and real-world analytical workflow**.

Key improvements in v2:

- Single, consistently filtered source of truth (`df_filtered`)
- Cleaner and more intuitive filter logic
- Stronger EDA-driven layout
- Clear KPI metrics for quick situational awareness
- Logical dashboard flow aligned with how analysts explore data
- Reduced cognitive load and improved readability

This version closely reflects how **cyber threat analysts or data analysts** would interact with real-world incident data.

> v2 is presented as the **primary dashboard** in this project.

---

## 📈 Dashboard Features (v2)

### 🔍 Interactive Filters

- Year range slider
- Country selection
- Industry selection
- Attack type selection

### 📌 Key Metrics

- Total incidents
- Countries affected
- Industries impacted
- Total financial loss

### 🌍 Visual Analysis

- Global incident distribution (choropleth map)
- Industry-wise threat distribution
- Attack type frequency
- Yearly incident trends
- Financial loss analysis by year and industry
- Top 10 countries and industries by incident count

### 📄 Data Transparency

- Filtered dataset preview for exploration and validation

---

## 🤖 Machine Learning (Optional Extension)

An optional extension explores **cyberattack severity prediction** using supervised machine learning.

- Feature encoding and preprocessing
- Severity classification model
- Integrated prediction workflow (separate from core EDA dashboard)

This component is kept modular to avoid overloading the main analytical dashboard.

---

## 🧠 Key Learnings

- The trade-off between **architectural complexity and analytical usability**
- Importance of a single, consistent data source in dashboards
- Designing dashboards around **how users think**, not just how data is structured
- Iterative refinement leads to significantly better insight delivery

---

## 🛠️ Tech Stack

- **Python**
- **Pandas** – data manipulation
- **Streamlit** – interactive dashboards
- **Plotly** – visualizations
- **Scikit-learn** – (optional) machine learning

---

## 🚀 How to Run

1. Clone the repository
2. Launch the main dashboard:

bash
streamlit run dashboards/v2_dashboard.py

## 📌 Final Notes

This project is intentionally presented as an **evolution**, not a single static solution. The goal is to demonstrate:

- Analytical thinking  
- Iterative improvement  
- Practical dashboard design  
- Real-world data exploration skills  
