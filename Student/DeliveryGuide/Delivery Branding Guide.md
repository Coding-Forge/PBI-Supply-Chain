# Delivery Branding Guide

Use this guide before every customer delivery. The student HTML pages use a shared branding component so the customer name and approved logo can be changed in one place.

## Current delivery

- Customer: **Boeing**
- Workshop label: **Power BI Workshop**
- Brand configuration: `Student\Lab\delivery-config.js`
- Shared renderer: `Student\Lab\delivery-brand.js`
- Customer assets: `Student\Lab\Branding\Boeing`

## Required instructor update

Open `Student\Lab\delivery-config.js` and update the delivery configuration:

```javascript
window.deliveryBrandConfig = {
  customerName: "Boeing",
  workshopName: "Power BI Workshop",
   titleSuffix: "Boeing",
   logoPath: "Branding/Boeing/boeing-mark.svg",
   badgePath: "Branding/Boeing/boeing-name-badge.svg"
};
```

| Setting | Instructor action |
| --- | --- |
| `customerName` | Replace with the delivery customer’s approved display name. |
| `workshopName` | Keep `Power BI Workshop` or replace it with the approved event title. |
| `titleSuffix` | Set the customer name appended to each browser title. |
| `logoPath` | Set a relative path to an approved compact logo SVG or PNG. Leave blank for the generic icon. |
| `badgePath` | Set a relative path to an approved combined customer/workshop badge. Leave blank to show the logo and text separately. |
| `theme` | Set approved accent, hover, soft-background, foreground, and link colors. |
| `icons` | Set optional delivery, cloud, and governance icon paths used by branded page content. |

The component adds the customer masthead to all six HTML pages and appends the customer name to each browser title.

## Using an approved customer logo

1. Obtain the logo from the customer, account team, or approved internal brand library. Do not download an unofficial logo from image search.
2. Create a customer folder under `Student\Lab\Branding` and place the approved assets there, for example:
   ```text
   Student\Lab\Branding\Customer\customer-mark.svg
   ```
3. Set the paths relative to the HTML files in `Student\Lab`:
   ```javascript
   logoPath: "Branding/Customer/customer-mark.svg",
   badgePath: "Branding/Customer/customer-name-badge.svg"
   ```
4. Prefer a transparent SVG or PNG with enough internal padding to remain legible in the 40 × 40 pixel masthead mark.
5. Open the course home and one lab in both light and dark themes. Confirm the logo is legible and does not stretch or clip.

When a badge is configured, its alt text combines the customer and workshop names. When only a logo is configured, visible customer and workshop text remains beside it.

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
8. Confirm every path configured in `delivery-config.js` is included in the student release.
9. Review Power BI report files separately for titles, themes, logos, and customer-specific metadata.

## Current Boeing delivery note

The HTML course is configured for Boeing and uses the approved assets currently stored under `Student\Lab\Branding\Boeing`. Confirm those assets and their permitted use before each delivery.