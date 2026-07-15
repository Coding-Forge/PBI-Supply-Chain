# PBI Factory Workshop Tracking

This file tracks completed changes, open work, and safe-edit procedures for the PBI Factory PBIP workshop project.

## Current project

- Repository: `C:\Projects\PowerBI\workshop\PBI_Factory`
- Active branch: `main`
- PBIP file: `Training\PBI_Factory.pbip`
- Semantic model folder: `Training\PBI_Factory.SemanticModel`
- Training data folder: `TrainingData`

## Change log

### 2026-07-15

- Renamed the local Git branch from `master` to `main`.
- Updated Power Query CSV source paths in the semantic model to use the local workshop training data folder:
  - `Training\PBI_Factory.SemanticModel\definition\tables\Budget vs Actuals.tmdl`
  - `Training\PBI_Factory.SemanticModel\definition\tables\Programs.tmdl`
  - `Training\PBI_Factory.SemanticModel\definition\tables\Purchase Orders.tmdl`
- Fixed TMDL indentation on the edited M expression lines after Power BI Desktop reported an indentation parse error.
- Added this tracking file to document work performed and safe editing practices.
- Added three modern comparison pages while keeping the original pages:
  - `Executive Command Center`
  - `Program Health Modern`
  - `Procurement Operations`
- Added `Student\DeliveryGuide\Modern Report Pages Delivery Guide.md` with instructor notes and page-by-page discussion prompts.

## Open work

- Reopen `Training\PBI_Factory.pbip` in Power BI Desktop and confirm the project loads without TMDL format errors.
- Refresh the model and confirm all CSV sources resolve from `TrainingData`.
- Review the new modern pages in Power BI Desktop and adjust any visual sizing, titles, or interactions that need final polish.
- Review the report pages, visuals, relationships, measures, and training instructions for the defense-industry delivery.
- Replace any remaining copied sample content, branding, terminology, or data that does not fit the intended defense-industry workshop.
- Commit after each meaningful, working change so rollback points remain available.

## Safe PBIP editing checklist

Use this checklist before editing any PBIP, TMDL, report, or semantic model file by hand.

1. Close Power BI Desktop completely before editing project files.
2. Confirm no `PBIDesktop.exe` process is still running.
3. Check Git status before editing:
   ```powershell
   git --no-pager status --short --branch
   ```
4. If there are unexpected local changes, stop and identify the owner or purpose before editing the same files.
5. Make a small, focused edit.
6. Validate file formatting and source references.
7. Reopen the PBIP in Power BI Desktop.
8. Confirm the project loads, refreshes, and behaves as expected.
9. Close Power BI Desktop again before making additional manual file edits.
10. Commit the working change with a clear message.

## TMDL standards checklist

Power BI Project TMDL files are indentation-sensitive. Follow these standards for manual edits.

1. Preserve existing indentation exactly. TMDL object structure commonly uses tabs, and M expression blocks may include spaces after those tabs.
2. Do not convert tabs to spaces across a `.tmdl` file.
3. Do not auto-format `.tmdl` files with a generic formatter.
4. Keep M expression lines under a `source =` property aligned with the surrounding expression block.
5. For Power Query source paths, change only the string value unless a broader refactor is intentional.
6. Preserve existing line endings. Avoid mixed line endings in the same file.
7. Avoid trailing whitespace unless it already exists as part of a generated structure.
8. After editing, inspect the changed lines with visible tabs or an equivalent check.
9. Search for stale copied paths before testing:
   ```powershell
   Select-String -Path (Get-ChildItem 'Training' -Recurse -File | Select-Object -ExpandProperty FullName) -Pattern 'C:\\Users\\|Downloads\\|syhassan' -CaseSensitive:$false
   ```
10. Open the PBIP in Power BI Desktop as the final parser validation.

## Git practice

Commit after each validated change or logical group of related changes.

Recommended flow:

```powershell
git --no-pager status --short --branch
git --no-pager diff --check
git add <changed-files>
git commit -m "<clear change summary>"
```

Rollback examples:

```powershell
git --no-pager log --oneline -10
git --no-pager show <commit>
git restore --source=<commit> -- <file>
```

Do not use destructive rollback commands such as `git reset --hard` unless explicitly approved.

## Useful validation commands

Check for edited Power Query source paths:

```powershell
Select-String -Path 'Training\PBI_Factory.SemanticModel\definition\tables\*.tmdl' -Pattern 'File\.Contents|Folder\.Files|Web\.Contents|SharePoint|Sql\.Database'
```

Check leading indentation around source expressions:

```powershell
$paths = @(
  'Training\PBI_Factory.SemanticModel\definition\tables\Budget vs Actuals.tmdl',
  'Training\PBI_Factory.SemanticModel\definition\tables\Programs.tmdl',
  'Training\PBI_Factory.SemanticModel\definition\tables\Purchase Orders.tmdl'
)

foreach ($path in $paths) {
  Write-Host "--- $path"
  $lines = [System.IO.File]::ReadAllLines((Resolve-Path $path))
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'File\.Contents|source =|^\s*let|Source = Csv\.Document|^\s*in\s*$') {
      $visible = $lines[$i].Replace("`t", '<TAB>')
      '{0,4}: {1}' -f ($i + 1), $visible
    }
  }
}
```
