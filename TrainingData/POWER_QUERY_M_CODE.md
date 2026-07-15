# Power Query M Code — All Transformations

## How to Use This File

If you want to paste the full transformation code instead of doing each step manually:

1. Open Power BI Desktop
2. **Home** > **Transform Data** (opens Power Query Editor)
3. Right-click the query in the left panel > **Advanced Editor**
4. Replace everything with the code below
5. Click **Done**

---

## File 1: Financial Data - Budget vs Actuals

```powerquery
let
    // Step 1: Load the CSV file
    Source = Csv.Document(
        File.Contents("C:\Training Data\Financial Data - Budget vs Actuals.csv"),
        [Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),

    // Step 2: Promote the first row to column headers
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    // Step 3: Remove the 3 footer/notes rows at the bottom
    #"Removed Bottom Rows" = Table.RemoveLastN(#"Promoted Headers", 3),

    // Step 4: Trim extra spaces from text columns
    #"Trimmed Text" = Table.TransformColumns(#"Removed Bottom Rows", {
        {"Program Name", Text.Trim, type text},
        {"Program ID", Text.Trim, type text},
        {"Cost Center", Text.Trim, type text},
        {"Budget Category", Text.Trim, type text},
        {"Funding Source", Text.Trim, type text},
        {"Status", Text.Trim, type text}
    }),

    // Step 5: Remove dollar signs from amount columns (Budgeted Amount, Actual Amount, Variance)
    #"Removed $ from Budgeted Amount" = Table.ReplaceValue(#"Trimmed Text", "$", "", Replacer.ReplaceText, {"Budgeted Amount"}),
    #"Removed $ from Actual Amount" = Table.ReplaceValue(#"Removed $ from Budgeted Amount", "$", "", Replacer.ReplaceText, {"Actual Amount"}),
    #"Removed $ from Variance" = Table.ReplaceValue(#"Removed $ from Actual Amount", "$", "", Replacer.ReplaceText, {"Variance"}),

    // Step 6: Remove commas from amount columns
    #"Removed , from Budgeted Amount" = Table.ReplaceValue(#"Removed $ from Variance", ",", "", Replacer.ReplaceText, {"Budgeted Amount"}),
    #"Removed , from Actual Amount" = Table.ReplaceValue(#"Removed , from Budgeted Amount", ",", "", Replacer.ReplaceText, {"Actual Amount"}),
    #"Removed , from Variance" = Table.ReplaceValue(#"Removed , from Actual Amount", ",", "", Replacer.ReplaceText, {"Variance"}),

    // Step 7: Remove parentheses from negative amounts (e.g., "(120000)" → "-120000")
    #"Removed ( from Budgeted Amount" = Table.ReplaceValue(#"Removed , from Variance", "(", "-", Replacer.ReplaceText, {"Budgeted Amount"}),
    #"Removed ) from Budgeted Amount" = Table.ReplaceValue(#"Removed ( from Budgeted Amount", ")", "", Replacer.ReplaceText, {"Budgeted Amount"}),
    #"Removed ( from Actual Amount" = Table.ReplaceValue(#"Removed ) from Budgeted Amount", "(", "-", Replacer.ReplaceText, {"Actual Amount"}),
    #"Removed ) from Actual Amount" = Table.ReplaceValue(#"Removed ( from Actual Amount", ")", "", Replacer.ReplaceText, {"Actual Amount"}),
    #"Removed ( from Variance" = Table.ReplaceValue(#"Removed ) from Actual Amount", "(", "-", Replacer.ReplaceText, {"Variance"}),
    #"Removed ) from Variance" = Table.ReplaceValue(#"Removed ( from Variance", ")", "", Replacer.ReplaceText, {"Variance"}),

    // Step 8: Remove % signs from Variance %
    #"Removed % Signs" = Table.ReplaceValue(#"Removed ) from Variance", "%", "", Replacer.ReplaceText, {"Variance %"}),

    // Step 9: Replace N/A with blank in Actual Amount, Variance, and Variance %
    #"Replaced N/A in Actual Amount" = Table.ReplaceValue(#"Removed % Signs", "N/A", "", Replacer.ReplaceText, {"Actual Amount"}),
    #"Replaced N/A in Variance" = Table.ReplaceValue(#"Replaced N/A in Actual Amount", "N/A", "", Replacer.ReplaceText, {"Variance"}),
    #"Replaced N/A in Variance %" = Table.ReplaceValue(#"Replaced N/A in Variance", "N/A", "", Replacer.ReplaceText, {"Variance %"}),

    // Step 10: Change ALL amount columns to Decimal Number type
    #"Changed Types" = Table.TransformColumnTypes(#"Replaced N/A in Variance %", {
        {"Budgeted Amount", type number},
        {"Actual Amount", type number},
        {"Variance", type number},
        {"Variance %", type number}
    }),

    // Step 11: Capitalize Each Word in Budget Category
    #"Capitalized Budget Category" = Table.TransformColumns(#"Changed Types", {
        {"Budget Category", Text.Proper, type text}
    }),

    // Step 12: Replace "Sub-Contracts" with "Subcontracts"
    #"Fixed Sub-Contracts" = Table.ReplaceValue(#"Capitalized Budget Category", "Sub-Contracts", "Subcontracts", Replacer.ReplaceText, {"Budget Category"}),

    // Step 13: Capitalize Each Word in Status column
    #"Capitalized Status" = Table.TransformColumns(#"Fixed Sub-Contracts", {
        {"Status", Text.Proper, type text}
    }),

    // Step 14: Fix shortened program names
    #"Fixed Satellite Name" = Table.ReplaceValue(#"Capitalized Status", "Satellite Comm Upgrade", "Satellite Communications Upgrade", Replacer.ReplaceText, {"Program Name"}),
    #"Fixed Radar Name" = Table.ReplaceValue(#"Fixed Satellite Name", "Next Gen Radar Systems", "Next-Gen Radar Systems", Replacer.ReplaceText, {"Program Name"})
in
    #"Fixed Radar Name"
```

