# API_Integration

This project demonstrates a simple Engineering pipeline using Python, REST APIs, Pandas, and Google's Gemini AI.

The pipeline extracts retail transaction data from the DummyJSON API, handles pagination to retrieve all available records, and transforms nested JSON data into a structured tabular format. The data is then cleaned using data quality checks such as duplicate removal, null value handling, and data type validation.

After processing the data, key business metrics including total orders, total customers, average cart value, and popular products are generated. These metrics are sent to the Gemini API, which automatically creates a business insight report with recommendations and observations.

Key Concepts
- REST API Integration using Python Requests
- API Headers and Request Handling
- Pagination using limit and skip parameters
- JSON Data Extraction and Flattening
- Data Cleaning and Validation with Pandas
- Business KPI Generation
- Gemini AI Integration
- Automated Report Generation

Pipeline Flow

- Transaction API → Data Extraction → Data Cleaning → KPI Generation → Gemini AI → Business Report

Output Files
- clean_transactions.csv – Processed transaction dataset
- retail_summary_report.txt – AI-generated business insights report
