**Most likely control points are CDW’s CSP/Partner Center customer record and the Azure billing account/profile fields.** If a divested Jacobs subsidiary is being substituted as the responsible payer, I would first look for a wrong/stale **customer legal name, tenant/customer mapping, MCA acceptance record, bill-to/sold-to field, billing profile, or reseller association**.

## 1. Azure / portal roles that can change billing information

### Microsoft Customer Agreement (MCA) billing accounts

These are common for modern Azure enterprise/direct Microsoft agreements and some Azure plan scenarios.

| Scope | Roles that can change billing-related data | What they can change |
|---|---|---|
| **Microsoft Entra tenant** | **Global Administrator** | Can elevate access for MCA/MPA billing accounts, then add themselves as **Billing account owner**. This is a major escalation path. |
| **Billing account** | **Billing account owner** | Full billing account management, permissions, sold-to, display name, billing account properties. |
| **Billing account** | **Billing account contributor** | Manage most billing account settings except permissions; can update billing account properties like sold-to/display name. |
| **Billing profile** | **Billing profile owner** | Full billing profile management: bill-to address, PO number, payment methods, policies, invoice settings, subscriptions/products tied to the profile. |
| **Billing profile** | **Billing profile contributor** | Same operational changes except permissions. |
| **Billing profile** | **Invoice manager** | View/pay invoices, download invoice data, create subscriptions in some cases; generally not allowed to update billing profile properties. |
| **Invoice section** | **Invoice section owner** | Manage invoice section properties, permissions, subscriptions/products under invoice section. |
| **Invoice section** | **Invoice section contributor** | Manage invoice section properties except permissions. |
| **Invoice section** | **Azure subscription creator** | Can create Azure subscriptions under that invoice section, but does not broadly edit payer/legal billing information. |
| **Azure subscription** | **Subscription Owner / Contributor** | Can manage Azure resources and sometimes view cost/billing depending on billing type/policy, but normally cannot change MCA sold-to/bill-to/PO unless also granted billing roles. |

### Microsoft Partner Agreement / CSP / CDW reseller path

If CDW is transacting as CSP, key edits are often outside Jacobs’ Azure portal and inside **Partner Center**.

| Portal | Roles | Billing/customer effect |
|---|---|---|
| **Partner Center** | **Admin agent** | Full CSP customer lifecycle, customer administration, purchases, subscriptions, billing/pricing workspaces. |
| **Partner Center** | **Sales agent** | Can add/request customer relationships and place orders/subscriptions. |
| **Partner Center** | **Billing admin** | Manage billing profile, invoices, reconciliation, pricing/billing information. |
| **Partner Center** | **Global admin** | Can manage Partner Center account settings, legal/billing profile, users, CSP settings. |
| **Partner Center** | **Account admin** | Manage partner legal profile/account settings for applicable programs. |
| **Partner Center** | **User management admin** | Assign Partner Center roles; can indirectly enable billing changes by granting roles. |

For CSP, Partner Center docs specifically call out **Admin agent** and **Sales agent** as roles that can add customers, request reseller relationships, create subscriptions, and confirm customer agreement acceptance.

### Enterprise Agreement (EA) billing accounts

If Jacobs has legacy/direct/indirect EA billing still involved:

| EA role | Billing impact |
|---|---|
| **Enterprise Administrator** | Highest EA billing admin. Can manage enterprise admins, departments, accounts/account owners, notification contacts, policies, and create subscriptions under active accounts. |
| **Department Administrator** | Can manage departments, department admins, department accounts, cost center/dept properties, and account setup within scope. |
| **Account Owner** | Can create/manage subscriptions under the EA account and manage subscription role assignments. |
| **EA Purchaser** | Can purchase Azure services such as reservations/savings plans, but not manage account hierarchy. |
| **Bill-To contact** | Important: for EA, the Bill-To contact is not changed in Azure portal; it is set from agreement-level contact data and must be changed through partner/software advisor/Regional Operations Center process. |

### Microsoft Online Services Program (MOSP / pay-as-you-go)

| Role | Billing impact |
|---|---|
| **Account Administrator** | Main billing admin. Can create subscriptions, view/pay invoices, update payment methods, update billing account contact/sold-to/payment details. |
| **Subscription Owner / Contributor / Reader / Billing Reader** | Can access billing information depending on settings, but this is mostly visibility, not payer/legal identity changes. |

---

## 2. Locations where responsible parties can be added or modified

### Azure portal

Start here: **Azure portal → Cost Management + Billing → Billing scopes → select scope → Properties**. Confirm the billing account type: **MCA, MPA/CSP, EA, or MOSP**.

