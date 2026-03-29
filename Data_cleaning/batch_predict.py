import pandas as pd
import joblib
import json

# Load model
model = joblib.load("final_xgboost_model.pkl")

# Load column structure
with open("model_columns.json", "r") as f:
    model_columns = json.load(f)

# Load new data
df = pd.read_csv("data/new_data.csv")

# ✅ KEEP timestamp & actual before processing
timestamp = df["timestamp"]

if "actual_usage" in df.columns:
    actual = df["actual_usage"]
else:
    actual = None

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Create time features
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["day"] = df["timestamp"].dt.day

# Drop timestamp for model input only
df_model = df.drop("timestamp", axis=1)

# One-hot encoding
df_model = pd.get_dummies(df_model)

# Align columns
for col in model_columns:
    if col not in df_model:
        df_model[col] = 0

df_model = df_model[model_columns]

# Predict
predictions = model.predict(df_model)

# ✅ ADD RESULTS BACK
df["forecast"] = predictions
df["timestamp"] = timestamp

if actual is not None:
    df["actual_usage"] = actual

# Save output
df = df[[
    "timestamp",
    "region_name",
    "service_category",
    "actual_usage",
    "forecast",
    "allocated_capacity",
    "operational_cost",
    "availability_ratio",
    "net_customer_change",
    "is_weekend",
    "business_confidence_index",
    "cloud_adoption_index",
    "year",
    "month",
    "day"
]]

df.to_csv("forecast_output.csv", index=False)

print("✅ Batch prediction completed successfully")
