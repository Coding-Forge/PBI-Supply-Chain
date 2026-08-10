# Customer Training Access and Readiness Email

Use this template to prepare attendees for the Power BI workshop. Replace every value in angle brackets before sending, remove sections that do not apply, and verify all links against the customer's approved environment.

## Instructor preparation

Before sending this email:

1. Publish the student ZIP as a release asset or place it in an approved customer-accessible location.
2. Test the exact student download link from an account with the same access level as an attendee.
3. Confirm the workshop date, time zone, delivery format, and support contact.
4. Confirm whether attendees will complete Lab 4 in GCC, GCC High, DoD, commercial Power BI, or as an instructor-led demonstration only.
5. Confirm the required Power BI license and destination workspace with the customer's tenant administrator.
6. Confirm whether `raw.githubusercontent.com` is permitted. If it is blocked, approve use of the CSV files included in the student package.
7. Remove all unused placeholders and optional instructions.
8. Never attach or link to the instructor release.

## Copy-ready email

**Subject:** Action required: prepare for <WORKSHOP NAME> on <DATE>

Hello <ATTENDEE OR TEAM NAME>,

You are registered for **<WORKSHOP NAME>** on **<DATE> from <START TIME> to <END TIME> <TIME ZONE>**. This is a hands-on Power BI workshop. Please complete every readiness check below no later than **<READINESS DEADLINE>** so we can use the class time for the labs rather than account, software, or network troubleshooting.

### What you will build

During the workshop, you will:

1. Connect Power BI Desktop to fictitious CSV data.
2. Clean and validate the data with Power Query.
3. Build a semantic model, DAX measures, and interactive report pages.
4. <Publish and validate the report in the approved Power BI environment. | Observe an instructor demonstration of publishing.>

No customer, controlled, classified, export-controlled, or operational data is required or permitted. The Coding-Forge workshop data is fictitious.

### Get the student materials

Download the **student package only** from:

<DIRECT LINK TO STUDENT ZIP OR APPROVED DOWNLOAD PAGE>

The expected file is:

`PBI-Factory-Student-<VERSION>.zip`

Complete these steps before class:

1. Download the ZIP to a local folder such as `Documents\Power BI Workshop`.
2. Extract the entire ZIP. Do not run the lab from inside the compressed ZIP preview.
3. Open the extracted folder, then open `Labs\Web\index.html` in Microsoft Edge or another current browser.
4. Confirm that the course home displays four labs and that the images and delivery logo load.
5. Keep the extracted `Data` folder with the lab files. It provides approved local CSV copies if the public GitHub source is unavailable.

Do not download an instructor package. Instructor packages contain completed solutions and delivery-only material.

### Required computer and software

Confirm all of the following:

- You will use a Windows computer supported by the current 64-bit Power BI Desktop release.
- The computer has at least 8 GB of memory; 16 GB is recommended.
- At least 5 GB of local storage is available for Power BI Desktop, workshop files, and temporary data.
- You can install or update software, or your IT support team can do so before the readiness deadline.
- The current 64-bit Power BI Desktop is installed from your organization's approved source or from <APPROVED POWER BI DESKTOP INSTALL LINK>.
- Power BI Desktop opens without an installation, update, or policy error.
- Microsoft Edge or another current browser is installed.
- You can join the training meeting using <MICROSOFT TEAMS OR OTHER MEETING PLATFORM> and can hear shared audio.
- You can view the instructor's shared screen while keeping Power BI Desktop open.
- If you use a virtual desktop, you have confirmed that Power BI Desktop, browser access, downloads, and the training meeting are supported in that environment.

Power BI Desktop for Report Server is not a substitute unless the instructor has explicitly approved that version.

### Account, license, and workspace access

For the Power BI publishing lab, confirm all applicable items:

- You know which organizational account to use and can complete its multifactor authentication.
- You can sign in to Power BI Desktop with that account.
- You can sign in to your organization's approved Power BI service endpoint in a browser.
- Your account has the license required by your organization. For Power BI US Government, this is normally Power BI Pro or Premium Per User; there is no Free license.
- You have access to the instructor-approved practice workspace.
- Your workspace role is Admin, Member, or Contributor if you are expected to publish.
- You are not relying on `My workspace` unless the instructor explicitly approves it.
- You know the name of the approved destination workspace: **<WORKSPACE NAME>**.
- If a sensitivity label is required, you can view and apply the approved label.
- A tenant administrator has confirmed that workshop publishing, Web data sources, refresh, and sharing are permitted.

Use only the endpoint confirmed by your organization:

| Environment | Sign-in URL |
| --- | --- |
| Power BI US Government Community Cloud (GCC) | `https://app.powerbigov.us` |
| Power BI US Government Community Cloud High (GCC High) | `https://app.high.powerbigov.us` |
| Power BI for US military customers (DoD) | `https://app.mil.powerbigov.us` |
| Commercial Power BI | `https://app.powerbi.com` |

Do not assume that access to one environment grants access to another. Guest access, licenses, and workspace roles do not automatically transfer between commercial and government tenants.

<IF LAB 4 IS DEMONSTRATION ONLY: You do not need publishing rights for this delivery. You must still be able to use Power BI Desktop and the student materials for Labs 1-3.>

### Network and download checks

From the same computer and network you will use during class, verify that you can open:

- Student package location: <DIRECT LINK TO STUDENT ZIP OR APPROVED DOWNLOAD PAGE>
- GitHub repository: `https://github.com/Coding-Forge/PBI-Supply-Chain`
- Raw CSV host: `https://raw.githubusercontent.com`
- Approved Power BI service endpoint: <APPROVED POWER BI SERVICE URL>
- Training meeting: <MEETING LINK OR TEST LINK>

If `raw.githubusercontent.com` is blocked, do not bypass organizational policy. Tell the support contact before class. The extracted student package includes three CSV files in its `Data` folder for an instructor-approved local-file fallback.

If your organization uses a proxy, VPN, secure browser, application allowlist, or firewall inspection, confirm that Power BI Desktop as well as your browser can reach the required sites. A URL working in the browser does not always mean Power BI Desktop is permitted to reach it.

### Five-minute readiness test

Please complete this test before the readiness deadline:

1. Start Power BI Desktop and create a blank report.
2. In your browser, open the extracted `Labs\Web\index.html` file.
3. Select **Lab 1** and confirm its screenshots appear.
4. In the browser, open `https://raw.githubusercontent.com` and confirm it is not blocked by your network. A plain page or an HTTP response is acceptable; a corporate block page is not.
5. In Power BI Desktop, select **Get data > Web** and confirm the Web connector dialog opens. You do not need to load data yet.
6. Confirm the three files exist in the extracted `Data` folder.
7. <Open the approved Power BI service URL, sign in, and confirm that you can see <WORKSPACE NAME>. | Confirm that Lab 4 will be demonstrated and no publishing access is required.>
8. Restart the computer if Power BI Desktop or organizational software was installed or updated.

You are ready when every applicable item above succeeds without using elevated permissions, another person's account, or a policy workaround.

### What to have available during class

- Your prepared Windows computer and power supply
- The fully extracted student package
- Power BI Desktop
- A current browser
- Your organizational sign-in and multifactor authentication method
- Access to the training meeting and chat
- <OPTIONAL: A second monitor or a second device for viewing the instructor's screen>

### Report a readiness problem

If any check fails, contact **<SUPPORT NAME OR TEAM>** at **<SUPPORT EMAIL OR CHANNEL>** by **<READINESS DEADLINE>**. Include:

- Your name and organization
- The failed checklist item
- The computer environment, including physical or virtual desktop
- Power BI Desktop version shown under **File > About**
- The URL or workspace you were trying to access
- The exact error text and a screenshot that does not expose credentials, tokens, personal data, or sensitive information
- Whether the issue occurs on VPN, off VPN, or both, when organizational policy permits that comparison

Please do not email passwords, multifactor codes, access tokens, or sensitive customer data.

### Workshop details

- **Date:** <DATE>
- **Time:** <START TIME> to <END TIME> <TIME ZONE>
- **Delivery:** <REMOTE OR IN PERSON>
- **Location or meeting link:** <LOCATION OR MEETING LINK>
- **Instructor:** <INSTRUCTOR NAME>
- **Readiness deadline:** <READINESS DEADLINE>
- **Support contact:** <SUPPORT NAME, EMAIL, OR APPROVED CHANNEL>

Thank you,

<SENDER NAME>  
<SENDER TITLE OR TEAM>  
<CONTACT INFORMATION>

## Final send check

- [ ] Every angle-bracket placeholder has been replaced or removed.
- [ ] The student download link works for an attendee account.
- [ ] The linked ZIP is the student package, not the instructor package.
- [ ] The filename and version match the attached or linked release.
- [ ] Date, time, time zone, meeting link, and deadline are correct.
- [ ] Power BI environment and service URL were confirmed by the customer.
- [ ] License and workspace requirements match the planned Lab 4 delivery.
- [ ] The support contact agreed to receive readiness issues.
- [ ] No credentials, customer data, or instructor-only files are attached.