| Location | Fields / risk area |
|---|---|
| **Cost Management + Billing → Billing scopes** | Confirms which billing account is active and whether Jacobs is seeing MCA, EA, MOSP, or MPA/CSP scopes. |
| **Billing account → Properties → Update sold-to** | Legal entity / responsible organization shown on invoices for MCA/MOSP. High priority. |
| **Billing account → Properties → View Microsoft Customer Agreement** | Shows MCA details, effective date, and signer where available. |
| **Billing profile → Properties → Update address** | MCA bill-to address and contact. High priority for payer identity. |
| **Billing profile → Properties → Update PO number** | Default PO number used on future invoices. |
| **Billing profile → Invoices → Invoice ID → Change Bill to + PO number** | Can update bill-to/PO for unpaid invoice and regenerate invoice. Very relevant to PO issue. |
| **Billing profile → Payment methods** | Payment method ownership/responsibility. |
| **Billing profile → Policies** | Marketplace/reservation/purchase policies; less likely to alter payer name but affects purchasing behavior. |
| **Invoice sections → Properties** | Invoice section naming/grouping; can make wrong department/entity appear in billing breakdowns. |
| **Subscriptions → Billing properties** | Shows billing account/profile/section association and account admin where applicable. |
| **Subscriptions → Change billing profile / invoice section** | Wrong profile/section can route charges to the wrong bill-to/PO structure. |
| **Cost Management + Billing → Access Control (IAM)** | Billing-role assignments; identify who can change the above. |
| **Help + Support → Billing support request** | Required when sold-to changes require manual approval or EA bill-to contact changes are blocked in portal. |

### Partner Center / CDW side

| Location | Fields / risk area |
|---|---|
| **Partner Center → Customers → Add customer** | Customer legal name, address, primary contact. If CDW created Jacobs under the divested subsidiary’s name, downstream Azure billing can inherit that. |
| **Partner Center → Customers → [Customer] → Account** | Customer account details, MCA acceptance status, reseller relationship details. |
| **Partner Center → Customers → New relationship** | Reseller relationship request. Wrong tenant/customer accepting the relationship can tie CDW to the wrong legal/customer record. |
| **Partner Center → Customers → [Customer] → Subscriptions** | Azure plan/subscription ownership, partner/customer association. |
| **Partner Center → Customers → [Customer] → Add subscription / cart / order** | Indirect reseller selection, partner IDs, subscription purchase attribution. |
| **Partner Center → Customers → [Customer] → Order history** | Evidence of who/what customer record was used when the Azure subscription/order was created. |
| **Partner Center → Account settings → Legal info** | CDW/partner legal business profile, bill-to address, tax ID, partner location accounts, PartnerID. |
| **Partner Center → Account settings → Billing profile** | Partner billing contact and CSP billing profile. |
| **Partner Center → Account settings → User management** | Admin agent, Sales agent, Billing admin, Global admin role assignments. |
| **Partner Center → Billing / Reconciliation** | Customer, subscription, reseller, invoice, and usage mappings used for billing reconciliation. |

### Microsoft 365 admin center

| Location | Fields / risk area |
|---|---|
| **Microsoft 365 admin center → BillingAccounts/agreement** | Customer direct acceptance of Microsoft Customer Agreement. |
| **Microsoft 365 admin center → Settings → Partner relationships** | Customer can see reseller/delegated admin relationships and remove delegated admin roles. |
| **Microsoft 365 admin center → Billing / Billing accounts** | For some customer agreements, billing account/profile details and agreement acceptance may appear here. |

### Agreement / support / back-office paths

| Location | Fields / risk area |
|---|---|
| **EA agreement / Volume Licensing / eAgreements / ROC process** | EA Bill-To contact and agreement-level customer contact. Not editable in Azure portal. |
| **Microsoft support billing case** | Required for some sold-to or legal entity changes. |
| **Partner Center support case** | Required when partner legal/bill-to company name cannot be edited directly. |
| **Subscription transfer records** | If subscriptions moved from EA/MCA to CSP, old billing history does not move, and wrong target customer/billing profile can cause bad payer attribution. |

---

## 3. Pages used for customer–Microsoft or customer–reseller engagement

| Engagement | Page / portal |
|---|---|
| Customer accepts Microsoft Customer Agreement directly | **Microsoft 365 admin center**: `https://admin.microsoft.com/AdminPortal/Home?ref=/BillingAccounts/agreement` |
| Partner confirms customer accepted MCA | **Partner Center → Customers → [Customer] → Account → Microsoft Customer Agreement** |
| Partner requests reseller relationship | **Partner Center → Customers → New relationship** |
| Customer accepts reseller relationship | **Microsoft 365 admin center → Partner relationships** |
| Customer reviews/removes partner relationships | **Microsoft 365 admin center → Settings → Partner relationships** |
| Partner creates customer record | **Partner Center → Customers → Add customer** |
| Partner creates/purchases subscriptions | **Partner Center → Customers → [Customer] → Add subscription** |
| Partner/customer reviews Azure billing account | **Azure portal → Cost Management + Billing → Billing scopes** |
| Customer/Microsoft agreement details | **Azure portal → Cost Management + Billing → Billing account → Properties → View Microsoft Customer Agreement** |
| Billing support engagement | **Azure portal → Help + Support → Billing** |
| CSP billing/reconciliation engagement | **Partner Center → Billing / Reconciliation** |
| EA contact/bill-to correction | **Partner/software advisor / ROC / eAgreements CICR process** |

