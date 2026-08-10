# Customer Communications and Backup Manuals

This folder contains reusable pre-delivery communications and PDF backups for instructors. Its contents are included only in the instructor release.

## Student manual PDFs

`Student Manual PDFs` contains printable backups of the current student course:

- Course overview
- Labs 1–4
- Optional Follow Up

Use these files only when students cannot use the interactive HTML manuals or when an approved document channel requires PDF attachments. The HTML course remains the primary experience because it provides navigation and locally stored progress checklists.

The PDFs reflect the delivery branding configured in `Student\Labs\Web\scripts\delivery-config.js` at generation time. Regenerate them after changing lab content, screenshots, or branding.

## Regenerate the PDFs

Microsoft Edge and Python are required. From the repository root:

1. Start a temporary local server:

   ```powershell
   python -m http.server 8766 --bind 127.0.0.1
   ```

2. In another PowerShell terminal, run:

   ```powershell
   .\Communications\build-student-manual-pdfs.ps1
   ```

3. Stop the temporary server.
4. Open every generated PDF and spot-check headings, screenshots, page breaks, links, and current delivery branding.
5. Rebuild both release archives. Confirm the PDFs appear only under `Instructor\Customer Communications\Student Manual PDFs` in the instructor archive.

The generator intentionally fails when the local source server is unavailable or Edge cannot create an expected PDF.

## Distribution rules

- Never add this folder or its PDF files to the student release manifest.
- Never send the instructor ZIP to attendees.
- Individual backup PDFs may be sent to attendees when needed.
- Review each PDF for correct customer branding before sending it.
- Do not add customer data, attendee information, credentials, or access tokens.