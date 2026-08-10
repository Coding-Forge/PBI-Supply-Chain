# Power BI Workshop Solution

This repository contains a reusable, instructor-led Power BI workshop. Participants connect to fictitious supply-chain data, transform it with Power Query, build a semantic model and report, and publish the result to an approved Power BI environment.

The solution includes four guided labs, optional follow-up exercises, instructor presentations, completed report references, delivery guidance, and a repeatable release-packaging process.

## Workshop path

1. Connect to CSV data hosted on GitHub.
2. Clean and validate the data with Power Query.
3. Build a star schema, measures, and interactive report pages.
4. Publish, refresh, and validate access in Power BI.

The publishing lab includes guidance for Power BI US Government environments. Instructors must confirm the appropriate tenant, licensing, workspace, and organizational policies before delivery.

## Use a release

Download the package intended for your role from the repository's GitHub Releases page.

### Students

Extract the student archive and open `Labs\Web\index.html` in a current browser. The package contains the guided labs, screenshots, branding assets, and local CSV fallback files. Completed reports and instructor material are intentionally excluded.

### Instructors

Extract the instructor archive and begin with its `README.md`. The package contains the student kit plus lesson decks, delivery guides, completed reports, source data, certificate assets, report backgrounds, reference documents, and sample reports.

Do not distribute the instructor package to students because it contains completed solutions and delivery-only material.

## Repository structure

| Path | Purpose |
| --- | --- |
| `Student\Labs\Web` | Course home, guided labs, optional exercises, and delivery branding. |
| `Student\Labs\PDF` | PDF lab instructions and reference guides. |
| `Student\Labs\Images` | Screenshots used by the lab pages. |
| `Student\Labs\Completed` | Completed Power BI report references and formatting utility. |
| `Instructor\DeliveryGuide` | Instructor preparation, report design, and branding guidance. |
| `Coding-Forge_Data` | Local copies of the fictitious workshop data. |
| `Instructor\PPT` | Instructor lesson decks and archived source material. |
| `Certificate` | Certificate generation assets. |
| `Sample Reports` | Supplemental demonstration reports. |
| `Communications` | Reusable readiness email, instructor-only backup manuals, and PDF generator. |
| `Release` | Package documentation and the release builder. |
| `PBIP` | Local Power BI project workspace; ignored by Git and release packaging. |

Coding-Forge is the fictitious organization represented by the workshop data and source URLs. It is separate from any customer or organization receiving the training.

## Customize a delivery

Configure the delivery identity in `Student\Labs\Web\scripts\delivery-config.js`. Customer-approved logos and icons belong under `Student\Labs\Web\Branding\<Customer>`.

See `Instructor\DeliveryGuide\Delivery Branding Guide.md` for supported settings and asset requirements. Changing the delivery identity must not alter Coding-Forge data names, repository URLs, filenames, or report examples.

## Build releases

Run the builder from the repository root with a release version:

```powershell
.\Release\build-releases.ps1 -Version "<version>"
```

For example:

```powershell
.\Release\build-releases.ps1 -Version "2026.08.09"
```

Generated files are written to the ignored `Release\dist` directory:

- `PBI-Factory-Student-<version>.zip`
- `PBI-Factory-Instructor-<version>.zip`
- `SHA256SUMS.txt`

The builder validates required files, duplicate archive entries, solution-file exclusions, and PBIP exclusions. Build both packages together so their contents and checksums remain aligned.

## Publish a release

1. Commit and push the validated source changes.
2. Build both archives using the intended version.
3. Create and push the required Git tag or tags.
4. Create the GitHub release and attach both ZIP files and `SHA256SUMS.txt`.
5. Record the Power BI Desktop version and significant workshop changes in the release notes.
6. Download the published assets and verify their SHA-256 hashes.

Generated archives should be uploaded as release assets rather than committed to the repository.

## Validate changes

Before publishing:

1. Open every HTML page at desktop and phone widths.
2. Confirm that all local links, scripts, images, and branding assets resolve.
3. Refresh the completed report and verify the expected model, measures, and totals.
4. Confirm that publishing instructions match the intended Power BI environment without assuming a tenant.
5. Remove references and assets from previous deliveries.
6. Build and extract both archives, inspect their contents, and verify `SHA256SUMS.txt`.

Workshop data is fictitious. Do not introduce customer, controlled, classified, export-controlled, or operational data into the repository or release packages.
