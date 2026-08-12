# Power BI Workshop: Instructor Runbook

This package contains the complete delivery kit. It includes the student materials and instructor-only references, solutions, lesson decks, and operations assets.

## Important

Distribute the separate **student ZIP** to attendees. Do not distribute this instructor package because it contains completed reports, delivery notes, certificate tooling, and supporting assets.

## Package layout

| Path | Purpose |
| --- | --- |
| `Student` | Exact student-facing lab, screenshot, branding, and quick-start material. |
| `Instructor\DeliveryGuide` | Branding and report-page delivery guidance. |
| `Instructor\Customer Communications` | Reusable readiness email, regeneration script, and student manual PDF backups. |
| `Instructor\Slide Decks` | Canonical Lessons 1–4 for delivery. |
| `Instructor\Completed Reports` | Canonical completed report for demonstration and recovery. |
| `Instructor\Source Data` | Local CSV fallback and validation sources. |
| `Instructor\Reference` | PDF guides, Power Query code, and report backgrounds. |
| `Instructor\Certificates` | Certificate template and merge database. |

## Before the delivery

1. Customize `Instructor\Customer Communications\Customer Training Access and Readiness Email.md`, test the student download link, and send it before the stated readiness deadline.
2. Open the backup PDFs in `Instructor\Customer Communications\Student Manual PDFs` and verify their lab content and delivery branding. Regenerate them after source or branding changes.
3. Read `Instructor\DeliveryGuide\Delivery Branding Guide.md`.
4. Confirm the customer name, workshop name, colors, icons, and approved logo in `Student\Labs\Web\scripts\delivery-config.js` before building the release.
5. Open `Student\Labs\Web\index.html` and every lab page at desktop and phone widths.
6. Verify the Coding-Forge raw GitHub URLs are reachable from the delivery network.
7. Test the local CSV fallback from `Instructor\Source Data`.
8. Open and refresh the completed report using the current Power BI Desktop release.
9. Confirm the expected totals in Lab 3.
10. Confirm which Power BI government tenant attendees use. Lab 4 lists GCC, GCC High, and DoD without choosing a default.
11. Verify attendees have a government Pro or PPU license and an approved practice workspace when Lab 4 includes hands-on publishing.
12. Review customer and organizational policy before enabling external sources, sharing, refresh, gateways, or sensitivity labels.

## Suggested delivery flow

| Segment | Material | Instructor focus |
| --- | --- | --- |
| Introduction | Lesson 1 and course home | Outcomes, fictitious data boundary, Power BI workflow. |
| Lab 1 | Lesson 2 and student Lab 1 | Raw URLs, Web connector, source profiling, fallback path. |
| Lab 2 | Lesson 2 and student Lab 2 | Transformation intent, quality checks, star schema. |
| Lab 3 | Lesson 3 and student Lab 3 | Measures, layout, interactions, accessibility, totals. |
| Lab 4 | Lesson 4 and student Lab 4 | Sovereign endpoint, publishing, credentials, refresh, governed access. |
| Lab 5 | Student Lab 5 | Workspace ownership, collaboration roles, app audiences, and scheduled refresh. |
| Follow up | Student Follow Up page | Optional production-readiness enhancements. |

## Facilitation and recovery

- Keep the completed report closed until students need a demonstration or recovery checkpoint.
- If a student falls behind, use the completed report as a reference; do not replace their work without explaining the recovery point.
- Use the local CSV files only when the public source is blocked and local-file use is approved.
- Never direct students to bypass government tenant, firewall, gateway, or data-loss-prevention controls.
- Never use **Publish to web** for government or organizational content.

## After the delivery

1. Remove attendee names and customer-specific artifacts from shared working folders.
2. Store or dispose of certificate merge data according to organizational policy.
3. Record issues with screenshots, source access, Power BI version, government-cloud behavior, and lab timing.
4. Apply corrections in source control and rebuild both release archives together.