---

## File 2: Financial Data - Purchase Orders

```powerquery
let
    // Step 1: Load the CSV file
    Source = Csv.Document(
        File.Contents("C:\Training Data\Financial Data - Purchase Orders.csv"),
        [Delimiter=",", Columns=17, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),

    // Step 2: Promote the first row to column headers
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    // Step 3: Remove duplicate rows based on PO ID
    #"Removed Duplicates" = Table.Distinct(#"Promoted Headers", {"PO ID"}),

    // Step 4: Trim spaces from all text columns
    #"Trimmed Text" = Table.TransformColumns(#"Removed Duplicates", {
        {"PO ID", Text.Trim, type text},
        {"PO Number", Text.Trim, type text},
        {"Vendor Name", Text.Trim, type text},
        {"Vendor ID", Text.Trim, type text},
        {"Program ID", Text.Trim, type text},
        {"Program Name", Text.Trim, type text},
        {"Description", Text.Trim, type text},
        {"PO Status", Text.Trim, type text},
        {"Approver Name", Text.Trim, type text},
        {"Cost Center", Text.Trim, type text},
        {"Priority", Text.Trim, type text},
        {"CLIN Number", Text.Trim, type text}
    }),

    // Step 5: Remove $ from PO Amount
    #"Removed $ from PO Amount" = Table.ReplaceValue(#"Trimmed Text", "$", "", Replacer.ReplaceText, {"PO Amount"}),

    // Step 6: Remove commas from PO Amount
    #"Removed , from PO Amount" = Table.ReplaceValue(#"Removed $ from PO Amount", ",", "", Replacer.ReplaceText, {"PO Amount"}),

    // Step 7: Remove $ from Amount Paid
    #"Removed $ from Amount Paid" = Table.ReplaceValue(#"Removed , from PO Amount", "$", "", Replacer.ReplaceText, {"Amount Paid"}),

    // Step 8: Remove commas from Amount Paid
    #"Removed , from Amount Paid" = Table.ReplaceValue(#"Removed $ from Amount Paid", ",", "", Replacer.ReplaceText, {"Amount Paid"}),

    // Step 9: Remove $ from Amount Remaining
    #"Removed $ from Amount Remaining" = Table.ReplaceValue(#"Removed , from Amount Paid", "$", "", Replacer.ReplaceText, {"Amount Remaining"}),

    // Step 10: Remove commas from Amount Remaining
    #"Removed , from Amount Remaining" = Table.ReplaceValue(#"Removed $ from Amount Remaining", ",", "", Replacer.ReplaceText, {"Amount Remaining"}),

    // Step 11: Replace NULL with 0 in Amount Paid
    #"Replaced NULL" = Table.ReplaceValue(#"Removed , from Amount Remaining", "NULL", "0", Replacer.ReplaceText, {"Amount Paid"}),

    // Step 12: Replace dash (-) with 0 in Amount Paid
    #"Replaced Dash" = Table.ReplaceValue(#"Replaced NULL", "-", "0", Replacer.ReplaceValue, {"Amount Paid"}),

    // Step 13: Change amount columns to Decimal Number type
    #"Changed Amount Types" = Table.TransformColumnTypes(#"Replaced Dash", {
        {"PO Amount", type number},
        {"Amount Paid", type number},
        {"Amount Remaining", type number}
    }),

    // Step 14: Change Order Date to Date type
    #"Changed Order Date Type" = Table.TransformColumnTypes(#"Changed Amount Types", {
        {"Order Date", type date}
    }),

    // Step 15: Replace errors in Order Date (from non-standard date formats)
    #"Replaced Order Date Errors" = Table.ReplaceErrorValues(#"Changed Order Date Type", {{"Order Date", null}}),

    // Step 16: Change Delivery Date to Date type
    #"Changed Delivery Date Type" = Table.TransformColumnTypes(#"Replaced Order Date Errors", {
        {"Delivery Date", type date}
    }),

    // Step 17: Replace errors in Delivery Date
    #"Replaced Delivery Date Errors" = Table.ReplaceErrorValues(#"Changed Delivery Date Type", {{"Delivery Date", null}}),

    // Step 18: Capitalize Each Word in PO Status
    #"Capitalized PO Status" = Table.TransformColumns(#"Replaced Delivery Date Errors", {
        {"PO Status", Text.Proper, type text}
    }),

    // Step 19: Capitalize Each Word in Priority
    #"Capitalized Priority" = Table.TransformColumns(#"Capitalized PO Status", {
        {"Priority", Text.Proper, type text}
    }),

    // Step 20: Fix vendor name inconsistencies
    #"Fixed Apex" = Table.ReplaceValue(#"Capitalized Priority", "Apex Dynamics Corp.", "Apex Dynamics Corp", Replacer.ReplaceText, {"Vendor Name"}),
    #"Fixed Centurion" = Table.ReplaceValue(#"Fixed Apex", "Centurion Inc.", "Centurion Inc", Replacer.ReplaceText, {"Vendor Name"}),

    // Step 21: Fix shortened program names
    #"Fixed Program Name" = Table.ReplaceValue(#"Fixed Centurion", "Satellite Comm Upgrade", "Satellite Communications Upgrade", Replacer.ReplaceText, {"Program Name"})
in
    #"Fixed Program Name"
```

---

## Notes

- **File paths:** Update the `File.Contents(...)` path to match where you saved the CSV files on your machine.
- **Date handling:** Power BI will auto-detect most date formats. The `ReplaceErrorValues` step catches any dates that fail to parse (e.g., `"Feb 10 2025"` format).
- **Null vs blank:** When replacing `N/A` or `NULL` with blank/zero, Power BI treats blank text cells as `null` after type conversion — this is expected behavior.
- **Text.Proper:** The `Text.Proper` function (Capitalize Each Word) handles most casing issues. The explicit Replace Values steps after it ensure multi-word statuses stay consistent (e.g., "Over Budget" not "Over budget").
