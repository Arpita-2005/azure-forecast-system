<h1 align="center">Azure Cloud Service Demand Forecasting</h1>

<p align="center">
Data Analytics Project – Time Series Demand Modeling
</p>

<hr>

<h2>📌 Project Overview</h2>

<p>
This project focuses on forecasting cloud service demand using structured time-series data.
The objective is to transform raw operational data into a model-ready dataset
through systematic preprocessing and feature engineering.
</p>

<hr>

<!-- ===================== MILESTONE 1 ===================== -->

<h1>🚀 Milestone 1 – Week 1 & Week 2</h1>

<h2>📅 Module: Data Collection & Understanding</h2>

<h3>🎯 Objective</h3>
<p>
Understand the dataset structure, validate business metrics,
clean inconsistencies, and prepare a structured baseline dataset.
</p>

<h3>📂 Dataset Attributes</h3>
<ul>
<li><b>timestamp</b> – Date and time of observation</li>
<li><b>region_name</b> – Cloud deployment region</li>
<li><b>service_category</b> – Service type (compute/storage)</li>
<li><b>actual_usage</b> – Resource consumption units</li>
<li><b>availability_ratio</b> – Service uptime ratio (0–1)</li>
<li><b>net_customer_change</b> – Customer growth indicator</li>
<li><b>business_confidence_index</b> – Economic indicator (0–100)</li>
</ul>

<h3>🛠 Tasks Completed</h3>
<ul>
<li>Converted timestamp to datetime format</li>
<li>Handled missing values appropriately</li>
<li>Validated availability ratio within 0–1 range</li>
<li>Explored regional and service-based usage patterns</li>
<li>Ensured consistent data schema</li>
</ul>

<h3>📊 Outcome of Milestone 1</h3>
<ul>
<li>Clean and validated dataset</li>
<li>Structured time-series format</li>
<li>Business metrics verified</li>
<li>Baseline dataset ready for feature engineering</li>
</ul>

<hr>

<!-- ===================== MILESTONE 2 ===================== -->

<h1>🚀 Milestone 2 – Week 3 & Week 4</h1>

<h2>📅 Module: Feature Engineering & Data Wrangling</h2>

<h3>🎯 Objective</h3>
<p>
Enhance predictive capability by engineering time-series
and business-driven features to prepare data for modeling.
</p>

<h3>🧠 Features Engineered</h3>

<h4>1️⃣ Time-Based Features</h4>
<ul>
<li>hour – Captures intraday demand patterns</li>
<li>day – Captures daily variation</li>
<li>weekday – Identifies weekday vs weekend trends</li>
</ul>

<h4>2️⃣ Lag Features (Historical Memory)</h4>
<ul>
<li>lag_1_usage – Previous time-period usage</li>
<li>lag_7_usage – Weekly recurring pattern</li>
</ul>

<h4>3️⃣ Rolling Features</h4>
<ul>
<li>rolling_mean_3 – 3-period moving average for trend smoothing</li>
</ul>

<h4>4️⃣ Business & Anomaly Indicators</h4>
<ul>
<li>customer_growth_flag – Binary indicator of customer increase</li>
<li>usage_spike – Flag for unusually high demand</li>
</ul>

<h4>5️⃣ Categorical Encoding</h4>
<ul>
<li>One-hot encoding for region and service category</li>
<li>Used drop_first=True to prevent multicollinearity</li>
</ul>

<h3>📊 Outcome of Milestone 2</h3>
<ul>
<li>Time-aware enriched dataset</li>
<li>Historical memory captured via lag features</li>
<li>Business-aligned indicators added</li>
<li>Fully model-ready structured dataset</li>
</ul>

<hr>

<h2>🧰 Tech Stack</h2>

<ul>
<li>Python</li>
<li>Pandas</li>
<li>NumPy</li>
<li>Jupyter Notebook</li>
</ul>

<hr>

<h2>📁 Repository Structure</h2>

<hr>

<p align="center">
Cloud Analytics Learning Project
</p>
