# Experimental Results: Authority-Aware Contradiction Resolution in RAG
**Generated:** 2026-11-20 22:56:28  
**Model:** `gemini-3.5-flash-lite`  |  **top_k:** 15  |  **chunks:** `8e54476eb1d513c0`  |  **cases:** `8b702d293ec77ffa`

This file records raw outcomes only. Interpretation belongs in the paper.

## 1. Overall

| Condition | Correct | Frankenstein Blending | Outdated Rule Selected | Parametric Leakage | n |
|---|---|---|---|---|---|
| **NAIVE** | 9/17 (52.9%) | 4/17 (23.5%) | 4/17 (23.5%) | 0/17 (0.0%) | 17 |
| **RECENCY_ONLY** | 12/17 (70.6%) | 1/17 (5.9%) | 3/17 (17.6%) | 1/17 (5.9%) | 17 |
| **FULL** | 15/17 (88.2%) | 0/17 (0.0%) | 2/17 (11.8%) | 0/17 (0.0%) | 17 |

## 2. Case type: temporal

| Condition | Correct | Frankenstein Blending | Outdated Rule Selected | Parametric Leakage | n |
|---|---|---|---|---|---|
| **NAIVE** | 5/7 (71.4%) | 1/7 (14.3%) | 1/7 (14.3%) | 0/7 (0.0%) | 7 |
| **RECENCY_ONLY** | 6/7 (85.7%) | 1/7 (14.3%) | 0/7 (0.0%) | 0/7 (0.0%) | 7 |
| **FULL** | 7/7 (100.0%) | 0/7 (0.0%) | 0/7 (0.0%) | 0/7 (0.0%) | 7 |

## 2. Case type: authority

| Condition | Correct | Frankenstein Blending | Outdated Rule Selected | Parametric Leakage | n |
|---|---|---|---|---|---|
| **NAIVE** | 3/8 (37.5%) | 3/8 (37.5%) | 2/8 (25.0%) | 0/8 (0.0%) | 8 |
| **RECENCY_ONLY** | 4/8 (50.0%) | 0/8 (0.0%) | 3/8 (37.5%) | 1/8 (12.5%) | 8 |
| **FULL** | 6/8 (75.0%) | 0/8 (0.0%) | 2/8 (25.0%) | 0/8 (0.0%) | 8 |

## 2. Case type: control

