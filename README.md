# azure-forecast-system
Predicting Azure Compute Storage demand to optimize capacity provisioning.

📌 Project Overview: 
This project focuses on building a predictive system to accurately forecast Azure Compute and Storage demand across multiple regions. The primary objective is to support the Azure Supply Chain team in making informed capacity provisioning decisions, thereby reducing both over-investment (excess idle capacity) and under-investment (service performance risks) in infrastructure.The solution leverages advanced data science techniques, structured feature engineering, and machine learning methodologies using Azure-based analytical tools to enhance forecasting accuracy and operational efficiency.

📘 Week 1 – Milestone 1: 
Milestone 1 establishes the foundation by collecting, integrating, cleaning, and validating a realistic cloud dataset.

🎯 Milestone 1 Objectives: 
Collect Azure Compute and Storage usage data with regional and seasonal dimensions
Source relevant external variables (economic indicators & market demand trends)
Clean and validate datasets to ensure consistency and reliability

📊 Dataset Description: 
⏳ Time Range: 2 Years (Daily Data)
🌍 Regions: us-east, us-west, india-south and india-west
🖥 Service Categories: compute, storage
🧾 Final Dataset Schema
Column Name             	  Description
timestamp               	  Daily observation date
region_name             	  Azure region
service_category	          Service type (compute/storage)
actual_usage	              Observed service consumption (target variable)
allocated_capacity	        Provisioned infrastructure capacity
operational_cost	          Incurred operational cost
availability_ratio	        Service availability/uptime score
net_customer_change	        Net customers added or lost
is_weekend	                Weekend indicator (0/1)
business_confidence_index	  Macro-economic indicator
cloud_adoption_index	      Market cloud growth trend

🧹 Data Cleaning & Validation Performed:
 Converted timestamps to datetime format
 Handled missing values using forward fill, median fill, and interpolation
 Removed duplicate records
 Standardized categorical formats
 Validated numeric ranges
 Verified capacity utilization consistency
 Sorted dataset chronologically

 🛠 Technologies Used: Python, Pandas, NumPy

🚀 Milestone 1 Outcome: 
  The dataset has been:
              Successfully collected and structured
              Integrated with external economic and market variables
              Cleaned and validated
              Prepared for feature engineering and modeling
