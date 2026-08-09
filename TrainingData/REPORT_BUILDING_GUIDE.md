# Report Building Guide

## Coding-Forge

---

## Prerequisites

Before building reports, make sure you have:

- All 3 data files loaded and cleaned (see POWER_QUERY_TRANSFORMATIONS.md)
- Relationships set up in Model View: Programs → Budget vs Actuals, Programs → Purchase Orders (see INSTRUCTIONS.md)
- Power BI Desktop

---

## Report 1: Program Financial Health Dashboard

**Audience:** Program Managers, Finance Directors  
**Purpose:** Track budget vs. actual spend across all programs at a glance

### Page Setup

1. Go to **Report View** (left sidebar)
2. Right-click the page tab at the bottom > **Rename** > `Program Health`

### Visuals to Build

#### Visual 1: Clustered Bar Chart — Budget vs Actual by Program

1. Click on empty space on the canvas
2. From the **Visualizations** pane, click **Clustered Bar Chart**
3. Drag fields from the **Fields** pane:
   - **Y-axis**: `Budget vs Actuals` > `Program Name`
   - **X-axis**: `Budget vs Actuals` > `Budgeted Amount`
   - Also drag `Actual Amount` to **X-axis** (it will appear as a second bar)
4. Resize the visual to fill the top half of the page

**Formatting:**

- Click the visual > **Format** pane (paint roller icon)
- Turn on **Data labels** (shows the numbers on the bars)
- Under **Title** > change text to `Budget vs Actual by Program`

#### Visual 2: Card — Total Budget

1. Click empty canvas space
2. Click **Card** visual
3. Drag `Budgeted Amount` to the **Fields** area
4. It will automatically show the SUM
5. In Format pane > **Callout value** > Set display units to `Millions`

#### Visual 3: Card — Total Actual Spend

1. Repeat same steps with `Actual Amount`

#### Visual 4: Table — Detailed Breakdown

1. Click **Table** visual
2. Drag these fields in order:
   - `Program Name`
   - `Budget Category`
   - `Budgeted Amount`
   - `Actual Amount`
   - `Variance`
   - `Status`
3. Resize to fill the bottom half

**Formatting the Table:**