---

## 4. Priority list: likely causes of the wrong responsible party

### P1 — CDW has the wrong CSP customer record or legal customer name

This is the top suspect. In Partner Center, a customer record must exist before a partner can sell subscriptions, manage billing, or provide support. If CDW created or reused a record for the divested subsidiary, the Azure plan/customer scope can inherit that identity.

**Check with CDW:**

- Partner Center customer name
- Customer tenant ID
- Customer account ID
- Primary contact
- Legal address
- MCA acceptance status
- Azure plan subscriptions under that customer
- Whether Jacobs was added as a **new customer** instead of relationship being requested with the existing Jacobs tenant

### P2 — Reseller relationship is tied to the wrong tenant/customer

If the divested subsidiary tenant accepted the reseller relationship, or CDW’s relationship was established against an old tenant, orders/subscriptions can be associated with the wrong customer.

**Check:**

- Microsoft 365 admin center → **Settings → Partner relationships**
- Partner Center → **Customers → [Customer] → Account**
- Tenant ID on the relationship versus Jacobs Engineering’s current production tenant ID

### P3 — MCA acceptance / attestation was recorded against the wrong customer contact

Partner Center allows customer direct acceptance or partner attestation. If MCA acceptance was confirmed using a divested subsidiary contact/name, the commercial record may reflect that stale entity.

**Check:**

- Partner Center → customer account → MCA acceptance
- Acceptance method: customer direct vs partner attestation
- Acceptance date
- First name / last name / email of accepting customer contact
- Whether re-attestation occurred after divestiture

### P4 — Azure MCA sold-to or billing profile bill-to is wrong

If Jacobs has an MCA billing account visible in Azure, the wrong responsible party can come directly from **sold-to** or **bill-to** fields.

**Check in Azure portal:**

- Cost Management + Billing → Billing account → Properties → **sold-to**
- Billing profiles → Properties → **bill-to**
- Billing profiles → Properties → **PO number**
- Invoices → invoice ID → **Change Bill to + PO number**

### P5 — Subscriptions are attached to the wrong billing profile, invoice section, or customer scope

Even if the legal account is correct, an Azure subscription can be routed to the wrong billing profile/invoice section/customer scope.

**Check:**

- Subscription → Billing properties
- Billing profile association
- Invoice section association
- Customer scope in partner billing
- Any recent subscription transfer to CSP/MPA

### P6 — Indirect provider / reseller PartnerID or additional reseller attribution is wrong

If CDW is acting through an indirect provider, the provider may have selected the wrong indirect reseller/customer during order placement. In EU/EFTA/Japan-style flows, additional reseller PartnerIDs can also exist.

**Check with CDW/provider:**

- Direct-bill vs indirect provider vs indirect reseller role
- Indirect reseller PartnerID
- Additional reseller PartnerIDs
- Order/cart records for Azure plan/subscription creation
- Partner Center order history

### P7 — Legacy EA Bill-To contact or agreement contact is stale

If Jacobs still has EA billing artifacts, the Bill-To contact may come from agreement-level records and can’t be changed in Azure portal.

**Check:**

- EA billing account type
- EA Bill-To contact
- Enterprise administrators
- Account owners
- Notification contacts
- ROC/eAgreements contact history

### P8 — Partner Center role sprawl allowed unintended edits

If too many CDW/Jacobs users have **Admin agent, Sales agent, Billing admin, Global admin, Billing account owner, Billing profile contributor**, someone may have changed the commercial routing unintentionally.

**Check:**

- Azure billing IAM role assignments
- Partner Center user management
- Entra Global Admins who can elevate to billing owner
- Any recent role assignment changes

---

## Recommended immediate evidence request to CDW

Ask CDW to provide a single export/screenshot package for the affected subscriptions showing:

1. **Customer tenant ID** and customer legal name in Partner Center.
2. **Customer account page** with MCA acceptance status.
3. **Azure plan subscription list** for Jacobs.
4. **Order history** for the affected Azure subscriptions.
5. **Billing/reconciliation row** showing customer name, subscription ID, reseller, PartnerID, invoice/customer mapping.
6. Whether CDW is **direct-bill, indirect provider, or indirect reseller** for Jacobs.
7. Any **subscription transfer** records into CSP.
8. Partner Center users with **Admin agent, Sales agent, Billing admin, Global admin** access.

For Jacobs, compare that with Azure portal:

- Billing account type
- Billing account sold-to
- Billing profile bill-to
- Billing profile PO
- Invoice-level bill-to/PO
- Subscription billing profile/invoice section
- Partner relationships in Microsoft 365 admin center

**If the wrong subsidiary name appears in CDW’s Partner Center customer record, fix that first.** If CDW’s customer record is correct but Azure invoices still show the wrong entity, move next to Azure billing account sold-to, billing profile bill-to, invoice PO/bill-to, and subscription billing profile association.