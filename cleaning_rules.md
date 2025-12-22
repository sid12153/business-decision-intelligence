# Data Cleaning Rules

This document describes the data cleaning and filtering decisions applied to the Online Retail II dataset prior to KPI calculation and modeling. All rules are based on exploratory analysis of the raw data.

---

## Invoice filtering (Cancellations)

**Rule**
- Remove all rows where the Invoice number starts with `"C"`.

**Rationale**
- Invoices prefixed with `"C"` represent cancelled transactions.
- These rows consistently contain negative quantities and do not represent completed sales.
- Including cancellations would distort revenue, order count, and customer activity KPIs.

---

## Quantity handling

**Rule**
- Remove all rows where `Quantity <= 0`.

**Rationale**
- Negative quantities represent product returns or cancellations.
- Zero quantities do not represent valid purchases.
- These values should not contribute to sales volume or revenue calculations.

---

## Price handling

**Rule**
- Remove all rows where `Price <= 0`.

**Rationale**
- Zero or negative prices were observed in the dataset.
- Such rows do not represent valid revenue-generating transactions and often coincide with missing product descriptions or customer identifiers.
- Revenue calculations require strictly positive unit prices.

---

## Customer ID handling

**Rule**
- Remove all rows with missing `Customer ID`.

**Rationale**
- Approximately 20% of rows are missing customer identifiers.
- Customer-level analysis, segmentation, and retention proxies require a valid customer ID.
- Retaining these rows would prevent accurate customer-based KPIs.

---

## Description handling

**Rule**
- Rows with missing `Description` values are removed indirectly through price and quantity filters.
- No additional imputation is applied to product descriptions.

**Rationale**
- Missing descriptions frequently occur alongside zero prices or invalid quantities.
- Product description is not required for KPI calculations once invalid transactions are removed.

---

## Date handling

**Rule**
- Parse `InvoiceDate` as a datetime field.
- Aggregate transactions at a monthly level for KPI reporting and trend analysis.

**Rationale**
- All invoice dates successfully parse as valid timestamps.
- Monthly aggregation aligns with common business reporting practices and reduces noise from intra-day variation.

---

## Country handling

**Rule**
- No country-level cleaning or filtering is applied.

**Rationale**
- Country values appear consistent and valid.
- Rare countries are retained to preserve full geographic coverage.
- Country-level aggregation may be applied during analysis but does not require cleaning.

---

## Scope decisions

- Analysis focuses exclusively on completed, revenue-generating transactions.
- No currency conversion is applied, as all transactions are recorded in a single currency.
- The cleaned dataset serves as the single source of truth for all downstream KPIs, models, and reports.

## Duplicate rows (multi-sheet merge)

**Rule**
- Drop exact full-row duplicates after combining sheets.

**Rationale**
- Online Retail II is provided across multiple sheets and contains repeated identical rows after merging.
- Only exact duplicates are removed to avoid accidentally dropping legitimate repeated purchases that may share the same invoice and product keys.