- Format pane > **Style presets** > Choose `Alternating rows` (this is now the default in April 2026+, but verify it's applied)
- Under **Conditional formatting**, right-click the `Status` column header in the visual > **Conditional formatting** > **Background color**:
  - Select **Rules**
  - If value contains `Over Budget` → Red
  - If value contains `At Risk` → Yellow
  - If value contains `On Track` → Green

#### Visual 5: Slicer — Filter by Fiscal Year

1. Click the **Button Slicer** visual in the Visualizations pane
2. Drag `Fiscal Year` field to the **Field** area
3. Place it in the top-right corner
4. Users can click FY2025 or FY2026 to filter the entire page

#### Visual 6: Slicer — Filter by Quarter

1. Click another **Button Slicer** visual
2. Drag `Quarter` field to the **Field** area
3. Place it next to the Fiscal Year slicer
4. Users can click a quarter to filter the entire page

---

## Report 2: Procurement & Purchase Orders

**Audience:** Procurement Officers, Contracting  
**Purpose:** Monitor PO status, vendor spend, and delivery timelines

### Page Setup

- Add a new page: Click the **+** at the bottom
- Rename to `Procurement`

### Visuals to Build

#### Visual 1: Stacked Bar Chart — PO Amount by Vendor

1. Click **Stacked Bar Chart**
2. **Y-axis**: `Purchase Orders` > `Vendor Name`
3. **X-axis**: `Purchase Orders` > `PO Amount`
4. **Legend**: `Purchase Orders` > `PO Status`

This shows which vendors have the most spend and what status their POs are in.

#### Visual 2: Donut Chart — PO Status Distribution

1. Click **Donut Chart**
2. **Legend**: `PO Status`
3. **Values**: `PO ID` (it will count them automatically)
4. Title: `PO Status Breakdown`

#### Visual 3: Table — Outstanding POs

1. Click **Table** visual
2. Add fields: `PO ID`, `Vendor Name`, `PO Amount`, `Amount Remaining`, `Delivery Date`, `Priority`
3. Click the column header `Amount Remaining` in the table > Sort descending (shows largest outstanding amounts first)

**Conditional Formatting on Priority:**

- Right-click `Priority` column header > **Conditional formatting** > **Background color** > **Rules**:
  - `Critical` → Red
  - `High` → Orange
  - `Medium` → Yellow
  - `Low` → Green

#### Visual 4: Clustered Column Chart — Spend by Program

1. Click **Clustered Column Chart**
2. **X-axis**: `Program Name`
3. **Y-axis**: `PO Amount`
4. Title: `Procurement Spend by Program`

#### Visual 5: Slicer — Filter by Priority

1. Click the **Button Slicer** visual in the Visualizations pane (displays items as clickable tiles)
2. Drag `Priority` to the **Field** area
3. This creates a row of clickable buttons — users can select one or multiple priorities

---

## Report 3: Executive Summary (Multi-Page Drillthrough)

**Audience:** Executives, Senior Leadership  
**Purpose:** High-level KPIs with ability to drill into details

### Page Setup

- Add new page > Rename to `Executive Summary`

### Visuals to Build

#### Row 1: KPI Cards (across the top)

Create 4 Card visuals side by side:

| Card              | Table             | Field              | Display Units |
| ----------------- | ----------------- | ------------------ | ------------- |
| Total Budget      | Budget vs Actuals | `Budgeted Amount`  | Millions      |
| Total Actual      | Budget vs Actuals | `Actual Amount`    | Millions      |
| Total PO Value    | Purchase Orders   | `PO Amount`        | Millions      |
| Total Outstanding | Purchase Orders   | `Amount Remaining` | Millions      |

#### Row 2: Program Status Overview

**Visual: Matrix**

1. Click **Matrix** visual
2. **Rows**: `Programs` > `Program Name`
3. **Columns**: `Budget vs Actuals` > `Quarter`
4. **Values**: `Budget vs Actuals` > `Actual Amount`
5. This gives a pivot-table style view of spending by program and quarter

#### Row 3: Trend Chart

**Visual: Line Chart**

1. Click **Line Chart**
2. **X-axis**: `Budget vs Actuals` > `Quarter`
3. **Y-axis**: `Budget vs Actuals` > `Actual Amount`
4. **Legend**: `Programs` > `Program Name`
5. Title: `Spending Trend by Program`

### Setting Up Drillthrough

Drillthrough lets users right-click a program name on the Executive Summary page and jump to a detail page:

1. Add a new page > Rename to `Program Detail`
2. In the **Visualizations** pane on that page, find the **Drillthrough** section at the bottom
3. Drag `Program Name` into the Drillthrough field
4. Now build detail visuals on this page (table of POs, budget breakdown, variance detail for that specific program)
5. A Back button appears automatically — users click it to return to the Executive Summary

---

## Filtering Within Visuals

Power BI offers several ways to filter data directly within visuals, giving report consumers interactive control without needing separate slicers.

### Visual-Level Filters (Filters Pane)

Each visual has its own filter area in the **Filters** pane on the right:

1. Select a visual on the canvas
2. In the **Filters** pane, you'll see three sections:
   - **Filters on this visual** — affects only the selected visual
   - **Filters on this page** — affects all visuals on the current page
   - **Filters on all pages** — affects the entire report
3. Drag any field into one of these sections
4. Set the filter type: Basic (checkboxes), Advanced (contains, starts with, etc.), or Top N

**Example:** Add `Budget vs Actuals` > `Status` to "Filters on this visual" on a table, then check only "Over Budget" and "At Risk" to show only problem areas.

### Show/Hide the Filters Pane for Report Consumers

1. Select the **Filters** pane header
2. In the **Format** pane, toggle **Filters pane** > **Allow end users to filter** (on/off per filter)
3. You can also lock filters so users see them but cannot change them

### Enable Visual Header Filter Icon

This adds a small funnel icon to the top-right of each visual that users can click to filter:

1. Go to **File** > **Options and settings** > **Options**
2. Under **Current file** > **Report settings**
3. Ensure **Persistent filters** is enabled
4. For individual visuals: Click a visual > **Format** pane > **General** > **Header icons** > Turn on **Filter icon**

### Cross-Filtering Between Visuals (Visual Interactions)

Clicking a data point in one visual automatically filters the others on the same page:

1. Click on a visual (e.g., the Clustered Bar Chart)
2. Go to **Format** tab in the ribbon > **Edit interactions**
3. Small icons appear on every other visual:
   - **Filter** (funnel) — the other visual filters to show only related data
   - **Highlight** — the other visual grays out non-related data but still shows totals
   - **None** — no interaction
4. Click the desired icon on each visual to control how they respond

**Recommended interactions for this report:**

- Bar Chart clicking → Filters the Table (shows only that program's details)
- Donut Chart clicking → Highlights the Bar Chart (shows proportion without losing totals)
- KPI Cards → Set to None (cards should always show overall totals)

### Adding a Visual-Level Filter Example (Step-by-Step)

To add a "Top 3 over-budget programs" filter on the Table visual:

1. Click the Table visual
2. In **Filters on this visual**, drag `Variance` field
3. Change filter type to **Top N**
4. Select **Bottom 3** (lowest variance = most over budget)
5. Drag `Variance` to the "By value" area
6. Click **Apply filter**

---

## General Formatting Tips

### Apply a Consistent Theme

1. **View** tab > **Themes** > Browse for a theme or select a built-in one
2. For Coding-Forge branding, consider creating a custom theme with company colors

### Add Page Navigation Buttons

1. **Insert** tab > **Buttons** > **Navigation** > **Page navigator**
2. This adds buttons at the top that let users click between pages

### Add a Title Banner

1. **Insert** tab > **Text box**
2. Type your report title (e.g., "Coding-Forge Program Financial Dashboard")
3. Format: Bold, larger font, company blue background

### Refresh Schedule (After Publishing)

In Power BI Service:

1. Go to the dataset in your workspace
2. **Settings** > **Scheduled refresh**
3. Set to refresh daily or as needed (depends on Dataverse gateway configuration)

---

*For data cleanup steps, see POWER_QUERY_TRANSFORMATIONS.md.*  
*For connection and setup details, see INSTRUCTIONS.md.*
