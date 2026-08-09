# Power BI - Financial Data Training Guide

## Coding-Forge

---

## Overview

This training uses sample financial data modeled after Dynamics 365 Finance & Operations and Dataverse table structures. Participants will learn to connect Power BI to Dataverse, build financial reports, and publish them securely within a GCC High environment.

---

## Prerequisites

- Power BI Desktop (GCC High version) installed
- Access to a Dynamics 365 Finance & Operations environment (or Dataverse sandbox)
- Appropriate security roles: **Finance Manager** or **Financial Analyst** in Dynamics 365
- Power BI Pro or Premium Per User license (GCC High tenant)

---

## Sample Data Files

The following CSV files are provided in the `Training Data/` folder for hands-on exercises:

| File                                     | Description                                          |
| ---------------------------------------- | ---------------------------------------------------- |
| `Financial Data - Programs.csv`          | Program dimension table (lookup/reference)           |
| `Financial Data - Budget vs Actuals.csv` | Program-level budget tracking with variance analysis |
| `Financial Data - Purchase Orders.csv`   | Procurement data with vendor and contract details    |

---

## Connecting to Dataverse from Power BI

### Method 1: Direct Dataverse Connector

1. Open Power BI Desktop
2. Select **Get Data** > **Dataverse**
3. Enter your environment URL: `https://yourorg.crm9.dynamics.com` (GCC High uses `.crm9`)
4. Authenticate with your organizational credentials
5. Select the required tables from the Navigator pane
6. Click **Transform Data** to open Power Query Editor

### Method 2: Dynamics 365 OData Feed

1. Select **Get Data** > **OData Feed**
2. Enter: `https://yourorg.crm9.dynamics.com/api/data/v9.2`
3. Select **Organizational Account** for authentication
4. Choose relevant entities

### Method 3: Import from CSV (Training Only)

1. Select **Get Data** > **Text/CSV**
2. Navigate to the `Training Data/` folder
3. Select the financial data CSV files
4. Review column types in the preview and click **Load**

---

## Data Model Relationships (Star Schema)

Set up the following relationships in Power BI Model View:

```
Programs[Program ID] (1) → Budget vs Actuals[Program ID] (Many)
Programs[Program ID] (1) → Purchase Orders[Program ID] (Many)
```

The **Programs** table acts as a dimension/lookup table with one row per program. Both fact tables (Budget vs Actuals and Purchase Orders) connect to it, enabling cross-filtering between budget data and procurement data through the shared dimension.

---

## Using Aggregations in Visuals (No Formulas Needed)

Power BI automatically calculates totals, averages, and counts when you drag fields into visuals. You do NOT need to write any formulas.

**How to change the aggregation on a field:**

1. Drag a number field (e.g., `Budgeted Amount`) into a visual
2. Click the dropdown arrow next to the field name in the **Values** area
3. Choose: Sum, Average, Count, Min, Max, etc.

**Common aggregations for this training data:**

| Visual Need           | Field to Use       | Aggregation |
| --------------------- | ------------------ | ----------- |
| Total Budget          | `Budgeted Amount`  | Sum         |
| Total Actual Spend    | `Actual Amount`    | Sum         |
| Total PO Value        | `PO Amount`        | Sum         |
| Number of POs         | `PO ID`            | Count       |
| Total Outstanding POs | `Amount Remaining` | Sum         |

> **Tip:** If Power BI shows "Count" when you expected "Sum", it means the column is still typed as Text. Go back to Power Query and change the data type to Decimal Number.

---

## Exercises

### Exercise 1: Load and Transform Data

1. Import all 3 CSV files into Power BI Desktop
2. In Power Query, clean the data following POWER_QUERY_TRANSFORMATIONS.md
3. Set appropriate data types (Currency, Percentage, Date)
4. Establish relationships between tables in Model View (Programs → Budget vs Actuals, Programs → Purchase Orders)

### Exercise 2: Build a Budget vs Actuals Dashboard

1. Create a clustered bar chart comparing Budget vs Actuals by Program
2. Add a KPI card showing total variance
3. Add conditional formatting (red for over-budget, green for on-track)
4. Add slicers for Fiscal Year and Quarter

### Exercise 3: Cross-Data Executive Summary

1. Create a Matrix with Programs as rows, Quarters as columns, showing Actual Amount
2. Add KPI Cards: Total Budget, Total Actual, Total PO Value, Total Outstanding
3. Build a line chart showing spending trend by Program across FY2025–FY2026
4. Add a Fiscal Year slicer to compare year-over-year performance

### Exercise 4: Publish to Power BI Service

1. Publish the report to a Power BI GCC High workspace
2. Set up a scheduled refresh connecting to Dataverse



## Troubleshooting

| Issue                         | Solution                                                                    |
| ----------------------------- | --------------------------------------------------------------------------- |
| "Cannot connect to Dataverse" | Verify GCC High URL uses `.crm9.dynamics.com`                               |
| Tables not visible            | Check Dataverse security role has Read access                               |
| Refresh fails in Service      | Configure gateway for on-premises data; use service principal for Dataverse |
| Slow query performance        | Use Import mode instead of DirectQuery for large datasets                   |
| Missing financial dimensions  | Map D365 financial dimension sets in Power Query                            |

---

## Additional Resources

- [Power BI for US Government Documentation](https://docs.microsoft.com/power-bi/admin/service-govus-overview)
- [Dataverse Connector for Power BI](https://docs.microsoft.com/power-apps/maker/data-platform/data-platform-powerbi-connector)
- [Dynamics 365 Finance Data Entities](https://docs.microsoft.com/dynamics365/fin-ops-core/dev-itpro/data-entities/data-entities)
- [GCC High Environment URLs](https://docs.microsoft.com/power-platform/admin/microsoft-dynamics-365-government)

---

*Prepared for Coding-Forge - Power BI for US DoD Training*
