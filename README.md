<h1 align="center">Cloud Service Demand Forecasting</h1>

<p align="center">
Milestone 1 & Milestone 2 – Data Preparation & Feature Engineering
</p>

<hr>

<h2>📌 Project Overview</h2>

<p>
This project focuses on forecasting cloud service demand using structured time-series data.
The objective is to transform raw cloud operational data into a model-ready dataset
through cleaning, feature engineering, and structured data wrangling.
</p>

<hr>

<!-- ===================== MILESTONE 1 ===================== -->

<h1>🚀 Milestone 1 (Weeks 1–2)</h1>

<h2>📅 Week 1 – Data Collection & Understanding</h2>

<h3>🎯 Objective</h3>
<p>
Understand the dataset structure, validate business metrics,
and perform initial preprocessing.
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
<li>Prepared clean baseline dataset</li>
</ul>

<hr>

<h2>📅 Week 2 – Feature Engineering & Data Wrangling</h2>

<h3>🎯 Objective</h3>
<p>
Enhance predictive power of dataset by creating time-series and business-driven features.
</p>

<h3>🧠 Features Engineered</h3>

<h4>1️⃣ Time-Based Features</h4>
<ul>
<li>hour – Captures intraday patterns</li>
<li>day – Captures daily variation</li>
<li>weekday – Identifies weekday vs weekend behavior</li>
</ul>

<h4>2️⃣ Lag Features (Historical Memory)</h4>
<ul>
<li>lag_1_usage – Previous period usage</li>
<li>lag_7_usage – Weekly recurring usage pattern</li>
</ul>

<h4>3️⃣ Rolling Features</h4>
<ul>
<li>rolling_mean_3 – 3-period moving average</li>
</ul>

<h4>4️⃣ Business Indicator</h4>
<ul>
<li>usage_spike – Anomaly detection flag</li>
</ul>

<h4>5️⃣ Categorical Encoding</h4>
<ul>
<li>One-hot encoding for region and service</li>
<li>drop_first=True used to prevent multicollinearity</li>
</ul>

<h3>📊 Outcome of Milestone 1</h3>
<ul>
<li>Clean and structured dataset</li>
<li>Time-aware feature enrichment</li>
<li>Business-aligned indicators</li>
<li>Model-ready data schema</li>
</ul>

<hr>

<!-- ===================== MILESTONE 2 ===================== -->

<h1>🚀 Milestone 2 (Weeks 3–4)</h1>

<h2>📌 Module: Advanced Feature Engineering & Data Transformation</h2>

<h3>🎯 Objective</h3>
<p>
Prepare the dataset for machine learning modeling by enriching features
and ensuring consistent schema and granularity.
</p>

<h3>🛠 Tasks Completed</h3>

<h4>1️⃣ Demand-Driving Feature Identification</h4>
<ul>
<li>Analyzed usage trends across regions</li>
<li>Evaluated impact of service uptime (availability_ratio)</li>
<li>Assessed customer behavior patterns</li>
</ul>

<h4>2️⃣ Derived Feature Engineering</h4>
<ul>
<li>Seasonality flags (weekday/weekend indicators)</li>
<li>Usage spike detection</li>
<li>Lag variables for short-term and weekly memory</li>
<li>Rolling averages for trend smoothing</li>
</ul>

<h4>3️⃣ Data Reshaping & Wrangling</h4>
<ul>
<li>Grouped calculations by region and service</li>
<li>Ensured chronological ordering before lag creation</li>
<li>Maintained consistent schema across transformations</li>
<li>Prepared final structured dataset for modeling</li>
</ul>

<h3>📊 Outcome of Milestone 2</h3>
<ul>
<li>Fully enriched time-series dataset</li>
<li>Model-ready feature matrix</li>
<li>Improved predictive capability through engineered features</li>
<li>Scalable structure for ML pipelines</li>
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

<hr>

<p align="center">
Cloud Analytics Project – Milestone 1 & 2
</p>
