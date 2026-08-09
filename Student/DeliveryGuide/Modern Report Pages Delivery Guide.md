# Modern Report Pages Delivery Guide

This guide supports the new comparison pages added to `Training\PBI_Factory.pbip`. The original workshop pages remain in place so instructors and students can compare the guided build with a more polished report design.

## Page comparison map

| Original page | Modern comparison page | Purpose |
| --- | --- | --- |
| Executive Summary | Executive Command Center | Show a cleaner executive landing page with KPI cards, trend context, and a detailed program matrix. |
| Program Health | Program Health Modern | Present budget health with a left-to-right flow from filters to variance summary, program comparison, and detail review. |
| Procurement | Procurement Operations | Convert the procurement page into an action-oriented operations view for priority, vendor exposure, status mix, and purchase order follow-up. |

## Instructor notes

Before delivery, complete the customer-branding checklist in `Delivery Branding Guide.md`. The current HTML configuration is set to Boeing through `Student\Lab\delivery-config.js`.

1. Start each section on the original page and ask students what works well and what feels unfinished.
2. Move to the matching modern page and discuss the design changes.
3. Emphasize that the modern pages use the same model fields as the original pages, so the improvement is driven by layout, hierarchy, titles, and report storytelling.
4. Use the comparison to discuss report development as an iterative process: first make the data work, then improve the user experience.

## Executive Command Center

### Learning objective

Help students understand how to turn a basic executive summary into a command-center style landing page.

### Discussion points

- KPI cards are grouped across the top to provide immediate financial context.
- The spend trend visual is positioned below the KPIs to explain movement over time.
- The matrix remains available as supporting detail instead of competing with top-level indicators.
- The page title and visual titles use defense-oriented language such as commitment, budget authority, and spend trend.

### Suggested walkthrough

1. Compare the original scattered KPI layout with the modern top-row KPI pattern.
2. Discuss how executives typically scan reports: headline metrics first, trend second, details last.
3. Ask students which KPIs they would add for a real defense program review, such as obligation rate, burn rate, or unfunded requirement.

## Program Health Modern

### Learning objective

Show how a program health page can guide the user from filter selection to summary interpretation and then to detail-level review.

### Discussion points

- Filters are placed in the upper-left area to establish report context.
- Budget variance is surfaced as a summary visual near the filters.
- Program comparison is placed prominently so outliers are visible.
- The detail table stays at the bottom for auditability and drill-down discussion.

### Suggested walkthrough

1. Start with fiscal-year and quarter filtering.
2. Review variance by budget category.
3. Use the program budget chart to identify the largest programs.
4. Review the detail table to connect visual insights back to program, cost center, status, and fiscal-year records.

## Procurement Operations

### Learning objective

Demonstrate how procurement data can be organized as an operational action queue.

### Discussion points

- Priority filtering is placed first to support triage.
- Vendor exposure and PO status visuals help identify concentration and execution risk.
- Program-level PO amounts show where procurement activity is concentrated.
- The action queue table supports follow-up on PO ID, vendor, remaining amount, delivery date, and priority.

### Suggested walkthrough

1. Filter by priority to focus the procurement queue.
2. Review vendor exposure by status.
3. Check PO status mix to understand execution maturity.
4. Use the action queue to identify items that need follow-up.

## Optional student exercise

Ask students to choose one modern page and propose one additional improvement:

- Add a slicer that supports the story.
- Rename a visual title for an executive audience.
- Reposition a visual to improve scan order.
- Replace a table with a visual that better answers the business question.
- Add a defense-specific KPI that is not currently in the dataset.

## Maintenance notes

- Update `Student\Lab\delivery-config.js` before each customer delivery and verify every HTML page.
- Keep Coding-Forge references when they identify the fictitious dataset or repository rather than the delivery customer.
- Close Power BI Desktop before editing PBIP project files manually.
- Preserve TMDL and PBIR indentation and line endings.
- Commit after each validated change so the workshop can be rolled back safely.