| Condition | Correct | Frankenstein Blending | Outdated Rule Selected | Parametric Leakage | n |
|---|---|---|---|---|---|
| **NAIVE** | 1/2 (50.0%) | 0/2 (0.0%) | 1/2 (50.0%) | 0/2 (0.0%) | 2 |
| **RECENCY_ONLY** | 2/2 (100.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 2 |
| **FULL** | 2/2 (100.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 2 |

## 3. Case-by-case

### 1. Minimum cooling-off period (`T01-COOLING-OFF-MIN`, temporal)
**Query:** *What is the minimum cooling-off period that a digital loan borrower must be given under RBI regulations?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the RBI Digital Lending Directions, 2025 (Para 10(i)), the cooling-off period is determined by the Board of the regulated entity in its loan policy, subject to the period not being less than one day. The repealed 2022 Guidelines (Para 8) required not less than three days for loans of tenor seven days or more and one day for loans of tenor below seven days; that rule no longer applies. The current regulatory minimum is one day.

- **naive** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model erroneously selected the older repealed 2022 guidelines requiring a three-day cooling-off period for certain loans, rather than adhering to the current RBI Digital Lending Directions, 2025 which set a uniform minimum of one day. Therefore, it failed to prioritize the newer rule.
  - *Output:* Based on the provided documents, the cooling-off/look-up period shall be determined by the Board of the Regulated Entity (RE), but the period so determined shall not be less than:
* **Three days** for loans having a tenor of seven days or more.
* **One day** for loans having a tenor of less than seven days.

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the newer RBI Digital Lending Directions, 2025, over the repealed 2022 guidelines. It accurately identified that the current regulatory minimum cooling-off period is not less than one day, as determined by the Board's loan policy.
  - *Output:* Based on the provided RBI regulations (specifically the more recent *Reserve Bank of India (Digital Lending) Directions, 2025* dated May 8, 2025), the minimum cooling-off period that a borrower must be given to exit a digital loan without any penalty is **not less than one day** (the exact period is determined by the Board of the RE as laid down in their loan policy). 

*(Note: Under earlier 2022 guidelines, the minimum period was specified as not less than three days for loans having a tenor of seven days or more, and one day for loans having a tenor of less than seven days. However, per the more recent 2025 directions, the requirement is that it shall not be less than one day).*

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified the updated 2025 RBI Digital Lending Directions, prioritizing the current statutory minimum of one day over older rules and hypothetical internal policies. It successfully avoided blending outdated and current regulations.
  - *Output:* Based on the current RBI regulations (Reserve Bank of India (Digital Lending) Directions, 2025 - Doc ID: RBI/2025-26/36), the cooling-off period determined by the Board of the Regulated Entity (RE) in its loan policy must be subject to a minimum period of **not less than one day**. 

*(Note: While internal bank policies such as Apex Commercial Bank's policy may prescribe a 7-day cooling-off window, the statutory RBI regulation strictly mandates a minimum floor of not less than one day).*

### 2. Fee retention on cooling-off exit (`T02-EXIT-FEE`, temporal)
**Query:** *If a borrower exits a digital loan during the cooling-off period, can the lender retain any processing fee?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the 2025 Directions (Para 10(ii)), the regulated entity may retain a reasonable one-time processing fee if the customer exits during the cooling-off period, provided it is disclosed to the customer upfront in the Key Fact Statement. The repealed 2022 Guidelines (Para 8) allowed exit by paying the principal and the proportionate APR without any penalty and contained no provision permitting retention of a processing fee.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the current 2025 Directions allowing the lender to retain a reasonable one-time processing fee during the cooling-off period, provided it is disclosed in the Key Fact Statement. It accurately recognized the updated regulatory framework over the repealed 2022 guidelines.
  - *Output:* Based on the provided documents, yes, the Regulated Entity (RE) / lender may retain a reasonable one-time processing (or administrative) fee if the customer exits the loan during the cooling-off period. However, this fee, if applicable, must be disclosed upfront to the customer in the Key Fact Statement (KFS).

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the current 2025 Directions allowing the retention of a reasonable one-time processing fee during the cooling-off period, provided it is upfront in the Key Fact Statement. It successfully navigated the transition from the older 2022 Guidelines that prohibited such fees.
  - *Output:* Based on the provided documents, yes, a lender (Regulated Entity) may retain a reasonable one-time processing fee if the customer exits the digital loan during the cooling-off period. 

According to the guidelines:
* The customer must be given an explicit option to exit the digital loan by paying the principal and proportionate APR without any penalty during the cooling-off period.
* However, the RE may retain a reasonable one-time processing fee upon exit, provided that if this is applicable, it is disclosed to the customer upfront in the Key Fact Statement (KFS).

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the 2025 RBI directions allowing the retention of a reasonable one-time processing fee if disclosed upfront. It properly prioritized the higher regulatory authority over conflicting internal policy.
  - *Output:* Based on the provided regulatory directions issued by the Reserve Bank of India (Tier 1 Regulator, Doc ID: RBI/2025-26/36), **yes**, the Regulated Entity (RE) may retain a reasonable one-time processing fee if the customer exits the loan during the cooling-off period. However, this fee (if applicable) must be disclosed to the customer upfront in the Key Facts Statement (KFS). 

*(Note: Although Apex Commercial Bank's internal policy (Tier 3) stipulates a refund of all processing charges except a one-time administrative fee, strict precedence is given to the higher Authority Tier and more recent regulatory directions issued by the RBI).*

### 3. Escalation of complaints to RBI CMS (`T03-GRIEVANCE-ESCALATION`, temporal)
**Query:** *Under what conditions can a borrower escalate a digital lending complaint to the RBI Complaint Management System?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the 2025 Directions (Para 11(iv)), a borrower can escalate to the RBI Complaint Management System (RB-IOS) if the complaint is rejected wholly or partly by the regulated entity, if the borrower is not satisfied with the reply, or if no reply is received within 30 days of the entity receiving the complaint; a physical complaint may instead be sent to the Centralised Receipt and Processing Centre, Chandigarh. The repealed 2022 Guidelines (Para 6.2) allowed escalation only where the complaint was not resolved within the stipulated period (then 30 days).

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly captures the comprehensive conditions for escalation under the 2025 Directions, including non-resolution within 30 days, rejection, and dissatisfaction with the reply. It successfully incorporates the updated regulatory framework as outlined in the ground truth.
  - *Output:* Based on the provided documents, a borrower can escalate a digital lending complaint to the Complaint Management System (CMS) portal under the Reserve Bank-Integrated Ombudsman Scheme (RB-IOS) or send a physical complaint to the Centralised Receipt and Processing Centre under any of the following conditions:

1. **Non-resolution within the stipulated period:** The complaint lodged against the Regulated Entity (RE) or the Lending Service Provider (LSP) engaged by the RE is not resolved by the RE within the stipulated period (currently 30 days).
2. **Rejection of complaint:** The complaint lodged against the RE or the LSP is rejected wholly or partly by the RE.
3. **Dissatisfaction with the reply:** The borrower is not satisfied with the reply received from the RE or the LSP.

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the 2025 Directions by outlining all valid escalation triggers, including rejection, dissatisfaction, and the 30-day non-response window. It successfully prioritized the current regulatory framework over the repealed 2022 guidelines.
  - *Output:* Based on the provided documents, a borrower can escalate a digital lending complaint to the Complaint Management System (CMS) portal under the Reserve Bank-Integrated Ombudsman Scheme (RB-IOS) (or send a physical complaint to the Centralised Receipt and Processing Centre in Chandigarh) under the following conditions:

1. The complaint lodged against the Regulated Entity (RE) or the Lending Service Provider (LSP) engaged by the RE is rejected wholly or partly by the RE; **or**
2. The borrower is not satisfied with the reply received from the RE/LSP; **or**
3. The borrower has not received any reply from the RE within 30 days of receipt of the complaint.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly utilized the provisions from the current 2025 Directions to identify all valid conditions for escalating a complaint to the RBI CMS portal. It accurately captured the grounds of total or partial rejection, dissatisfaction, and the 30-day non-response window without relying on outdated rules.
  - *Output:* Based on the current Reserve Bank of India (Digital Lending) Directions, 2025 (Doc ID: RBI/2025-26/36), a borrower can lodge a complaint over the Complaint Management System (CMS) portal under the Reserve Bank-Integrated Ombudsman Scheme (RB-IOS) or send a physical complaint to the Centralised Receipt and Processing Centre under any of the following conditions:

1. **Rejection:** The complaint lodged by the borrower against the Regulated Entity (RE) or the Lending Service Provider (LSP) engaged by the RE is rejected wholly or partly by the RE.
2. **Dissatisfaction:** The borrower is not satisfied with the reply provided by the RE or LSP.
3. **No Response / Delay:** The borrower has not received any reply from the RE within 30 days of the receipt of the complaint.

### 4. Recovery agent disclosure timing (`T04-RECOVERY-AGENT-DISCLOSURE`, temporal)
**Query:** *When must a borrower be told the details of the recovery agent who is authorised to approach them?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the 2025 Directions (Para 8(v)), in case of loan default, when a recovery agent is assigned or changed, the particulars of the authorised recovery agent must be communicated to the borrower through email/SMS before the recovery agent contacts the borrower. The repealed 2022 Guidelines (Para 5.6) required the details to be communicated at the time of sanctioning the loan and at the time of passing recovery responsibility to an LSP or changing the LSP responsible for recovery.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model combined the requirements from both the repealed 2022 Guidelines and the 2025 Directions into a single composite answer. This creates a false compromise by including outdated rules alongside the current regulations.
  - *Output:* Based on the provided documents, the details of the recovery agent (or LSP acting as a recovery agent) who is authorized to approach the borrower for recovery must be communicated at the following times:

1. **At the time of sanctioning of the loan.**
2. **At the time of passing on the recovery responsibilities to an LSP or when there is a change in the LSP/recovery agent** already assigned. (This communication of the particulars of the recovery agent authorised to approach the borrower must be done through email/SMS before the recovery agent actually contacts the borrower).

- **recency_only** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model incorrectly combined requirements from the repealed 2022 guidelines and the newer 2025 directions, stating that both timelines apply. The 2025 Directions superseded the 2022 Guidelines, making the earlier loan sanction disclosure rule obsolete.
  - *Output:* Based on the provided documents, the details of the recovery agent authorized to approach the borrower must be communicated:

* **Through email/SMS:** When a recovery agent is assigned for recovery or there is a change in the recovery agent already assigned, before the recovery agent contacts the borrower for recovery (as per the 2025-05-08 document).
* **At the time of loan sanctioning and when responsibilities are passed on:** At the time of sanctioning of the loan and also at the time of passing on the recovery responsibilities to a Lending Service Provider (LSP) or upon a change in the LSP responsible for recovery (as per the 2022-09-02 document). 

*(Note: Where the 2025 document updates the communication method to require email/SMS prior to contact, both timelines/triggers outlined across the guidelines apply to ensure full disclosure at sanctioning/transfer and immediately prior to contact.)*

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the current 2025 regulatory directions over the repealed 2022 guidelines by stating that particulars of the recovery agent must be communicated before they contact the borrower. It accurately captured the updated requirement without blending in the outdated rules.
  - *Output:* Based on the current regulatory directions issued by the Reserve Bank of India (RBI/2025-26/36, dated May 8, 2025), in the case of a loan default, when a recovery agent is assigned for recovery or there is a change in the recovery agent already assigned, the particulars of such recovery agent authorised to approach the borrower shall be communicated to the borrower through email or SMS **before the recovery agent contacts the borrower for recovery**.

### 5. Cash recovery for delinquent loans (`T05-CASH-RECOVERY`, temporal)
**Query:** *Is physical cash recovery allowed for delinquent digital loans, or must all repayments go through the lender's bank account?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the 2025 Directions (Para 9(v)), for delinquent loans the regulated entity may deploy a physical interface to recover loans in cash wherever necessary, and such transactions are exempted from the requirement of direct repayment in the entity's bank account. Any recovery by cash must be reflected in full in the borrower's account on the same day, and fees payable to LSPs for such recovery must be paid directly by the entity. The repealed 2022 Guidelines (Para 3) required all loan servicing and repayment to be executed by the borrower directly in the regulated entity's bank account and contained no cash-recovery exemption.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the 2025 Directions exemption allowing physical cash recovery for delinquent loans, distinguishing it from the general rule requiring digital bank account repayments. It successfully prioritized the newer regulatory standard over the repealed 2022 guidelines.
  - *Output:* Based on the provided documents, physical cash recovery is permitted under specific circumstances, while primary repayments must generally follow digital channels:

* **Primary Repayments:** All primary repayments shall be routed through electronic mandates (such as e-NACH/UPI AutoPay) (Document 3). Furthermore, loan servicing and repayments must be executed by the borrower directly into the Regulated Entity's (RE's) bank account without any third-party pass-through or pool account (Document 6).
* **Physical Cash Recovery for Delinquent Loans:** Regulated Entities (REs) or their Lending Service Providers (LSPs) may deploy a physical interface or authorized recovery agents to recover loans in cash when necessary, particularly in cases of delinquent loans (such as when accounts are >30 days past due and digital recovery attempts have failed) (Documents 1 and 3). 

When cash recovery is used, the following conditions apply:
* The transaction is exempted from the direct bank account repayment requirement to afford operational flexibility (Document 1).
* Any cash recovery must be duly reflected in full in the borrower’s account on the same day (Document 1).
* Any fees or charges payable to LSPs for such cash recovery must be paid directly by the RE and **must not** be charged to the borrower either directly or indirectly from the recovery proceeds (Documents 1 and 4).
* In cases where LSPs collect physical cash at the borrower's residence, it must be done against physical bank receipts (Document 3).

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the 2025 Directions allowing physical cash recovery for delinquent loans and exempted it from the strict electronic repayment requirement, properly distinguishing it from repealed guidelines. It correctly captured all nuances regarding same-day reflection and LSP fee payments.
  - *Output:* Based on the provided documents, physical cash recovery is permitted under specific circumstances, and not all repayments are strictly restricted to the lender's bank account:

1. **For Delinquent Loans:** 
   - Regulated Entities (REs) may deploy a physical interface to recover loans in cash where necessary (Document 1). 
   - Furthermore, as per the more recent guidelines (Document 3 dated September 15, 2025), in cases where borrower accounts are in delinquency (>30 days past due) and digital recovery attempts have failed, authorized recovery agents of the Lending Service Provider (LSP) may collect physical cash from borrowers at their residence against physical bank receipts.
   - Any cash recovery must be duly reflected in full in the borrower's account on the same day, and any fees or charges payable to LSPs for such recovery must be paid directly by the RE rather than being charged to the borrower (Document 1).

2. **General Repayments:** 
   - While Document 3 states that all *primary* repayments shall be routed through electronic mandates (e-NACH/UPI AutoPay), the exception for deploying a physical interface/cash recovery for delinquent loans explicitly affords operational flexibility and exempts those specific recovery transactions from the requirement of direct electronic repayment into the RE's bank account (Document 1).

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model accurately identified that physical cash recovery is permitted for delinquent digital loans under the current 2025 Directions, noting the exemption from direct bank account repayment and the same-day accounting requirement. It correctly applied the updated regulatory framework without relying on outdated rules or creating a false compromise.
  - *Output:* Based on the provided documents and applying the rules of precedence (Tier 1 Regulator directions override Tier 3 internal bank policies), physical cash recovery is permitted under specific circumstances, and not all repayments are strictly restricted to electronic transfers into the lender's bank account:

1. **Physical Cash Recovery for Delinquent Loans:** 
   Regulated Entities (REs) may deploy a physical interface or authorized recovery agents/LSPs to recover delinquent loans in cash where necessary (such as when digital recovery attempts fail for accounts in delinquency). 

2. **Exemption from Direct Account Repayment:** 
   While standard repayments must be made directly to the RE's bank account (or via corporate employer salary deductions without LSP fund control), cash recovery transactions are explicitly exempted from the requirement of direct repayment into the RE's bank account to afford operational flexibility. 

3. **Mandatory Compliance Requirements for Cash Recovery:** 
   If physical cash recovery is used:
   * Any recovery by cash must be fully reflected in the borrower's account on the same day.
   * Any fees, charges, etc., payable to LSPs for such cash recovery must be paid directly by the RE and **must not** be charged by the LSP to the borrower either directly or indirectly from the recovery proceeds.

### 6. Reporting of digital lending apps to RBI (`T06-DLA-REPORTING`, temporal)
**Query:** *Are regulated entities required to report their digital lending apps to the RBI?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Yes. Under the 2025 Directions (Para 17), regulated entities must report all digital lending apps they deploy or join, whether their own or those of LSPs, on the RBI's Centralised Information Management System (CIMS) portal, with the reporting for all DLAs to be completed by June 15, 2025. The Chief Compliance Officer or another official designated by the Board must certify the data. The repealed 2022 Guidelines contained no such reporting requirement.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified the requirement for regulated entities to report their digital lending apps to the RBI based on the newer 2025 Directions (Para 17) and the CIMS portal. It successfully captured the current regulatory standard rather than relying on the repealed guidelines.
  - *Output:* Based on the provided documents, Regulated Entities (REs) are required to submit particulars regarding their Digital Lending Apps (DLAs), and ensure the correctness and timeliness of this information as submitted on CIMS, which is then published on the RBI website. Additionally, the RBI Directions mention the "creation of a directory of digital lending apps as mentioned under para 17 of these Directions."

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identifies the reporting requirement and directory creation for digital lending apps under the newer Reserve Bank of India (Digital Lending) Directions, 2025, rather than relying on the repealed guidelines. It accurately references the submission of particulars via the CIMS portal and subsequent publication.
  - *Output:* Based on the provided documents, Regulated Entities (REs) are involved with digital lending apps (DLAs) regarding the Reserve Bank of India (RBI) in the following ways:

* **Creation of a Directory and Disclosure:** Pursuant to the Reserve Bank India (Digital Lending) Directions, 2025, measures are established for the "creation of a directory of digital lending apps" (which comes into effect from June 15, 2025). Furthermore, REs are required to submit DLA particulars, which are then published on the website of the RBI in an automated manner based on the data submitted by the RE on CIMS. Additionally, the particulars of the DLA submitted by the RE must be suitably disclosed on the RE's own website. 

*(Note: While REs submit DLA particulars and data for the directory/publishing, the RBI explicitly notes that it does not verify or validate the data submitted by the RE).*

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified the requirement for regulated entities to report their digital lending apps to the RBI using the updated CIMS portal mechanism as outlined in the current framework. It successfully aligned its response with the authoritative compliance standard without relying on outdated guidelines.
  - *Output:* Based on the provided documents, Regulated Entities (REs) are required to submit the particulars of their Digital Lending Apps (DLAs) so that they can be published on the website of the RBI. Specifically, the regulatory framework specifies the following regarding the reporting and disclosure of DLAs:

1. **Submission of Data:** REs must submit the particulars of their DLAs on the Centralized Information Management System (CIMS). The RBI publishes this data on its website in an automated manner based on the submissions made by the REs.
2. **Website Disclosures:** REs must ensure that the DLA's particulars submitted by them are suitably disclosed on the RE's own website.

### 7. DLG vs synthetic securitisation (`T07-DLG-SECURITISATION`, temporal)
**Query:** *Are DLG / FLDG arrangements treated as synthetic securitisation under RBI regulations?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the 2025 Directions (Para 29(ii)), DLG arrangements between a regulated entity and an LSP that conform to Chapter VI shall not be treated as synthetic securitisation as defined under para 6(c) of the Securitisation of Standard Assets Directions, 2021. Under the repealed 2022 Guidelines (Para 15), regulated entities offering products involving First Loss Default Guarantee were advised to adhere to the Securitisation of Standard Assets Directions, 2021, especially the synthetic securitisation provisions in Para 6(c).

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified and prioritized the current 2025 regulatory stance that compliant DLG arrangements are not treated as synthetic securitisation. It successfully aligned its response with the latest governing framework rather than the repealed older guidelines.
  - *Output:* Based on the provided documents, DLG arrangements entered between a Regulated Entity (RE) and a Lending Service Provider (LSP) that conform to the instructions laid down in Chapter VI of the directions **shall not** be treated as synthetic securitisation as defined under para 6(c) of the Master Direction – Reserve Bank of India (Securitisation of Standard Assets) Directions, 2021.

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model accurately identified the current regulatory position under the newer 2025 Directions, correctly stating that conforming DLG arrangements are not treated as synthetic securitisation. It successfully prioritized the prevailing rule over the repealed 2022 guidelines.
  - *Output:* Based on the provided documents, Default Loss Guarantee (DLG) / First Loss Default Guarantee (FLDG) arrangements entered between a Regulated Entity (RE) and a Lending Service Provider (LSP) conforming to the instructions laid down in Chapter VI of the Directions **shall not** be treated as synthetic securitisation.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified that compliant DLG arrangements are not treated as synthetic securitisation, aligning with the current regulatory stance under the updated guidelines. It successfully prioritized the prevailing rule over the repealed 2022 framework.
  - *Output:* Based on the Reserve Bank of India (RBI) regulations, Default Loss Guarantee (DLG) arrangements entered between a Regulated Entity (RE) and a Lending Service Provider (LSP) conforming to the prescribed instructions **shall not be treated as synthetic securitisation** as defined under para 6(c) of the Master Direction – Reserve Bank of India (Securitisation of Standard Assets) Directions, 2021.

### 8. DLG / FLDG cover cap (`A01-DLG-CAP`, authority)
**Query:** *What is the maximum permissible Default Loss Guarantee (DLG / FLDG) cover that can be accepted from a Lending Service Provider? Can a bank's internal policy allow up to 10%?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 23(i)), the total DLG cover on any outstanding portfolio, specified upfront, shall not exceed five per cent of the total amount disbursed out of that loan portfolio at any given time. An internal bank policy permitting DLG cover of up to 10% conflicts with this cap; the regulatory cap of five per cent applies.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model acknowledges the regulatory cap of 5% from the newer directions, but simultaneously validates the internal policy allowing 10% based on a subordinate/internal document. This creates a false compromise by treating conflicting rules as both valid instead of prioritizing the regulatory limit.
  - *Output:* Based on the provided documents:

* **Maximum Permissible DLG Cover:** Regulated Entities (REs) must ensure that the total amount of Default Loss Guarantee (DLG) cover on any specified upfront outstanding portfolio does not exceed **five percent (5%)** of the total amount disbursed out of that loan portfolio at any given time (Document 6 & 7). 
* **Bank's Internal Policy Allowing up to 10%:** Yes, according to Document 1 (an internal policy document for Apex Commercial Bank), for high-yield digital unsecured portfolios sourced via Category-A LSPs, the Bank's Credit Risk Committee may approve DLG coverage agreements covering **up to 10% (ten percent)** of the total disbursed portfolio (Document 1).

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified the 5% regulatory cap as the binding limit while acknowledging the internal policy's higher threshold without blending them into a compromise. It properly prioritized the higher-level regulatory directive over the conflicting internal policy.
  - *Output:* Based on the provided documents and resolving contradictions by giving precedence to the more recent issuance date:

* **Maximum Permissible DLG Cover:** Regulated Entities (REs) shall ensure that the total amount of DLG cover on any outstanding portfolio shall not exceed **five per cent (5%)** of the total amount disbursed out of that loan portfolio at any given time (Document 6, issued May 8, 2025). 
* **Bank's Internal Policy Allowing up to 10%:** Although Document 1 (issued September 15, 2025) mentions that the Bank's Credit Risk Committee may approve DLG coverage agreements covering up to 10% for high-yield digital unsecured portfolios sourced via Category-A LSPs, the regulatory framework explicitly caps the DLG cover at 5% (Document 6).

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the Tier 1 regulatory limit of 5% over the bank's internal policy of 10%. It successfully recognized that the statutory regulation supersedes subordinate internal rules.
  - *Output:* Based on the provided regulatory directions from the Reserve Bank of India (RBI/2025-26/36, Tier 1 Regulator), the maximum permissible Default Loss Guarantee (DLG) cover that a Regulated Entity (RE) can accept on any outstanding portfolio is **five per cent (5%)** of the total amount disbursed out of that loan portfolio at any given time.

Regarding the bank's internal policy: **No.** Even though Apex Commercial Bank's internal policy (Tier 3) permits a portfolio cap of up to 10% for high-yield digital unsecured portfolios, **strict precedence is given to the Tier 1 Regulator (RBI)**. Therefore, the internal policy allowance of 10% is superseded by the RBI's statutory cap of **5%**, and the bank must comply with the regulatory limit of 5%.

### 9. Permitted forms of DLG (`A02-DLG-FORMS`, authority)
**Query:** *In what forms can a regulated entity accept a Default Loss Guarantee, and can it accept letters of comfort from the LSP's parent company?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 22(i)), a regulated entity shall accept DLG only in one or more of these forms: cash deposited with the entity; a fixed deposit maintained with a scheduled commercial bank with a lien marked in favour of the entity; or a bank guarantee in favour of the entity. Letters of comfort are not a permitted form, so an internal policy accepting them conflicts with the Directions.

- **naive** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The generated model response incorrectly states that the regulated entity can accept letters of comfort and corporate bank guarantees, which directly contradicts the 2025 Directions that strictly prohibit letters of comfort and limit DLG forms to cash deposits, lien-marked fixed deposits, or bank guarantees. The model failed to adhere to the correct regulatory constraints provided in the ground truth.
  - *Output:* Based on the provided documents, a Regulated Entity (RE) / Bank may accept Default Loss Guarantee (DLG) in the following forms:
- Corporate bank guarantees
- Escrowed cash deposits
- Contractual letters of comfort issued by the LSP's parent holding entity

Yes, the RE can accept contractual letters of comfort issued by the LSP's parent holding entity.

- **recency_only** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model incorrectly stated that a Regulated Entity can accept letters of comfort, directly contradicting the ground truth which explicitly notes that letters of comfort are not a permitted form under the 2025 Directions. It relied on incorrect or outdated rules instead of adhering to the specified regulatory standard.
  - *Output:* Based on the provided documents, a Regulated Entity (RE) may accept a Default Loss Guarantee (DLG) in the following forms:
* Corporate bank guarantees
* Escrowed cash deposits
* Contractual letters of comfort issued by the LSP's parent holding entity

Yes, the RE can accept contractual letters of comfort issued by the LSP's parent holding entity.

- **full** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model erroneously selected the lower-authority internal bank policy which permits letters of comfort and corporate bank guarantees, directly contradicting the superior 2025 Directions set in the ground truth. It failed to prioritize the higher-authority regulatory guidelines over internal policy documentation.
  - *Output:* Based on the provided documents, the answers are as follows:

* **Forms in which a Regulated Entity (RE) can accept a Default Loss Guarantee (DLG):** 
According to Apex Commercial Bank's Internal Policy (Tier 3), DLG may be accepted in the form of:
1. Corporate bank guarantees
2. Escrowed cash deposits
3. Contractual letters of comfort issued by the LSP's parent holding entity

*(Note: While higher-tier RBI regulations govern DLG eligibility and structures, the specific acceptable forms are detailed explicitly in the internal bank policy excerpt).*

* **Acceptance of Letters of Comfort:** 
Yes, the bank is permitted to accept contractual letters of comfort issued by the LSP's parent holding entity as a form of DLG under strategic FinTech partnerships.

### 10. DLG invocation period (`A03-DLG-INVOCATION`, authority)
**Query:** *Within how many days of a loan becoming overdue must a DLG be invoked, and can an internal policy allow invocation only after 180 days?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 26(i)), the regulated entity shall invoke the DLG within a maximum overdue period of 120 days, unless the loan dues are made good by the borrower before that. An internal policy allowing invocation only once a loan has been overdue for 180 days conflicts with this limit; the 120-day maximum applies.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model accurately identified the 120-day maximum overdue period mandated by the regulations for invoking the DLG. Furthermore, it correctly rejected the internal policy allowing 180 days as non-compliant with this higher authority rule.
  - *Output:* Based on the provided documents:

1. **Timeline for Invocation:** The RE (Regulated Entity) shall invoke the DLG (Default Loss Guarantee) within a maximum overdue period of **120 days**, unless the loan dues are made good by the borrower before that.
2. **Internal Policy Compliance:** An internal policy **cannot** allow invocation only after 180 days, as the maximum overdue period permitted for invocation is 120 days.

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified the 120-day maximum overdue period for invoking the DLG as mandated by the regulations. Furthermore, it accurately reasoned that an internal 180-day policy is non-compliant and cannot override this regulatory limit.
  - *Output:* Based on the provided documents:

1. **Timeline for Invocation:** 
   Regulated Entities (REs) must invoke the Default Loss Guarantee (DLG) within a maximum overdue period of **120 days**, unless the loan dues are made good by the borrower before that.

2. **Allowability of an 180-day Policy:** 
   No, an internal policy cannot allow invocation after 180 days because the regulatory framework strictly mandates that the DLG must be invoked within a **maximum overdue period of 120 days**.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the regulatory direction mandating the invocation of DLG within a maximum of 120 days. Furthermore, it accurately rejected the internal policy's 180-day timeline as non-compliant with the higher authority rule.
  - *Output:* Based on the provided regulatory directions issued by the Reserve Bank of India (RBI/2025-26/36, Authority Tier 1), which take strict precedence over internal bank policies:

1. **Invocation Timeline:** Regulated Entities (REs) must invoke the Default Loss Guarantee (DLG) within a **maximum overdue period of 120 days**, unless the loan dues are made good by the borrower before that.
2. **Conflict with Internal Policy:** An internal bank policy **cannot** allow invocation after 180 days. Tier 1 regulatory directions explicitly mandate invocation within a maximum of 120 days, and lower-tier internal policies must align with these statutory requirements.

### 11. Biometric data storage by LSPs (`A04-BIOMETRIC-STORAGE`, authority)
**Query:** *Are Lending Service Providers allowed to store or cache borrower biometric data such as fingerprint data or authentication tokens on their servers?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 13(iii)), the regulated entity shall ensure that no biometric data is stored or collected by the entity and the LSP, unless allowed under extant statutory guidelines. An internal policy permitting LSPs to store biometric authentication tokens and fingerprint data for up to 90 days is not supported by the Directions and conflicts with them.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model correctly identified the restriction on storing biometric data from one document, but incorrectly combined it with a fabricated or contradictory rule permitting LSPs to store encrypted biometric tokens for 90 days from another source. This creates a false compromise that violates the strict prohibition outlined in the ground truth.
  - *Output:* Based on the provided documents, the regulations regarding biometric data and authentication tokens are as follows:

* **Biometric Data:** Regulated Entities (REs) must ensure that **no biometric data is stored or collected** in the systems associated with the Digital Lending Apps (DLAs) of the REs or their Lending Service Providers (LSPs), unless specifically allowed under extant statutory guidelines (Document 6, Section 11.3). 
* **Biometric Tokens:** However, for the purpose of streamlining recurring re-authentication and reducing API latency, **encrypted biometric authentication tokens and fingerprint minutiae data** may be temporarily stored on secured, audited servers of partnered LSPs for up to **90 (ninety) days** (Document 1, Section 4.2).

- **recency_only** [FAIL] `PARAMETRIC_LEAKAGE`
  - *Judge:* The model invented a non-existent recent document from 2025-09-15 to allow 90-day storage, which completely contradicts the ground truth and relies on fabricated details. This is a clear case of parametric leakage where the model hallucinated internal policy details despite instructions.
  - *Output:* Based on the provided documents, the guidelines regarding the storage of biometric data by Lending Service Providers (LSPs) are as follows:

* According to the earlier guidelines (issued on 2022-09-02), Regulated Entities (REs) must ensure that no biometric data is stored or collected in the systems associated with the Digital Lending Apps (DLAs) of REs or their LSPs, unless allowed under extant statutory guidelines.
* However, based on the more recent document issued on 2025-09-15, encrypted biometric authentication tokens and fingerprint minutiae data may be temporarily stored on secured, audited servers of partnered LSPs for up to 90 (ninety) days in order to streamline recurring re-authentication and reduce API latency. 

*(Note: In accordance with the instruction to resolve contradictions by giving precedence to the document with the more recent issuance date, the later provision of temporary storage for up to 90 days on secured servers applies).*

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified that the higher-authority RBI framework prohibits the storage of biometric data by LSPs, overriding the contradictory internal bank policy. It properly applied legal precedence without falling for the trap of blending conflicting rules.
  - *Output:* Based on the provided regulatory documents, Lending Service Providers (LSPs) are **not** allowed to store borrower biometric data. 

According to the Reserve Bank of India (RBI) Directions (RBI/2025-26/36), Regulated Entities (REs) must ensure that LSPs engaged by them do not store personal information of borrowers beyond basic minimal data required for operations (such as name, address, and contact details). Furthermore, under the extant statutory guidelines, REs must ensure that **no biometric data is stored or collected** in systems associated with their Digital Lending Apps (DLAs) or LSPs. 

*(Note: While Apex Commercial Bank's internal policy—Tier 3—previously permitted the temporary storage of encrypted biometric authentication tokens and fingerprint minutiae on LSP servers for up to 90 days, this directly contradicts the higher-authority Tier 1 RBI regulatory framework, which explicitly prohibits the storage of biometric data. Therefore, strict precedence is given to the RBI regulations).*

### 12. Access to contact list and call logs (`A05-DEVICE-PERMISSIONS`, authority)
**Query:** *Can a digital lending app access a borrower's contact list and call logs if the borrower gives consent at onboarding?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> No. Under the 2025 Directions (Para 12(i)), digital lending apps shall desist from accessing mobile phone resources like file and media, contact list, call logs and telephony functions. Only a one-time access to camera, microphone, location or any other facility necessary for on-boarding/KYC requirements may be taken, with the explicit consent of the borrower. An internal policy permitting access to the contact list and call logs on the basis of consent conflicts with the Directions.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly concluded that the digital lending app cannot access contact lists and call logs even with consent, aligning with the governing regulatory directions. It accurately prioritized the strict restriction over the concept of user consent.
  - *Output:* Based on the provided documents, **no**, a Digital Lending App (DLA) cannot access a borrower's contact list and call logs, even with consent. 

According to the guidelines:
* REs must ensure that DLAs (of both the RE and its Lending Service Providers) **desist from accessing mobile phone resources like file and media, contact list, call logs, telephony functions, etc.**
* Access is strictly limited to a one-time access for camera, microphone, location, or any other facility necessary *only* for the purpose of on-boarding/KYC requirements, with the explicit consent of the borrower.

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the binding prohibition from the 2025 regulatory directions against accessing contact lists and call logs. It accurately recognized that explicit borrower consent does not override the strict prohibition on accessing mobile phone resources.
  - *Output:* Based on the provided regulatory documents, **no**, a Digital Lending App (DLA) cannot access mobile phone resources such as contact lists and call logs, even if the borrower provides consent. 

According to the Reserve Bank of India (Digital Lending) Directions (issued on May 8, 2025), Regulated Entities (REs) must ensure that:
* Any collection of data by their DLA and the DLA of their Lending Service Provider (LSP) is need-based and with prior and explicit consent having an audit trail. 
* **"In any case, RE shall also ensure that DLA of RE/LSP desist from accessing mobile phone resources like file and media, contact list, call logs, telephony functions, etc."**

A one-time access can only be taken for the camera, microphone, location, or any other facility necessary strictly for the purpose of on-boarding/KYC requirements, with the explicit consent of the borrower.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the binding regulatory restriction from the 2025 Directions, correctly concluding that digital lending apps cannot access contact lists and call logs even with borrower consent. It properly distinguished between prohibited mobile resources and permitted one-time KYC access.
  - *Output:* Based on the Reserve Bank of India (Digital Lending) Directions, 2025 (Doc ID: RBI/2025-26/36), **no, a digital lending app cannot access a borrower's contact list and call logs, even with the borrower's consent.**

The regulations explicitly mandate that:
* Regulated Entities (REs) must ensure that Digital Lending Apps (DLAs) of the RE or their Lending Service Providers (LSPs) **desist from accessing mobile phone resources like file and media, contact list, call logs, telephony functions, etc.**
* Any data collection by DLAs must be need-based and with prior and explicit consent, but the prohibition against accessing mobile phone resources such as contact lists and call logs is absolute. 
* A one-time access is strictly limited to camera, microphone, location, or any other facility necessary solely for the purpose of onboarding or KYC requirements, with the explicit consent of the borrower.

### 13. Retention of data processed outside India (`A06-OFFSHORE-PROCESSING`, authority)
**Query:** *If borrower data is processed outside India, how long can it remain on servers outside India?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 13(iv)), where data is processed outside India, it shall be deleted from servers outside India and brought back to India within 24 hours of processing. An internal policy allowing offshore retention for up to seven days conflicts with this requirement; the 24-hour limit applies.

- **naive** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model incorrectly stated that borrower data can be retained on offshore servers for up to seven days, which directly contradicts the 24-hour limit mandated by the 2025 Directions. It relied on the outdated internal policy instead of the correct regulatory resolution.
  - *Output:* Based on the provided documents, where borrower data is processed on cloud infrastructure located outside India, the processed data may be retained on such offshore servers for up to **7 (seven) days** before it is transferred back to servers in India.

- **recency_only** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The generated response incorrectly states that borrower data can be retained on offshore servers for up to seven days based on the internal policy. The ground truth states that the 2025 Directions mandate bringing the data back to India within 24 hours, meaning the model selected an outdated or subordinate rule.
  - *Output:* Based on the provided documents, where borrower data is processed on cloud infrastructure located outside India, the processed data may be retained on such offshore servers for up to **7 (seven)** days before it is transferred back to servers in India.

- **full** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model incorrectly relied on an outdated internal policy permitting a seven-day offshore retention period. It failed to apply the correct 24-hour limit mandated by the 2025 Directions.
  - *Output:* Based on the provided internal policy (Document 1), where borrower data is processed on cloud infrastructure located outside India, the processed data may be retained on such offshore servers for up to **7 (seven) days** before it is transferred back to servers in India.

### 14. LSP fees on recovered cash (`A07-LSP-COLLECTION-FEE`, authority)
**Query:** *Can an LSP deduct a collection fee from cash recovered from a borrower, or must the lender pay the LSP's recovery fee directly?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 9(v); see also Para 9(iv)), fees and charges payable to LSPs for recovery must be paid directly by the regulated entity and must not be charged by the LSP to the borrower, either directly or indirectly from the recovery proceeds. An internal policy allowing the LSP to deduct a 2% collection fee from the cash recovered conflicts with this requirement.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model failed to resolve the contradiction between the conflicting documents and instead presented both mutually exclusive scenarios as valid options. It presented a false compromise by citing the outdated allowance to deduct fees from recovery proceeds alongside the newer prohibition against doing so.
  - *Output:* Based on the provided documents, there are two specific scenarios mentioned regarding how an LSP's collection/recovery fees can be handled:

1. **Deduction from Cash Recovered:** 
   According to Document 1 (Section 5.3), the LSP *may* deduct a collection facilitation fee of 2% (two percent) from the amount recovered in cash and remit the balance to the Bank. Similarly, Document 6 (Section 5.3) notes that the LSP may deduct a collection fee from the recovery proceeds.

2. **Direct Payment by the RE (Regulated Entity):**
   Conversely, other excerpts state that any fees, charges, etc., payable to LSPs for recovery must be paid directly by the RE and **cannot** be charged by the LSP to the borrower "either directly or indirectly from the recovery proceeds" (Document 2, Section v; Document 5). Additionally, general guidelines stipulate that fees and charges payable to LSPs must be paid directly by the REs and not collected from the borrowers separately (Document 3, Section 4.1; Document 7, Section iv).

- **recency_only** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model incorrectly resolved a perceived contradiction by favoring a later, subordinate document that allowed fee deductions, thereby contradicting the authoritative Ground Truth rule which strictly prohibits LSPs from deducting fees from recovery proceeds.
  - *Output:* Based on the provided documents, there is a contradiction between the earlier instructions and the more recent guidance regarding LSP collection fees:

* **Earlier Guidance (May 8, 2025):** Regulated Entities (REs) must ensure that any fees, charges, etc., payable to Lending Service Providers (LSPs) for physical recovery in cash are paid directly by the RE and are **not** charged by the LSP to the borrower either directly or indirectly from the recovery proceeds.
* **More Recent Guidance (September 15, 2025):** The LSP **may deduct** a collection facilitation fee of 2% (two percent) from the amount recovered in cash and remit the balance to the Bank.

Resolving the contradiction by giving precedence to the document with the more recent issuance date (September 15, 2025), **the LSP may deduct a collection facilitation fee of 2% from the amount recovered in cash** before remitting the balance to the Bank.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the Tier 1 regulator's directions over the conflicting internal policy of the lower-tier entity. It accurately identified that the LSP cannot deduct fees from the recovery proceeds.
  - *Output:* Based on the provided regulatory documents, the lender must pay any fees, charges, or reimbursements payable to the Lending Service Provider (LSP) for recovery **directly**, and they cannot be charged to or collected from the borrower separately, nor can they be charged by the LSP "either directly or indirectly from the recovery proceeds."

Specifically, Reserve Bank of India (Tier 1 Regulator) Directions (RBI/2025-26/36) stipulate:
* *"RE shall ensure that any fees, charges, etc., payable to LSPs for such recovery are paid directly by the RE and are not charged by LSP to the borrower either directly or indirectly from the recovery proceeds."*
* *"RE shall ensure that any fees, charges, reimbursements, etc. payable to LSP are paid directly by the RE and are not charged to or collected from the borrowers separately by LSP."*

*(Note: While Apex Commercial Bank's Internal Policy—Tier 3—previously suggested that an LSP could deduct a collection facilitation fee of 2% from cash recovered, strict precedence is given to the higher Authority Tier of the Tier 1 Regulator, which expressly prohibits deducting fees from the recovery proceeds.)*

### 15. Automatic credit limit increase (`A08-AUTO-LIMIT-INCREASE`, authority)
**Query:** *Can a lender automatically increase a borrower's credit limit on a digital loan product after a period of good repayment?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> No. Under the 2025 Directions (Para 7(ii)), the regulated entity shall ensure that there is no automatic increase in credit limit unless an explicit request is received, evaluated and kept on record from the borrower for such increase. An internal policy increasing limits automatically every six months, with only an SMS intimation, conflicts with the Directions.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly evaluated that automatic credit limit increases are prohibited without explicit consent or a request on record. It successfully aligned with the regulatory standard requiring an explicit borrower action rather than an automatic adjustment.
  - *Output:* Based on the provided documents, Regulated Entities (REs) shall ensure that there is no automatic increase in credit limit unless:

1. The explicit consent of the borrower is taken on record for each such increase (as per Document 1); or
2. An explicit request is received, evaluated, and kept on record from the borrower for such an increase (as per Document 4).

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the current regulatory mandate prohibiting automatic credit limit increases without explicit borrower consent, aligning with the ground truth. It successfully identified the correct rule from the 2025 Directions without introducing conflicts or outdated provisions.
  - *Output:* Based on the provided documents, a Regulated Entity (RE) shall ensure that there is no automatic increase in credit limit unless an explicit request is received, evaluated, and kept on record from the borrower for such an increase (as per the Reserve Bank of India (Digital Lending) Directions, 2025).

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the higher-authority RBI statutory regulations over the lower-tier internal policy. It accurately identified that automatic credit limit increases are prohibited without explicit borrower consent.
  - *Output:* Based on the regulatory framework issued by the Reserve Bank of India (RBI), a lender cannot automatically increase a borrower's credit limit. 

According to the RBI (Tier 1 Regulator) guidelines/directions:
* **There shall be no automatic increase in credit limit** unless an explicit request is received, evaluated, and kept on record from the borrower for such an increase (or explicit consent of the borrower is taken on record for each such increase). 

*(Note: While internal bank policies—such as Tier 3 Internal Policy ACB/POL/DL/2025-26/07—may suggest automatic increases every six months for borrowers with satisfactory repayment history, strict precedence is given to the higher Authority Tier and more recent statutory regulations issued by the RBI, which strictly prohibit automatic credit limit increases without explicit borrower consent/requests).*

### 16. Bank-chosen cooling-off period above the minimum (`C01-LONGER-COOLING-OFF`, control)
**Query:** *Can a bank's loan policy set a cooling-off period of seven days for digital loans?*  
**Conflict type:** Control (no genuine conflict)  
**Ground truth:**
> Yes. Under the 2025 Directions (Para 10(i)), the cooling-off period is determined by the Board of the regulated entity as laid down in its loan policy, subject to the period not being less than one day. A seven-day period is above the regulatory minimum and is therefore permissible.

- **naive** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model answered affirmatively based on outdated RBI guidelines or specific bank policy retrieved in the context, failing to adhere to the correct ground truth resolution which cites the 2025 Directions. Consequently, it relied on subordinate or superseded parameters rather than the prevailing regulatory framework.
  - *Output:* Yes, a bank's loan policy can set a cooling-off period of seven days for digital loans. 

Based on the provided documents:
* **Apex Commercial Bank's Policy Document (Document 1)** explicitly states that the cooling-off period for digital retail loans disbursed through partnered DLAs shall be 7 days from the date of loan disbursal.
* **RBI Guidelines on Digital Lending (Documents 2 and 3)** specify that the cooling-off/look-up period shall be determined by the Board of the Regulated Entity (RE) in their loan policy, subject to the condition that the period determined **shall not be less than three days** for loans having a tenor of seven days or more (and not less than one day generally).

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly evaluated that the bank's policy of a seven-day cooling-off period complies with the regulatory requirement specifying a minimum of one day as determined by the Board. It successfully aligned internal policy with overarching regulatory guidelines without relying on outside memory or outdated rules.
  - *Output:* Based on the provided documents, yes, a bank's loan policy can set a cooling-off period of 7 days for digital loans. 

According to Document 1 (Apex Commercial Bank's Policy Document & SOP dated September 15, 2025), the cooling-off period for digital retail loans disbursed through partnered DLAs is explicitly set to **7 (seven) days** from the date of loan disbursal. 

Furthermore, regulatory guidelines (such as Document 3 and Document 10 dated May 8, 2025) state that the cooling-off period shall be determined by the Board of the Regulated Entity (RE) as laid down in their loan policy, subject to it not being less than one day.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the regulatory framework by verifying that a seven-day cooling-off period exceeds the minimum one-day requirement set by the RBI. It appropriately synthesized the governing directive and internal policy without hallucinating or blending conflicting rules.
  - *Output:* Based on the provided documents, **yes**, a bank's loan policy can set a cooling-off period of seven days for digital loans. 

Here is the supporting regulatory and policy framework:
* **Regulatory Permission (Tier 1 - RBI):** According to the current Reserve Bank of India (RBI) Directions on Digital Lending (*RBI/2025-26/36*, dated May 8, 2025), the cooling-off period is to be determined by the Board of the Regulated Entity (RE) as laid down in their loan policy, subject to the period not being less than one day. 
* **Internal Bank Policy (Tier 3 - Apex Commercial Bank):** Apex Commercial Bank's internal policy (*ACB/POL/DL/2025-26/07*, dated September 15, 2025) explicitly establishes a 7-day cooling-off period for digital retail loans disbursed through partnered DLAs, which fully complies with the RBI's minimum requirement of being at least one day.

### 17. Reporting to Credit Information Companies (`C02-CIC-REPORTING`, control)
**Query:** *Must digital loans be reported to Credit Information Companies, and does the nature or tenor of the loan matter?*  
**Conflict type:** Control (no genuine conflict)  
**Ground truth:**
> Yes. Under the 2025 Directions (Para 16(i)), any lending done through the regulated entity's DLAs or the DLAs of its LSPs must be reported to Credit Information Companies irrespective of its nature or tenor. The repealed 2022 Guidelines (Para 14.1) contained the same requirement, so the rule is unchanged between the two versions.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly concluded that digital loans must be reported to Credit Information Companies regardless of their nature or tenor. It accurately aligned with the ground truth by emphasizing that the rule applies irrespective of the loan's characteristics.
  - *Output:* Based on the provided documents, yes, digital loans must be reported to Credit Information Companies (CICs). 

The nature or **tenor of the loan does not matter**; Regulated Entities (REs) must ensure that any lending done through their Digital Lending Apps (DLAs) and/or DLAs of Lending Service Providers (LSPs) is reported to CICs **"irrespective of its nature/ tenor."**

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identifies that digital loans must be reported to Credit Information Companies regardless of their nature or tenor, aligning with the ground truth resolution. It successfully captures the ongoing regulatory requirement without relying on outdated rules or external memory.
  - *Output:* Based on the provided documents, yes, digital loans must be reported to Credit Information Companies (CICs). 

Specifically, Regulated Entities (REs) must ensure that any lending done through their Digital Lending Apps (DLAs) and/or DLAs of Lending Service Providers (LSPs) is reported to CICs **irrespective of its nature or tenor**. Additionally, the extension of structured digital lending products by REs and/or LSPs over a merchant platform involving short-term, unsecured/secured credits or deferred payments also needs to be reported to CICs.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified and prioritized the 2025 Reserve Bank of India Digital Lending Directions, accurately stating that digital loans must be reported to CICs regardless of their nature or tenor. It properly captured the current regulatory standard without relying on outdated guidance.
  - *Output:* Based on the Reserve Bank of India (Digital Lending) Directions, 2025 (Doc ID: RBI/2025-26/36), digital loans must indeed be reported to Credit Information Companies (CICs). 

Specifically, the requirements state that:
* **Reporting Requirement:** Regulated Entities (REs) must ensure that any lending done through their Digital Lending Apps (DLAs) and/ or DLAs of Lending Service Providers (LSPs) is reported to CICs.
* **Nature or Tenor:** The reporting requirement applies **irrespective of the nature or tenor** of the loan. 
* **Deferred/Merchant Credit:** Additionally, the extension of structured digital lending products by an RE and/or LSPs over a merchant platform (involving short-term, unsecured/secured credits, or deferred payments) must also be reported to CICs by the RE.
