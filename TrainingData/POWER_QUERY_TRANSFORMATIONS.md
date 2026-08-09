# Power Query Transformations Guide

## Coding-Forge | Cleaning Financial Data in Power BI

---

## Introduction

Real-world data from Dynamics 365 and Dataverse exports is never clean. This guide walks you through fixing common data quality issues using **only the Power Query Editor ribbon buttons** — no code required.

---

## How to Open Power Query Editor

1. In Power BI Desktop, go to **Home** > **Transform Data**
2. The Power Query Editor window opens
3. Each table appears on the left under "Queries"
4. Your cleanup steps are recorded on the right panel under **Applied Steps**

> **Tip:** Turn on **Column Quality**, **Column Distribution**, and **Column Profile** from the **View** tab. These show data issues at a glance.

---

## File 1: Budget vs Actuals

### What's Wrong With This Data?

| Problem                          | What It Looks Like                                           |
| -------------------------------- | ------------------------------------------------------------ |
| Dollar signs in numbers          | `$150000`, `-$120000`                                        |
| Percentage signs                 | `6.0%`                                                       |
| Inconsistent capitalization      | `materials`, `travel`, `OVER BUDGET`, `at risk`              |
| Extra spaces                     | `" Cyber Defense Initiative"`                                |
| N/A text in number columns       | `N/A`                                                        |
| Footer/notes rows at the bottom  | `"Notes: Data exported from..."` + blank row + duplicate row |
| Shortened names                  | `"Satellite Comm Upgrade"` instead of full name              |
| Multiple fiscal years & quarters | FY2025 (Q1–Q4) and FY2026 (Q1–Q2)                            |

---

### How to Fix It

#### 1. Remove the footer/notes rows at the bottom

- **Home** > **Remove Rows** > **Remove Bottom Rows** > Type `3`
- *(This removes the blank row, notes row, and duplicate row at the bottom in one step)*

#### 2. Trim extra spaces from text

- Select all text columns (hold Ctrl and click: Program Name, Program ID, Cost Center, Budget Category, Funding Source, Status)
- **Transform** > **Format** > **Trim**

#### 3. Fix dollar signs and commas in amount columns

- Select `Budgeted Amount`, `Actual Amount`, and `Variance` columns (hold Ctrl to multi-select)
- **Transform** > **Replace Values** > Find: `$` Replace with: *(leave blank)* > OK
- **Transform** > **Replace Values** > Find: `,` Replace with: *(leave blank)* > OK

#### 4. Fix percentage signs

- Select `Variance %` column
- **Transform** > **Replace Values** > Find: `%` Replace with: *(leave blank)* > OK

#### 5. Fix N/A values

- Select `Actual Amount`, `Variance`, and `Variance %` columns
- **Transform** > **Replace Values** > Find: `N/A` Replace with: *(leave blank)* > OK

#### 6. Change columns to the right data type

- Click the "ABC" icon on `Budgeted Amount` column header > Select **Decimal Number**
- Click the "ABC" icon on `Actual Amount` column header > Select **Decimal Number**
- Click the "ABC" icon on `Variance` column header > Select **Decimal Number**
- Click the "ABC" icon on `Variance %` column header > Select **Decimal Number**

#### 7. Fix inconsistent capitalization in Budget Category

- Select `Budget Category` column
- **Transform** > **Format** > **Capitalize Each Word**

#### 8. Fix "Sub-Contracts" → "Subcontracts"

- Select `Budget Category` column
- **Transform** > **Replace Values** > Find: `Sub-Contracts` Replace with: `Subcontracts`

#### 9. Fix Status column consistency

- Select `Status` column
- **Transform** > **Format** > **Capitalize Each Word**

#### 10. Fix shortened program names

- Select `Program Name` column
- **Transform** > **Replace Values**:
  - Find: `Satellite Comm Upgrade` Replace with: `Satellite Communications Upgrade`
  - Find: `Next Gen Radar Systems` Replace with: `Next-Gen Radar Systems`

---

## File 2: Purchase Orders

### What's Wrong With This Data?

| Problem                              | What It Looks Like                                      |
| ------------------------------------ | ------------------------------------------------------- |
| Different date formats               | `10/15/2024`, `11-20-2024`, `2025-02-01`, `Feb 10 2025` |
| Dollar signs and commas              | `"$1,250,000.00"`                                       |
| NULL and dashes as values            | `NULL`, `-`                                             |
| Inconsistent status capitalization   | `CLOSED`, `closed`, `in progress`                       |
| Inconsistent priority capitalization | `CRITICAL`, `medium`, `high`                            |
| Extra spaces in names                | `"Triton Systems "`, `" James Mitchell"`                |
| Vendor name variations               | `"Apex Dynamics Corp"` vs `"Apex Dynamics Corp."`       |
| Duplicate row                        | PO-1006 appears twice                                   |
| Shortened program name               | `"Satellite Comm Upgrade"`                              |

