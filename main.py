# Importing necessary libraries

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from google import genai



# Loading environment variables from .env file

load_dotenv()

#DUMMYJSON_API_KEY = os.getenv("DUMMYJSON_API_KEY")           --- keeping this line commented out as the dummy API does not require authentication.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError(
        "GEMINI_API_KEY not found, please check your .env file."
    )



#Extracting data from API and Pagination logic to retrieve all records

base_url = "https://dummyjson.com/carts"

headers = {
    #"Authorization": f"Bearer {dummyjson_API_Key}",          --- Keeping this line commented out as the dummy API does not require authentication.
    "Accept": "application/json"
}


all_carts = []

skip = 0
limit = 20

print("Fetching transaction data from API")


while True:
    url = f"{base_url}?limit={limit}&skip={skip}"

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    carts = data["carts"]

    if len(carts) == 0:
        break

    all_carts.extend(carts)
    skip += limit

print(f"Total carts fetched: {len(all_carts)}")



# flattening the json data and creating a DataFrame

rows = []

for cart in all_carts:
    for product in cart["products"]:
        rows.append({
            "cart_id": cart["id"],
            "user_id": cart["userId"],
            "product_id": product["id"],
            "product_name": product["title"],
            "quantity": product["quantity"],
            "price": product["price"],
            "total": product["total"]
        })



# creating a DataFrame from the flattened data

df = pd.DataFrame(rows)

print("\nSample Data:")
print(df.head())



# Creating data quality checks and validation rules for the DataFrame

df = df.drop_duplicates()
df = df.dropna()
df["quantity"] = pd.to_numeric(df["quantity"])
df["price"] = pd.to_numeric(df["price"])
df["total"] = pd.to_numeric(df["total"])



# Saving the cleaned DataFrame to a CSV file

df.to_csv("data/clean_transactions.csv", index=False)

print("\nClean data saved successfully.")



# Creating business insights

summary = {
    "total_orders": int(df["cart_id"].nunique()),
    "total_customers": int(df["user_id"].nunique()),
    "total_revenue": round(float(df["total"].sum()), 2),
    "average_order_value": round(float(df.groupby("cart_id")["total"].sum().mean()), 2),
    "top_products": df.groupby("product_name")["total"].sum().sort_values(ascending=False).head(5).to_dict()
}

print("\nBusiness Summary:")
print(summary)



# Gemini API integration for generating a business report

client = genai.Client(
    api_key=GEMINI_API_KEY
)

prompt = f"""
You are a Retail Data Analyst.

Analyze the following transaction summary.

Metrics:
{summary}

Provide:
1. Executive Summary
2. Key Insights
3. Product Trends
4. Revenue Analysis
5. Business Recommendations

Use simple business language.
"""

print("\nGenerating Gemini Report")

response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
report = response.text



# Saving the generated report to a text file

with open(
    "reports/retail_summary_report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(report)


print("\nGemini Report Generated Successfully.")
print(report)
