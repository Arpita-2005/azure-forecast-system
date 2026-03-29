<h1 align="center">Azure Based Demand Forecasting & Capacity Optimization System </h1>

<p align="center">
Data Analytics Project – Time Series Demand Modeling
</p>

<hr>

<h2>📌 Project Overview</h2>

<p>
This project focuses on forecasting cloud service demand using structured time-series data.
The objective is to transform raw operational data into a model-ready dataset
through systematic preprocessing, feature engineering, and machine learning.
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

<!-- ===================== MILESTONE 3 ===================== -->

<h1>🚀 Milestone 3 – Week 5 & Week 6</h1>

<h2>📅 Module: Machine Learning Model Development</h2>

<h3>🎯 Objective</h3>
<p>
Build, evaluate, and optimize machine learning models to accurately forecast
cloud service demand using historical usage data.
</p>

<h3>🤖 Models Implemented</h3>

<h4>1️⃣ ARIMA (Time Series Model)</h4>
<ul>
<li>Captured trend and seasonality in usage data</li>
<li>Used as a baseline forecasting model</li>
<li>Hyperparameter tuning performed</li>
</ul>

<h4>2️⃣ XGBoost (Machine Learning Model)</h4>
<ul>
<li>Handled non-linear relationships and feature interactions</li>
<li>Utilized engineered features like lag variables and rolling mean</li>
<li>Hyperparameter tuning performed using GridSearchCV</li>
</ul>

<h4>3️⃣ Hybrid Model (ARIMA + XGBoost)</h4>
<ul>
<li>ARIMA used for trend prediction</li>
<li>XGBoost trained on residual errors</li>
<li>Combined predictions for improved accuracy</li>
<li><b>Observation:</b> Hybrid model did not improve performance and produced unstable results</li>
</ul>

<h3>📊 Model Selection</h3>
<ul>
<li>Compared ARIMA, XGBoost, and Hybrid model</li>
<li>XGBoost achieved the lowest RMSE and MAE</li>
<li><b>Final Model Selected: XGBoost</b></li>
</ul>

<h3>📊 Evaluation Metrics</h3>
<ul>
<li>RMSE (Root Mean Squared Error)</li>
<li>MAE (Mean Absolute Error)</li>
<li>Forecast Bias</li>
</ul>

<h3>📊 Outcome of Milestone 3</h3>
<ul>
<li>Multiple models developed and evaluated</li>
<li>Hybrid approach explored but not effective</li>
<li>XGBoost finalized as best-performing model</li>
<li>Model ready for deployment</li>
</ul>

<hr>

<!-- ===================== MILESTONE 4 ===================== -->

<h1>🚀 Milestone 4 – Week 7 & Week 8</h1>

<h2>📅 Module: Forecast Integration & Visualization</h2>

<h3>🎯 Objective</h3>
<p>
Deploy the trained model and build an interactive dashboard to visualize
cloud demand forecasts and support decision-making.
</p>

<h3>🛠 Key Components</h3>

<h4>1️⃣ Model Deployment (Streamlit)</h4>
<ul>
<li>Trained XGBoost model saved and loaded</li>
<li>Built interactive web app using Streamlit</li>
<li>Enabled real-time predictions via user input</li>
</ul>

<h4>2️⃣ Dashboard Visualization</h4>
<ul>
<li>Displayed actual vs predicted demand</li>
<li>Visualized trends and patterns</li>
<li>Improved interpretability of predictions</li>
</ul>

<h4>3️⃣ Deployment Links</h4>
<ul>
<li><b>Local URL:</b> http://localhost:8502</li>
<li><b>Network URL:</b> http://192.168.31.59:8502</li>
</ul>

<h3>📊 Outcome of Milestone 4</h3>
<ul>
<li>Interactive ML application deployed</li>
<li>Real-time prediction system created</li>
<li>End-to-end pipeline completed</li>
<li>User-friendly visualization for decision-making</li>
</ul>

<hr>

<h2>🧰 Tech Stack</h2>

<ul>
<li>Python</li>
<li>Pandas</li>
<li>NumPy</li>
<li>Matplotlib</li>
<li>XGBoost</li>
<li>Streamlit</li>
<li>Statsmodels (ARIMA)</li>
<li>Scikit-learn</li>
</ul>

<hr>

<h2>📁 Repository Structure</h2>

<hr>

<p align="center">
Cloud Analytics Learning Project
</p>
