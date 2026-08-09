# Delivery Branding Guide

Use this guide before every customer delivery. The student HTML pages use a shared branding component so the customer name and approved logo can be changed in one place.

## Current delivery

- Customer: **Boeing**
- Workshop label: **Power BI Workshop**
- Brand configuration: `Student\Lab\delivery-brand.js`
- Customer logo: not bundled; the generic aviation icon is used until an approved asset is provided

## Required instructor update

Open `Student\Lab\delivery-brand.js` and update only the configuration at the top of the file:

```javascript
const deliveryBrand = {
  customerName: "Boeing",
  workshopName: "Power BI Workshop",
  logoPath: ""
};
```

| Setting | Instructor action |
| --- | --- |
| `customerName` | Replace with the delivery customer’s approved display name. |
| `workshopName` | Keep `Power BI Workshop` or replace it with the approved event title. |
| `logoPath` | Leave blank for the generic icon, or provide a relative path to an approved SVG or PNG. |

The component adds the customer masthead to all six HTML pages and appends the customer name to each browser title.

## Using an approved customer logo

1. Obtain the logo from the customer, account team, or approved internal brand library. Do not download an unofficial logo from image search.
2. Place the asset in `Student\Images`, for example:
   ```text
   Student\Images\customer-logo.svg
   ```
3. Set the path relative to the HTML files in `Student\Lab`:
   ```javascript
   logoPath: "../Images/customer-logo.svg"
   ```
4. Prefer a transparent SVG or PNG with enough internal padding to remain legible in the 40 × 40 pixel masthead mark.
5. Open the course home and one lab in both light and dark themes. Confirm the logo is legible and does not stretch or clip.

The customer name remains visible text even when a logo is configured. This preserves accessibility and avoids relying on the logo alone for identification.

## Do not replace fictitious-data references automatically

`Coding-Forge` identifies the fictitious company, repository, data folder, and report filename used by the lab. It is not the delivery customer.

Keep Coding-Forge references when only the delivery branding changes, including:

- GitHub raw-data URLs
- `Coding-Forge_Data`
- `Coding-Forge-Supply-Chain-Lab.pbix`
- report examples that describe the fictitious dataset

Change those references only when the source repository and training data are intentionally replaced and validated end to end.

## Pre-delivery verification

1. Search `Student\Lab` for the previous customer name.
2. Open `Student\Lab\index.html` and confirm the masthead customer and workshop name.
3. Open Labs 1–4 and Follow Up; verify the masthead appears once on every page.
4. Check desktop and phone widths for horizontal overflow.
5. Verify the course home still lists four guided labs.
6. Confirm all local links resolve.
7. Confirm Coding-Forge data URLs still work unless the dataset was intentionally replaced.
8. Review Power BI report files separately for titles, themes, logos, and customer-specific metadata.

## Current Boeing delivery note

The HTML course is configured for Boeing by name and uses a neutral aviation icon. Replace the generic icon only when an approved Boeing logo asset is supplied for this delivery.