---

### How to Fix It

#### 1. Remove duplicate rows

- Select the `PO ID` column > **Home** > **Remove Rows** > **Remove Duplicates**

#### 2. Trim spaces from all text columns

- Select all text columns > **Transform** > **Format** > **Trim**

#### 3. Clean the dollar amounts

- Select `PO Amount` column
- **Transform** > **Replace Values**: Find `$` Replace with blank
- **Transform** > **Replace Values**: Find `,` Replace with blank
- Repeat for `Amount Paid` and `Amount Remaining`

#### 4. Fix NULL and dash values

- Select `Amount Paid` column
- **Transform** > **Replace Values**: Find `NULL` Replace with `0`
- **Transform** > **Replace Values**: Find `-` Replace with `0`

#### 5. Change amount columns to Decimal Number type

- Click column type icon on `PO Amount` > **Decimal Number**
- Repeat for `Amount Paid` and `Amount Remaining`

#### 6. Fix date columns

- Select `Order Date` column > Click the type icon > Choose **Date**
  - Power BI will auto-detect most formats
  - If any rows show "Error", right-click the column > **Replace Errors** > enter `null`
- Repeat for `Delivery Date`

#### 7. Fix PO Status capitalization

- Select `PO Status` column
- **Transform** > **Format** > **Capitalize Each Word**

#### 8. Fix Priority capitalization

- Select `Priority` column
- **Transform** > **Format** > **Capitalize Each Word**

#### 9. Fix vendor name inconsistencies

- Select `Vendor Name` column
- **Transform** > **Replace Values**: Find `Apex Dynamics Corp.` Replace with `Apex Dynamics Corp`
- **Transform** > **Replace Values**: Find `Centurion Inc.` Replace with `Centurion Inc`

#### 10. Fix shortened program names

- Select `Program Name` column
- **Transform** > **Replace Values**: Find `Satellite Comm Upgrade` Replace with `Satellite Communications Upgrade`

---

## File 3: Programs (Dimension Table)

### What's Wrong With This Data?

Nothing! This is a clean lookup table with one row per program. It serves as the central dimension for the star schema.

### Steps

#### 1. Verify data types

- All columns should import as **Text** — no changes needed

#### 2. Rename the query

- Right-click the query name on the left > **Rename** > `Programs`

---

## Tips for the Exercises

### How to Know You're Done Cleaning

Use the **View** tab and enable:

- **Column Quality** — shows % valid, error, and empty per column
- **Column Distribution** — shows distinct/unique value counts
- **Column Profile** — shows statistics for the selected column

You want:

- 0% errors in all columns
- Number columns showing as numbers (not text)
- Consistent values (check Column Distribution — you shouldn't see `Closed` AND `closed`)

---

### Common Mistakes to Avoid

1. **Don't forget to click "Close & Apply"** when done — otherwise nothing saves
2. **Order matters** — Remove rows FIRST, then fix values (don't waste time cleaning rows you'll delete)
3. **Watch for partial matches** — When replacing text, make sure you don't accidentally create doubled words
4. **Check date conversions** — After changing to Date type, look for "Error" values that didn't convert

---

### Undo a Step

If you make a mistake:

- Look at **Applied Steps** on the right panel
- Click the **X** next to any step to delete it
- Steps below it will also be removed

---

## After Cleanup: Setting Up Relationships

Once all 3 tables are clean and loaded:

1. Go to **Model View** (left sidebar)
2. Drag `Program ID` from **Programs** to `Program ID` in **Budget vs Actuals**
3. Double-click the relationship line to open the dialog:
   - Cardinality: **One-to-Many**
   - Cross filter direction: **Single**
4. Drag `Program ID` from **Programs** to `Program ID` in **Purchase Orders**
5. Double-click the relationship line:
   - Cardinality: **One-to-Many**
   - Cross filter direction: **Single**

**Why Single?** In a star schema, filters flow from the dimension table (Programs) down to the fact tables. A slicer on Program Name will filter both Budget vs Actuals and Purchase Orders automatically. "Both" is generally not recommended — it can cause ambiguity and performance issues.

The Programs table is your **dimension table** (star schema center). Both Budget vs Actuals and Purchase Orders are fact tables that connect to it. This enables cross-filtering between all tables through the shared Program dimension.

---

*Next: See REPORT_BUILDING_GUIDE.md for how to build each report.*
