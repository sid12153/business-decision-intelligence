## Dataset: Online Retail II

**Source:** UCI Machine Learning Repository  
**Link:** https://archive.ics.uci.edu/dataset/502/online+retail+ii

### Time Period
- Transactions from December 2009 to December 2011

### What each row represents
Each row represents a single product-level transaction within a customer invoice. An invoice may contain multiple rows if a customer purchased multiple products in a single order.

### Key Columns
- InvoiceNo: Unique identifier for each customer order
- StockCode: Product identifier
- Description: Product description
- Quantity: Number of units purchased
- InvoiceDate: Date and time of the transaction
- UnitPrice: Price per unit of the product
- CustomerID: Unique customer identifier
- Country: Country where the customer is located

### Why this dataset was chosen
- Real-world transactional data from an e-commerce business
- Suitable for core business KPI calculations such as revenue, order volume, and average order value
- Enables customer-level analysis, segmentation, and retention proxies
- Contains time-series data appropriate for trend analysis and forecasting
- Commonly used for business analytics and BI case studies

### Intended usage in this project
- Build Excel-style KPI calculations for business performance tracking
- Analyze trends, seasonality, and growth over time
- Perform customer and segment-level analysis
- Train simple, interpretable models for forecasting or risk identification
- Generate stakeholder-ready Excel reports and written insights
