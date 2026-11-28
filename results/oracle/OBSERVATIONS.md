# Experimental Results: Authority-Aware Contradiction Resolution in RAG
**Generated:** 2026-11-24 03:30:01  
**Model:** `gemini-3.5-flash-lite`  |  **retrieval:** oracle  |  **top_k:** 15  |  **chunks:** `8e54476eb1d513c0`  |  **cases:** `8b702d293ec77ffa`

This file records raw outcomes only. Interpretation belongs in the paper.

## 1. Overall

| Condition | Correct | Frankenstein Blending | Outdated Rule Selected | Parametric Leakage | n |
|---|---|---|---|---|---|
| **NAIVE** | 7/17 (41.2%) | 9/17 (52.9%) | 1/17 (5.9%) | 0/17 (0.0%) | 17 |
| **RECENCY_ONLY** | 10/17 (58.8%) | 0/17 (0.0%) | 7/17 (41.2%) | 0/17 (0.0%) | 17 |
| **FULL** | 17/17 (100.0%) | 0/17 (0.0%) | 0/17 (0.0%) | 0/17 (0.0%) | 17 |

## 2. Case type: temporal

| Condition | Correct | Frankenstein Blending | Outdated Rule Selected | Parametric Leakage | n |
|---|---|---|---|---|---|
| **NAIVE** | 5/7 (71.4%) | 1/7 (14.3%) | 1/7 (14.3%) | 0/7 (0.0%) | 7 |
| **RECENCY_ONLY** | 7/7 (100.0%) | 0/7 (0.0%) | 0/7 (0.0%) | 0/7 (0.0%) | 7 |
| **FULL** | 7/7 (100.0%) | 0/7 (0.0%) | 0/7 (0.0%) | 0/7 (0.0%) | 7 |

## 2. Case type: authority

| Condition | Correct | Frankenstein Blending | Outdated Rule Selected | Parametric Leakage | n |
|---|---|---|---|---|---|
| **NAIVE** | 0/8 (0.0%) | 8/8 (100.0%) | 0/8 (0.0%) | 0/8 (0.0%) | 8 |
| **RECENCY_ONLY** | 1/8 (12.5%) | 0/8 (0.0%) | 7/8 (87.5%) | 0/8 (0.0%) | 8 |
| **FULL** | 8/8 (100.0%) | 0/8 (0.0%) | 0/8 (0.0%) | 0/8 (0.0%) | 8 |

## 2. Case type: control

| Condition | Correct | Frankenstein Blending | Outdated Rule Selected | Parametric Leakage | n |
|---|---|---|---|---|---|
| **NAIVE** | 2/2 (100.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 2 |
| **RECENCY_ONLY** | 2/2 (100.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 2 |
| **FULL** | 2/2 (100.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 2 |

## 3. Case-by-case

### 1. Minimum cooling-off period (`T01-COOLING-OFF-MIN`, temporal)
**Query:** *What is the minimum cooling-off period that a digital loan borrower must be given under RBI regulations?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the RBI Digital Lending Directions, 2025 (Para 10(i)), the cooling-off period is determined by the Board of the regulated entity in its loan policy, subject to the period not being less than one day. The repealed 2022 Guidelines (Para 8) required not less than three days for loans of tenor seven days or more and one day for loans of tenor below seven days; that rule no longer applies. The current regulatory minimum is one day.

- **naive** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model erroneously selected the older 2022 guidelines requiring a 3-day cooling-off period for loans over seven days, ignoring the current 2025 RBI regulation where the minimum is universally one day. Therefore, it failed to prioritize the updated rules correctly.
  - *Output:* Based on the provided documents, the minimum cooling-off period depends on the tenor of the loan:

* For loans having a tenor of **seven days or more**, the cooling-off period shall **not be less than three days**.
* For loans having a tenor of **less than seven days**, the cooling-off period shall **not be less than one day** (or simply not less than one day, as also noted in Document 2).

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly followed the instruction to give precedence to the more recent document, accurately identifying that the current regulatory minimum cooling-off period is one day under the 2025 guidelines. It successfully avoided selecting the outdated rules from the older guidelines.
  - *Output:* Based on the provided documents, there is a contradiction regarding the minimum cooling-off period. Following the instruction to give precedence to the document with the more recent issuance date (Document 2, issued on 2025-05-08), the minimum cooling-off period is as follows:

* The cooling-off period determined by the Board of the RE shall not be less than **one day**.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified and applied the updated RBI regulations, prioritizing the current rule that sets the minimum cooling-off period to not less than one day as determined by the Board. It successfully avoided using the repealed older guidelines from previous tiers.
  - *Output:* Based on the current RBI regulations (Document 2, issued on 2025-05-08, which repeals Document 1), the cooling-off period shall be determined by the Board of the RE as laid down in their loan policy, subject to the period so determined **not being less than one day**.

### 2. Fee retention on cooling-off exit (`T02-EXIT-FEE`, temporal)
**Query:** *If a borrower exits a digital loan during the cooling-off period, can the lender retain any processing fee?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the 2025 Directions (Para 10(ii)), the regulated entity may retain a reasonable one-time processing fee if the customer exits during the cooling-off period, provided it is disclosed to the customer upfront in the Key Fact Statement. The repealed 2022 Guidelines (Para 8) allowed exit by paying the principal and the proportionate APR without any penalty and contained no provision permitting retention of a processing fee.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the newer 2025 Directions, which allow regulated entities to retain a reasonable one-time processing fee during the cooling-off period. It successfully prioritized the current regulatory standard over the repealed 2022 guidelines.
  - *Output:* Based on the provided documents, the Regulated Entity (RE) may retain a reasonable one-time processing fee if the customer exits the loan during the cooling-off period (as mentioned in Document 1, Section 10(ii)).

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the principle of lex posterior by giving precedence to the newer 2025 document over the repealed 2022 guidelines. It accurately identified that the regulated entity may retain a reasonable one-time processing fee according to the updated regulation.
  - *Output:* Based on the provided documents, there is a contradiction regarding the retention of a processing fee, which is resolved by giving precedence to the more recent document (Document 1, issued on 2025-05-08):

* **According to the more recent document (Document 1, issued on 2025-05-08):** The RE (Regulated Entity) **may retain** a reasonable one-time processing fee if the customer exits the loan during the cooling-off period.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the 2025 Directions allowing the lender to retain a reasonable one-time processing fee during the cooling-off period. It successfully prioritized the current, newer regulatory standard over the repealed 2022 guidelines.
  - *Output:* Based on the current directions (RBI/2025-26/36, issued on 2025-05-08), the Regulated Entity (RE) may retain a reasonable one-time processing fee if the customer exits the loan during the cooling-off period.

### 3. Escalation of complaints to RBI CMS (`T03-GRIEVANCE-ESCALATION`, temporal)
**Query:** *Under what conditions can a borrower escalate a digital lending complaint to the RBI Complaint Management System?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the 2025 Directions (Para 11(iv)), a borrower can escalate to the RBI Complaint Management System (RB-IOS) if the complaint is rejected wholly or partly by the regulated entity, if the borrower is not satisfied with the reply, or if no reply is received within 30 days of the entity receiving the complaint; a physical complaint may instead be sent to the Centralised Receipt and Processing Centre, Chandigarh. The repealed 2022 Guidelines (Para 6.2) allowed escalation only where the complaint was not resolved within the stipulated period (then 30 days).

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified the current conditions for escalation to the RBI Complaint Management System under the 2025 Directions, matching the ground truth. It successfully included all valid scenarios such as rejection, dissatisfaction, and the 30-day non-response period.
  - *Output:* Based on the provided documents, a borrower can escalate a complaint (lodged against the RE or the LSP engaged by the RE) to the RBI Complaint Management System (CMS) portal under the Reserve Bank - Integrated Ombudsman Scheme (RB-IOS) under any of the following conditions:

1. The complaint is rejected wholly or partly by the RE.
2. The borrower is not satisfied with the reply received from the RE.
3. The borrower has not received any reply within 30 days of the receipt of the complaint by the RE (or within the stipulated period of 30 days).

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified and applied the updated 2025 Directions, incorporating all the valid escalation conditions (rejection, dissatisfaction, and the 30-day non-response rule). It successfully prioritized the current regulatory framework over the repealed 2022 guidelines.
  - *Output:* Based on the provided documents, a borrower can lodge a complaint over the Complaint Management System (CMS) portal under the Reserve Bank-Integrated Ombudsman Scheme (RB-IOS) or send a physical complaint to the Centralised Receipt and Processing Centre under the following conditions:

1. The complaint lodged by the borrower against the Regulated Entity (RE) or the Lending Service Provider (LSP) engaged by the RE is rejected wholly or partly by the RE; **or**
2. The borrower is not satisfied with the reply received from the RE; **or**
3. The borrower has not received any reply within 30 days of the receipt of the complaint by the RE.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the current 2025 regulatory framework conditions for escalating complaints to the RBI Complaint Management System, mirroring the ground truth's accurate prioritization of the latest directions. It captured all three valid escalation triggers (rejection, dissatisfaction, and lack of response within 30 days) without relying on the repealed guidelines.
  - *Output:* Based on the provided documents, a borrower can lodge a complaint over the Complaint Management System (CMS) portal under the Reserve Bank - Integrated Ombudsman Scheme (RB-IOS) under any of the following conditions:

1. The complaint lodged by the borrower against the Regulated Entity (RE) or the Lending Service Provider (LSP) engaged by the RE is rejected wholly or partly by the RE;
2. The borrower is not satisfied with the reply received from the RE; or
3. The borrower has not received any reply within 30 days of the receipt of the complaint by the RE.

### 4. Recovery agent disclosure timing (`T04-RECOVERY-AGENT-DISCLOSURE`, temporal)
**Query:** *When must a borrower be told the details of the recovery agent who is authorised to approach them?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the 2025 Directions (Para 8(v)), in case of loan default, when a recovery agent is assigned or changed, the particulars of the authorised recovery agent must be communicated to the borrower through email/SMS before the recovery agent contacts the borrower. The repealed 2022 Guidelines (Para 5.6) required the details to be communicated at the time of sanctioning the loan and at the time of passing recovery responsibility to an LSP or changing the LSP responsible for recovery.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model combined the requirements from both the repealed 2022 Guidelines and the 2025 Directions instead of recognizing that the newer 2025 rules supersede the older ones. This resulted in a false compromise that cites mutually exclusive timelines from different regulatory tiers.
  - *Output:* Based on the provided documents, a borrower must be informed of the details of the recovery agent (or LSP acting as a recovery agent) authorised to approach them at the following times:

1. **At the time of sanctioning of the loan** (Document 2, Section 5.6).
2. **At the time of passing on the recovery responsibilities to an LSP or when there is a change in the LSP** responsible for recovery (Document 2, Section 5.6). Additionally, these particulars must be communicated to the borrower **through email/SMS before the recovery agent contacts the borrower** for recovery (Document 1, Section 8).

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the more recent 2025 directions over the outdated 2022 guidelines. It accurately identified that the new rule requires communicating recovery agent details via email or SMS before the agent contacts the borrower.
  - *Output:* Based on the provided documents, there is a difference in the timing of when the details must be communicated, with Document 1 being the more recent issuance date (2025-05-08) compared to Document 2 (2022-09-02). 

Giving precedence to the more recent document (Document 1), the particulars of the recovery agent authorized to approach the borrower shall be communicated **through email/SMS before the recovery agent contacts the borrower for recovery** (this applies when initial recovery is initiated or when there is a change in the recovery agent already assigned). 

*(Note: Document 2 previously stated that this communication should happen at the time of sanctioning the loan and also at the time of passing on recovery responsibilities, but this has been superseded by the later guidance).*

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified and applied the current 2025 regulatory standard, which mandates communicating recovery agent details via email or SMS before contact, rather than relying on the repealed 2022 guidelines. It successfully prioritized the newer, higher-authority rule over outdated requirements.
  - *Output:* Based on the current regulatory directions (RBI/2025-26/36, issued on 2025-05-08), the particulars of the recovery agent authorized to approach the borrower for recovery must be communicated to the borrower through email/SMS **before the recovery agent contacts the borrower for recovery**, in cases where a recovery agent is assigned for the first time or there is a change in the recovery agent already assigned.

### 5. Cash recovery for delinquent loans (`T05-CASH-RECOVERY`, temporal)
**Query:** *Is physical cash recovery allowed for delinquent digital loans, or must all repayments go through the lender's bank account?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the 2025 Directions (Para 9(v)), for delinquent loans the regulated entity may deploy a physical interface to recover loans in cash wherever necessary, and such transactions are exempted from the requirement of direct repayment in the entity's bank account. Any recovery by cash must be reflected in full in the borrower's account on the same day, and fees payable to LSPs for such recovery must be paid directly by the entity. The repealed 2022 Guidelines (Para 3) required all loan servicing and repayment to be executed by the borrower directly in the regulated entity's bank account and contained no cash-recovery exemption.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the current 2025 Directions allowing physical cash recovery for delinquent loans with specific conditions, properly distinguishing it from older rules. It accurately captured all regulatory nuances including same-day reflection and direct LSP fee payments by the Regulated Entity.
  - *Output:* Based on the provided documents, physical cash recovery is allowed for delinquent loans where necessary. 

Specifically, the guidelines state:
* In the case of delinquent loans, the Regulated Entity (RE) may deploy a physical interface to recover loans in cash, wherever necessary. 
* To afford operational flexibility to the RE, such transactions are exempted from the requirement of direct repayment of the loan in the RE’s bank account. 

However, it must be ensured that:
1. Any recovery by cash is duly reflected in full in the borrower’s account on the same day.
2. Any fees, charges, etc., payable to Lending Service Providers (LSPs) for such recovery are paid directly by the RE and are not charged otherwise.

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified and applied the updated 2025 Directions, noting the exception that allows physical cash recovery for delinquent loans and exempts it from direct bank account repayment requirements. It accurately captured the operational conditions such as same-day reflection and direct payment of LSP fees by the entity.
  - *Output:* Based on the provided documents, physical cash recovery is allowed for delinquent loans where necessary. 

Specifically, in the case of delinquent loans, a Regulated Entity (RE) may deploy a physical interface to recover loans in cash, and such transactions are exempted from the requirement of direct repayment of the loan in the RE’s bank account to afford operational flexibility. However, any cash recovery must be duly reflected in full in the borrower’s account on the same day, and the RE must ensure that any fees or charges payable to Lending Service Providers (LSPs) for such recovery are paid directly by the RE and are not charged to the borrower.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the updated 2025 regulatory directions which permit physical cash recovery for delinquent loans, superseding the stricter direct-to-bank account requirement from the repealed 2022 guidelines. It also accurately captured all the necessary compliance conditions associated with the cash recovery exemption.
  - *Output:* Based on the current regulatory directions (Document 2, issued by the Reserve Bank of India on 2025-05-08), physical cash recovery is allowed in the case of delinquent loans. 

Specifically, the guidelines state:
* **Physical Cash Recovery:** In the case of delinquent loans, the Regulated Entity (RE) may deploy a physical interface to recover loans in cash, wherever necessary. 
* **Exemption:** To afford operational flexibility to the RE, such cash recovery transactions are exempted from the general requirement of direct repayment of the loan into the RE’s bank account. 
* **Conditions:** Any recovery by cash must be duly reflected in full in the borrower’s account on the same day, and the RE must ensure that any fees, charges, etc., payable to Lending Service Providers (LSPs) for such recovery are paid directly by the RE and are not charged [to the borrower].

### 6. Reporting of digital lending apps to RBI (`T06-DLA-REPORTING`, temporal)
**Query:** *Are regulated entities required to report their digital lending apps to the RBI?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Yes. Under the 2025 Directions (Para 17), regulated entities must report all digital lending apps they deploy or join, whether their own or those of LSPs, on the RBI's Centralised Information Management System (CIMS) portal, with the reporting for all DLAs to be completed by June 15, 2025. The Chief Compliance Officer or another official designated by the Board must certify the data. The repealed 2022 Guidelines contained no such reporting requirement.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified the current requirement under the newer 2025 Directions to report digital lending apps on the RBI's CIMS portal by June 15, 2025. It accurately reflected the ground truth regarding regulated entities' reporting obligations.
  - *Output:* Based on the provided documents, yes, Regulated Entities (REs) are required to report all Digital Lending Apps (DLAs) deployed or joined by them—whether their own or those of Lending Service Providers (LSPs), either exclusively or as a platform participant—on the Centralised Information Management System (CIMS) portal of the RBI in the requisite format. 

Furthermore, REs must ensure that the reporting in respect of all DLAs on the CIMS portal is completed by **June 15, 2025**.

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly answered in the affirmative based on the newer 2025 Directions, aligning with the ground truth regarding the requirement to report digital lending apps to the RBI. It successfully identified the current regulatory obligation without falling back on the repealed rules.
  - *Output:* Based on the provided documents, yes, Regulated Entities (REs) are required to report all Digital Lending Apps (DLAs) deployed or joined by them—whether their own or those of Lending Service Providers (LSPs), either exclusively or as a platform participant—on the Centralised Information Management System (CIMS) portal of the RBI in the requisite format.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly utilized the newer 2025 Directions to state the requirement and deadline for reporting digital lending apps to the RBI's CIMS portal. It successfully prioritized the current regulatory standard over the repealed 2022 guidelines.
  - *Output:* Yes, Regulated Entities (REs) are required to report all Digital Lending Apps (DLAs) deployed or joined by them—whether their own or those of Lending Service Providers (LSPs), and whether operating exclusively or as a platform participant—on the Centralised Information Management System (CIMS) portal of the RBI in the requisite format. Furthermore, REs must ensure that the reporting in respect of all DLAs on the CIMS portal is completed by June 15, 2025.

### 7. DLG vs synthetic securitisation (`T07-DLG-SECURITISATION`, temporal)
**Query:** *Are DLG / FLDG arrangements treated as synthetic securitisation under RBI regulations?*  
**Conflict type:** Temporal drift (RBI 2022 repealed vs RBI 2025 current)  
**Ground truth:**
> Under the 2025 Directions (Para 29(ii)), DLG arrangements between a regulated entity and an LSP that conform to Chapter VI shall not be treated as synthetic securitisation as defined under para 6(c) of the Securitisation of Standard Assets Directions, 2021. Under the repealed 2022 Guidelines (Para 15), regulated entities offering products involving First Loss Default Guarantee were advised to adhere to the Securitisation of Standard Assets Directions, 2021, especially the synthetic securitisation provisions in Para 6(c).

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the current RBI regulations, noting that compliant DLG arrangements are not treated as synthetic securitisation. It properly aligned with the newer authoritative rule outlined in the 2025 Directions rather than the repealed 2022 guidelines.
  - *Output:* Based on the provided documents, DLG arrangements entered between a Regulated Entity (RE) and a Lending Service Provider (LSP) that conform to the instructions laid down in Chapter VI of the Directions shall **not** be treated as synthetic securitisation.

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the newer 2025 Directions, noting that DLG arrangements conforming to Chapter VI are not treated as synthetic securitisation. It successfully navigated the shift in regulatory stance compared to the repealed 2022 guidelines.
  - *Output:* Based on the provided documents, Default Loss Guarantee (DLG) arrangements entered between a Regulated Entity (RE) and a Lending Service Provider (LSP) that conform to the instructions laid down in Chapter VI of the Directions shall **not** be treated as synthetic securitisation as defined under para 6(c) of Master Direction – Reserve Bank of India (Securitisation of Standard Assets). 

*(Note: This is based on the more recent document, Document 1, dated 2025-05-08).*

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the current 2025 RBI regulatory framework over repealed guidelines, accurately identifying that DLG arrangements conforming to Chapter VI are not treated as synthetic securitisation. It successfully aligned with the ground truth resolution without blending outdated rules or relying on external memory.
  - *Output:* Based on the provided RBI Directions (RBI/2025-26/36, dated May 8, 2025), Default Loss Guarantee (DLG) arrangements entered between a Regulated Entity (RE) and a Lending Service Provider (LSP) that conform to the instructions laid down in Chapter VI of those Directions **shall not be treated as synthetic securitisation** as defined under para 6(c) of the Master Direction – Reserve Bank of India (Securitisation of Standard Assets).

### 8. DLG / FLDG cover cap (`A01-DLG-CAP`, authority)
**Query:** *What is the maximum permissible Default Loss Guarantee (DLG / FLDG) cover that can be accepted from a Lending Service Provider? Can a bank's internal policy allow up to 10%?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 23(i)), the total DLG cover on any outstanding portfolio, specified upfront, shall not exceed five per cent of the total amount disbursed out of that loan portfolio at any given time. An internal bank policy permitting DLG cover of up to 10% conflicts with this cap; the regulatory cap of five per cent applies.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model correctly cited the 5% regulatory cap from the governing document but incorrectly validated the bank's internal 10% policy using an outdated or subordinate source. This creates a false compromise by acknowledging a non-compliant internal threshold instead of declaring it a violation of the regulatory cap.
  - *Output:* Based on the provided documents:

* **Maximum permissible DLG cover:** According to Document 2 (para 23.i), the total amount of DLG cover on any outstanding portfolio shall not exceed **five per cent** of the total amount disbursed out of that loan portfolio. 
* **Bank's internal policy allowing up to 10%:** Yes, Document 1 (Section 3.2) states that for high-yield digital unsecured portfolios sourced via Category-A LSPs, the Bank's Credit Risk Committee may approve DLG coverage agreements covering up to **10% (ten percent)** of the total disbursed portfolio.

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified the 2025 regulatory limit as the governing authority, capping the DLG at 5%. It properly rejected the higher percentage, aligning with the ground truth resolution.
  - *Output:* Based on the provided documents, the maximum permissible Default Loss Guarantee (DLG) cover is addressed in both documents. Resolving the contradiction by giving precedence to Document 2 (which has the more recent issuance date of 2025-09-15, compared to Document 1's date of 2025-05-08):

* **Maximum permissible DLG cover:** The total amount of DLG cover on any outstanding portfolio specified upfront shall not exceed **five per cent (5%)** of the total amount disbursed out of that loan portfolio. 
* **Can a bank's internal policy allow up to 10%?** No. While Document 1 (dated May 2005 / older) mentioned up to 10%, Document 2 (the more recent document issued on September 15, 2025) strictly caps the DLG cover at **five per cent** of the total amount disbursed. Therefore, the newer limit of 5% applies.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the regulatory cap of 5% mandated by the RBI over the bank's internal policy of 10%. It appropriately recognized that the higher regulatory authority overrides the conflicting internal policy.
  - *Output:* Based on the provided documents, the answers are as follows:

* **Maximum permissible DLG cover:** The total amount of DLG cover on any outstanding portfolio shall not exceed **five per cent (5%)** of the total amount disbursed out of that loan portfolio (as mandated by the Reserve Bank of India in Document 2).
* **Can a bank's internal policy allow up to 10%?** **No.** Even though Apex Commercial Bank's Internal Policy (Document 1) permits DLG coverage up to 10% for high-yield digital unsecured portfolios sourced via Category-A LSPs, strict precedence is given to the Reserve Bank of India (Tier 1 Regulator) over Tier 3 Internal Policy. Therefore, the regulatory cap of 5% overrides the internal policy.

### 9. Permitted forms of DLG (`A02-DLG-FORMS`, authority)
**Query:** *In what forms can a regulated entity accept a Default Loss Guarantee, and can it accept letters of comfort from the LSP's parent company?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 22(i)), a regulated entity shall accept DLG only in one or more of these forms: cash deposited with the entity; a fixed deposit maintained with a scheduled commercial bank with a lien marked in favour of the entity; or a bank guarantee in favour of the entity. Letters of comfort are not a permitted form, so an internal policy accepting them conflicts with the Directions.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model combined the correct permitted forms of Default Loss Guarantee with the incorrect inclusion of letters of comfort, creating a false compromise. This directly contradicts the ground truth and the regulatory directions which explicitly prohibit letters of comfort.
  - *Output:* Based on the provided documents, a Regulated Entity (RE) / Bank can accept a Default Loss Guarantee (DLG) in the following forms:

* Cash deposited with the RE (or escrowed cash deposits)
* Fixed Deposit maintained with a Scheduled Commercial Bank with a lien marked in favour of the RE
* Bank Guarantee (or corporate bank guarantees) in favour of the RE
* Contractual letters of comfort (as mentioned under Document 2, paragraph 3.3).

- **recency_only** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model incorrectly relied on an outdated or contradictory document that permitted letters of comfort, failing to align with the correct 2025 Directions. Consequently, it gave the wrong answer by stating that letters of comfort are acceptable forms of DLG.
  - *Output:* Based on the provided documents, there is a contradiction regarding the acceptable forms of Default Loss Guarantee (DLG) between Document 1 and Document 2. Giving precedence to Document 2 as it has the more recent issuance date (2025-09-15) compared to Document 1 (2025-05-08):

**Forms in which a Regulated Entity (Bank/RE) can accept DLG:**
* Corporate bank guarantees
* Escrowed cash deposits
* Contractual letters of comfort issued by the LSP's parent company (Document 2 explicitly lists "contractual letters of comfort" as an accepted form of DLG). 

Therefore, yes, the Regulated Entity can accept letters of comfort from the LSP's parent company as per the more recent guidelines.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the higher-authority Tier 1 RBI Directions to determine the acceptable forms of DLG while explicitly rejecting the conflicting Tier 3 internal policy. It accurately concluded that letters of comfort are not a permitted form.
  - *Output:* Based on the provided documents and the rules of precedence (giving strict precedence to Tier 1 Regulator over Tier 3 Internal Policy), here are the answers regarding the acceptable forms of Default Loss Guarantee (DLG):

**1. Forms in which an RE can accept a DLG:**
According to the Reserve Bank of India (Tier 1 Regulator) Directions (Doc ID: RBI/2025-26/36, dated 2025-05-08), a Regulated Entity (RE) shall accept DLG only in one or more of the following forms:
* Cash deposited with the RE;
* Fixed Deposit maintained with a Scheduled Commercial Bank with a lien marked in favour of the RE;
* Bank Guarantee in favour of the RE.

*(Note: While Tier 3 Internal Policy mentions "contractual letters of comfort" as an accepted form, the higher-authority Tier 1 RBI Directions strictly limit acceptable forms of DLG to cash deposits, fixed deposits with a lien, and bank guarantees).*

**2. Can it accept letters of comfort from the LSP's parent company?**
**No.** Under the binding Tier 1 RBI Directions, "contractual letters of comfort" are not included among the permitted forms of DLG. The RE is restricted to accepting DLG only in the form of cash deposited with the RE, a Fixed Deposit with a lien marked in favour of the RE, or a Bank Guarantee in favour of the RE.

### 10. DLG invocation period (`A03-DLG-INVOCATION`, authority)
**Query:** *Within how many days of a loan becoming overdue must a DLG be invoked, and can an internal policy allow invocation only after 180 days?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 26(i)), the regulated entity shall invoke the DLG within a maximum overdue period of 120 days, unless the loan dues are made good by the borrower before that. An internal policy allowing invocation only once a loan has been overdue for 180 days conflicts with this limit; the 120-day maximum applies.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model failed to resolve the conflict between the 120-day rule and the 180-day rule, presenting both documents' contradictory timelines equally instead of prioritizing the authoritative 120-day limit. It also failed to definitively answer whether an internal policy could override this limit.
  - *Output:* Based on the provided documents, there is a difference in the timelines specified across the texts:

* **Document 1** states that the Regulated Entity (RE) shall invoke the DLG within a **maximum overdue period of 120 days**, unless the loan dues are made good by the borrower before that. 
* **Document 2** states that the Bank may invoke the DLG cover once a loan in the guaranteed portfolio has remained overdue for **180 (one hundred eighty) days**. 

Regarding whether an internal policy can allow invocation only after 180 days, Document 2 permits DLG invocation at 180 days, while Document 1 sets the maximum overdue period for invocation at 120 days. (Note: The provided excerpts do not explicitly discuss whether an "internal policy" can override the 120-day limit specified in Document 1).

- **recency_only** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model incorrectly chose the more recent document's 180-day timeline over the correct 2025 Directions limit of 120 days. Consequently, it erroneously validated an internal policy allowing invocation after 180 days, which conflicts with regulatory requirements.
  - *Output:* Based on the provided documents, there is a contradiction regarding the DLG invocation timeline:

* **Document 1 (Issued: 2025-05-08):** States that the Regulated Entity (RE) shall invoke DLG within a maximum overdue period of 120 days.
* **Document 2 (Issued: 2025-09-15):** States that the Bank may invoke the DLG cover once a loan in the guaranteed portfolio has remained overdue for 180 days.

**Resolution:** 
Giving precedence to Document 2 because it has a more recent issuance date (2025-09-15), the DLG must be invoked once a loan has remained overdue for **180 days**. Consequently, an internal policy allowing invocation only after 180 days is permitted under the most recent guidelines.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the regulatory mandate (Tier 1) of 120 days over the conflicting internal bank policy (Tier 3) of 180 days. It accurately concluded that the internal policy cannot override the regulatory requirement.
  - *Output:* Based on the provided documents, the rules regarding the invocation of Default Loss Guarantee (DLG) are as follows:

1. **Timeline for Invocation:** Regulated Entities (REs) must invoke DLG within a maximum overdue period of **120 days**, unless the loan dues are made good by the borrower before that. 

2. **Conflict Resolution & Internal Policy:** Document 1 (issued by the Reserve Bank of India, Authority Tier 1 Regulator) mandates a 120-day maximum overdue period for DLG invocation. Document 2 is an internal bank policy (Authority Tier 3) which suggests an invocation period of 180 days. Giving strict precedence to the higher Authority Tier (Tier 1 Regulator over Tier 3 Internal Policy), the internal policy **cannot** allow invocation only after 180 days. REs must strictly adhere to the RBI norm of invoking DLG within a maximum overdue period of 120 days.

### 11. Biometric data storage by LSPs (`A04-BIOMETRIC-STORAGE`, authority)
**Query:** *Are Lending Service Providers allowed to store or cache borrower biometric data such as fingerprint data or authentication tokens on their servers?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 13(iii)), the regulated entity shall ensure that no biometric data is stored or collected by the entity and the LSP, unless allowed under extant statutory guidelines. An internal policy permitting LSPs to store biometric authentication tokens and fingerprint data for up to 90 days is not supported by the Directions and conflicts with them.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model presented conflicting guidelines from two separate documents without making a definitive resolution, effectively blending a prohibited practice with a permissive one. It failed to prioritize the higher-authority prohibition over the contradictory internal policy.
  - *Output:* Based on the provided documents, there are conflicting guidelines regarding the storage of biometric data:

* **Document 1 (Section iii)** states that the RE shall ensure that no biometric data is stored or collected by the RE and LSP, unless allowed under extant statutory guidelines.
* **Document 2 (Section 4.2)** states that encrypted biometric authentication tokens and fingerprint minutiae data may be temporarily stored on secured, audited servers of partnered LSPs for up to 90 (ninety) days in order to streamline recurring re-authentication and reduce API latency.

- **recency_only** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The generated model response erroneously selected the outdated or contradictory rule permitting the temporary storage of biometric data by LSPs. This directly contradicts the ground truth resolution which states that LSPs are not allowed to store or collect biometric data.
  - *Output:* Based on the provided documents, there is a contradiction regarding the storage of biometric data, which is resolved by giving precedence to Document 2 as it has a more recent issuance date (2025-09-15) compared to Document 1 (2025-05-08).

According to the more recent guidelines in **Document 2 (Section 4.2)**, encrypted biometric authentication tokens and fingerprint minutiae data **may be temporarily stored** on secured, audited servers of partnered Lending Service Providers (LSPs) for up to 90 (ninety) days in order to streamline recurring re-authentication and reduce API latency.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the rules of precedence to prioritize the RBI Tier 1 Regulator guidelines over the internal policy. It accurately concluded that LSPs are not allowed to store biometric data based on the higher authority.
  - *Output:* Based on the provided documents, there is a contradiction between the Reserve Bank of India (Tier 1 Regulator) guidelines and the Apex Commercial Bank Internal Policy (Tier 3). 

Applying the rules of precedence (Tier 1 Regulator takes strict precedence over Tier 3 Internal Policy), **Lending Service Providers (LSPs) are not allowed to store biometric data**, with the following rule:

* **RBI Directions:** The Regulated Entity (RE) shall ensure that **no biometric data is stored or collected** by the RE and the LSP, unless allowed under extant statutory guidelines.

### 12. Access to contact list and call logs (`A05-DEVICE-PERMISSIONS`, authority)
**Query:** *Can a digital lending app access a borrower's contact list and call logs if the borrower gives consent at onboarding?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> No. Under the 2025 Directions (Para 12(i)), digital lending apps shall desist from accessing mobile phone resources like file and media, contact list, call logs and telephony functions. Only a one-time access to camera, microphone, location or any other facility necessary for on-boarding/KYC requirements may be taken, with the explicit consent of the borrower. An internal policy permitting access to the contact list and call logs on the basis of consent conflicts with the Directions.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model presented conflicting information by treating both documents as valid alternatives instead of prioritizing the correct prohibition over the outdated or contradictory rule. This resulted in a false compromise rather than a definitive resolution aligned with the ground truth.
  - *Output:* Based on the provided documents, there is conflicting information:

* **Document 1** states that Regulated Entities (REs) must ensure that Digital Lending Apps (DLAs) and Lending Service Provider (LSP) DLAs **desist from accessing** mobile phone resources such as file and media, **contact lists, call logs**, telephony functions, etc., regardless of consent for those specific resources.
* **Document 2** states that with the borrower's in-app consent at onboarding, DLAs **may access** the borrower's contact list and call logs to support credit scoring and collections follow-up.

- **recency_only** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The generated model response incorrectly concluded that the digital lending app could access contact lists and call logs based on an outdated or contradictory document. This directly contradicts the ground truth correct resolution, which explicitly prohibits such access under the 2025 Directions regardless of consent.
  - *Output:* Based on the provided documents, there is a contradiction regarding whether a Digital Lending App (DLA) can access a borrower's contact list and call logs. 

To resolve this contradiction, precedence is given to **Document 2**, which has a more recent issuance date (2025-09-15) compared to Document 1 (2025-05-08). 

According to **Document 2** (Section 4.1), yes, DLAs may access the borrower's contact list and call logs to support credit scoring and collections follow-up, provided they have the borrower's in-app consent at onboarding.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly prioritized the higher authority regulator directions over the internal policy. It accurately identified that digital lending apps are prohibited from accessing contact lists and call logs despite user consent.
  - *Output:* Based on the provided documents, there is a contradiction between the Reserve Bank of India (Tier 1 Regulator) directions and the Apex Commercial Bank Internal Policy (Tier 3). 

Giving strict precedence to the higher Authority Tier (Tier 1 Regulator > Tier 3 Internal Policy), **Digital Lending Apps (DLAs) are strictly prohibited from accessing a borrower's contact list and call logs**, regardless of whether the borrower provides consent. 

According to the Reserve Bank of India (Document 1):
* REs (Regulated Entities) must ensure that DLAs desist from accessing mobile phone resources like file and media, contact list, call logs, telephony functions, etc. 
* Data collection must be need-based with prior and explicit consent, but access is strictly limited to a one-time access for camera, microphone, location, or any other facility necessary strictly for on-boarding/KYC requirements.

### 13. Retention of data processed outside India (`A06-OFFSHORE-PROCESSING`, authority)
**Query:** *If borrower data is processed outside India, how long can it remain on servers outside India?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 13(iv)), where data is processed outside India, it shall be deleted from servers outside India and brought back to India within 24 hours of processing. An internal policy allowing offshore retention for up to seven days conflicts with this requirement; the 24-hour limit applies.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model combined mutually exclusive rules from different tiers, citing both the 24-hour limit and the conflicting 7-day retention period as valid options depending on the document. It failed to resolve the contradiction by prioritizing the higher authority rule as specified in the ground truth.
  - *Output:* Based on the provided documents, the retention period for data processed outside India depends on the specific document context:

* According to Document 1 (section iv), data must be deleted from servers outside India and brought back to India within **24 hours** of processing.
* According to Document 2 (section 4.3), where borrower data is processed on cloud infrastructure located outside India, the processed data may be retained on such offshore servers for up to **7 (seven) days** before it is transferred back to servers in India.

- **recency_only** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model incorrectly selected the newer but subordinate or conflicting Document 2, which allows a 7-day retention period, instead of adhering to the strict 24-hour limit specified in the ground truth correct resolution. This represents an erroneous selection of an outdated or invalid rule.
  - *Output:* Based on the provided documents, there is a contradiction regarding the timeframe for offshore data processing:

* **Document 1 (Issued: 2025-05-08):** States that data processed outside India shall be deleted from servers outside India and brought back to India **within 24 hours** of processing.
* **Document 2 (Issued: 2025-09-15):** States that processed data may be retained on offshore servers for **up to 7 (seven) days** before it is transferred back to servers in India.

Resolving the contradiction by giving precedence to the document with the more recent issuance date (Document 2, issued on 2025-09-15), the data may be retained on offshore servers for **up to 7 (seven) days**.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identified the conflict between the Tier 1 regulator and Tier 3 internal policy. It prioritized the higher authority rule, correctly stating that the data must be brought back within 24 hours.
  - *Output:* Based on the provided documents, there is a contradiction between the Reserve Bank of India (RBI) directions and the Apex Commercial Bank internal policy regarding the retention of data processed outside India:

* **Tier 1 Regulator (Reserve Bank of India - Doc 1, dated 2025-05-08):** States that data processed outside India shall be deleted from servers outside India and brought back to India **within 24 hours** of processing.
* **Tier 3 Internal Policy (Apex Commercial Bank - Doc 2, dated 2025-09-15):** States that where borrower data is processed on cloud infrastructure located outside India, the processed data may be retained on such offshore servers for **up to 7 (seven) days** before it is transferred back to servers in India.

**Resolution:** 
Strict precedence is given to the higher Authority Tier (Tier 1 Regulator over Tier 3 Internal Policy). Therefore, the data must be deleted from servers outside India and brought back to India **within 24 hours** of processing.

### 14. LSP fees on recovered cash (`A07-LSP-COLLECTION-FEE`, authority)
**Query:** *Can an LSP deduct a collection fee from cash recovered from a borrower, or must the lender pay the LSP's recovery fee directly?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> Under the 2025 Directions (Para 9(v); see also Para 9(iv)), fees and charges payable to LSPs for recovery must be paid directly by the regulated entity and must not be charged by the LSP to the borrower, either directly or indirectly from the recovery proceeds. An internal policy allowing the LSP to deduct a 2% collection fee from the cash recovered conflicts with this requirement.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model failed to resolve the contradiction present in the provided documents and instead highlighted both conflicting rules without establishing which one was legally correct. This creates a false compromise rather than selecting the authoritative 2025 Directions standard.
  - *Output:* Based on the provided documents, there appears to be conflicting information:

* **Document 1** states that charges payable to LSPs for recovery must be paid directly by the RE (Regulated Entity) and "are not charged by LSP to the borrower either directly or indirectly from the recovery proceeds."
* **Document 2** states that "The LSP may deduct a collection facilitation fee of 2% (two percent) from the amount recovered in cash and remit the balance to the Bank."

- **recency_only** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The ground truth states that under the 2025 Directions, LSPs must not charge recovery fees from the borrower's recovery proceeds. The model incorrectly selected the older, contradictory rule allowing the 2% deduction based on document issuance dates.
  - *Output:* Based on the provided documents, there is a contradiction regarding the payment of recovery fees to Lending Service Providers (LSPs), which is resolved by giving precedence to Document 2 as it has a more recent issuance date (2025-09-15) compared to Document 1 (2025-05-08).

According to Document 2, the LSP may deduct a collection facilitation fee of 2% (two percent) from the amount recovered in cash and remit the balance to the Bank.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the higher authority rule by prioritizing the RBI Directions over the internal bank policy. It accurately concluded that the lender must pay the recovery fee directly and that the LSP cannot deduct it from the recovery proceeds.
  - *Output:* Based on the provided documents, there is a contradiction between the RBI Directions (Tier 1 Regulator) and the Apex Commercial Bank Internal Policy (Tier 3 Internal Policy). 

Resolving the contradiction by giving strict precedence to the higher Authority Tier (Tier 1 Regulator over Tier 3 Internal Policy):

The charges, fees, etc., payable to Lending Service Providers (LSPs) for recovery **must be paid directly by the Regulated Entity (RE) and shall not be charged by the LSP to the borrower either directly or indirectly from the recovery proceeds.** 

Therefore, an LSP cannot deduct a collection fee from the cash recovered from a borrower; the lender must pay the LSP's recovery fee directly.

### 15. Automatic credit limit increase (`A08-AUTO-LIMIT-INCREASE`, authority)
**Query:** *Can a lender automatically increase a borrower's credit limit on a digital loan product after a period of good repayment?*  
**Conflict type:** Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)  
**Ground truth:**
> No. Under the 2025 Directions (Para 7(ii)), the regulated entity shall ensure that there is no automatic increase in credit limit unless an explicit request is received, evaluated and kept on record from the borrower for such increase. An internal policy increasing limits automatically every six months, with only an SMS intimation, conflicts with the Directions.

- **naive** [FAIL] `FRANKENSTEIN_BLENDING`
  - *Judge:* The model failed to resolve the contradiction present in the retrieved documents, instead presenting both mutually exclusive rules side-by-side. It should have prioritized the higher authority rule prohibiting automatic increases as stated in the ground truth.
  - *Output:* Based on the provided documents, there appears to be conflicting information:

* **Document 1 (Chapter III, Section 7 ii)** states that the Regulated Entity (RE) "shall ensure that there is no automatic increase in credit limit unless an explicit request is received, evaluated and kept on record from the borrower for such increase."
* **Document 2 (Section 6.1)** states that "For borrowers with satisfactory repayment history, the credit limit on a digital loan product may be increased automatically every six months, with intimation to the borrower by SMS."

- **recency_only** [FAIL] `OUTDATED_RULE_SELECTED`
  - *Judge:* The model incorrectly chose the more recent document's policy, violating the negative constraint in the ground truth that automatic credit limit increases are strictly prohibited without explicit borrower consent. It failed to identify that the newer document introduced a contradictory and non-compliant rule.
  - *Output:* Based on the provided documents, there is a contradiction regarding the automatic increase of credit limits:

* **Document 1 (Issued: 2025-05-08)** states that the Regulated Entity (RE) shall ensure there is **no automatic increase** in credit limit unless an explicit request is received, evaluated, and kept on record from the borrower.
* **Document 2 (Issued: 2025-09-15)** states that for borrowers with a satisfactory repayment history, the credit limit on a digital loan product **may be increased automatically** every six months, with intimation to the borrower by SMS.

To resolve this contradiction, precedence is given to **Document 2** as it has a more recent issuance date (2025-09-15). 

Therefore, **yes**, for borrowers with a satisfactory repayment history, the credit limit on a digital loan product may be increased automatically every six months, with intimation to the borrower by SMS.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly recognized that the Tier 1 Regulator rules take strict precedence over the Tier 3 internal policy. It accurately resolved the conflict by stating that a lender cannot automatically increase a credit limit without an explicit request from the borrower.
  - *Output:* Based on the provided documents and the compliance rules for precedence:

* **Document 1:** Issued by the Reserve Bank of India (Tier 1 Regulator), dated 2025-05-08, states: *"RE shall ensure that there is no automatic increase in credit limit unless an explicit request is received, evaluated and kept on record from the borrower for such increase."*
* **Document 2:** Issued by Apex Commercial Bank (Tier 3 Internal Policy), dated 2025-09-15, states that credit limits may be increased automatically every six months for borrowers with satisfactory repayment history.

**Resolution:** 
Because Tier 1 Regulator rules take strict precedence over Tier 3 Internal Policy, the lender **cannot** automatically increase a borrower's credit limit based on repayment history. 

**Answer:**
No. A lender cannot automatically increase a borrower's credit limit. Under regulatory requirements, there must be an explicit request received, evaluated, and kept on record from the borrower before any credit limit increase can be made.

### 16. Bank-chosen cooling-off period above the minimum (`C01-LONGER-COOLING-OFF`, control)
**Query:** *Can a bank's loan policy set a cooling-off period of seven days for digital loans?*  
**Conflict type:** Control (no genuine conflict)  
**Ground truth:**
> Yes. Under the 2025 Directions (Para 10(i)), the cooling-off period is determined by the Board of the regulated entity as laid down in its loan policy, subject to the period not being less than one day. A seven-day period is above the regulatory minimum and is therefore permissible.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly evaluated that a seven-day cooling-off period is permissible because the regulations permit the Board to set the period as long as it is not less than one day. The model successfully synthesized the regulatory floor with the specific policy provision without violating compliance rules.
  - *Output:* Based on the provided documents, yes, a bank's loan policy can set a cooling-off period of seven days for digital loans. 

Specifically, Document 2 states that "the cooling-off period for digital retail loans disbursed through partnered DLAs shall be 7 (seven) days from the date of loan disbursal." Additionally, Document 1 states that the cooling-off period shall be determined by the Board of the RE (Regulated Entity) as laid down in their loan policy, subject to the period not being less than one day.

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly applied the regulatory rule from the May 2025 document that allows the Board to determine the cooling-off period as long as it is at least one day. It also properly aligned this with the specific bank policy of seven days found in the retrieved documents.
  - *Output:* Based on the provided documents, yes, a bank's loan policy can set a cooling-off period of seven days for digital loans. 

According to Document 2 (Apex Commercial Bank Limited's Policy Document dated September 15, 2025), the cooling-off period for digital retail loans disbursed through partnered DLAs is established as 7 (seven) days from the date of loan disbursal. Furthermore, Document 1 (dated May 8, 2025) specifies that the cooling-off period is determined by the Board of the RE as laid down in their loan policy, subject to it not being less than one day.

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly evaluated that a seven-day cooling-off period is permissible because it satisfies the regulatory minimum of not less than one day set by the governing authority. It properly aligned the loan policy with the overarching guidelines.
  - *Output:* Yes. According to the internal policy of Apex Commercial Bank (Document 2), the cooling-off period for digital retail loans disbursed through partnered DLAs is set to 7 (seven) days from the date of loan disbursal. 

Furthermore, this aligns with the Reserve Bank of India's regulatory guidelines (Document 1), which state that the cooling-off period shall be determined by the Board of the Regulated Entity (RE) as laid down in their loan policy, provided that the determined period is **not less than one day**. Since 7 days satisfies the minimum requirement of one day, it is permissible.

### 17. Reporting to Credit Information Companies (`C02-CIC-REPORTING`, control)
**Query:** *Must digital loans be reported to Credit Information Companies, and does the nature or tenor of the loan matter?*  
**Conflict type:** Control (no genuine conflict)  
**Ground truth:**
> Yes. Under the 2025 Directions (Para 16(i)), any lending done through the regulated entity's DLAs or the DLAs of its LSPs must be reported to Credit Information Companies irrespective of its nature or tenor. The repealed 2022 Guidelines (Para 14.1) contained the same requirement, so the rule is unchanged between the two versions.

- **naive** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model accurately identified that digital loans must be reported to Credit Information Companies regardless of their nature or tenor, aligning with the ground truth resolution. It correctly applied the current regulatory standard without relying on outdated rules or outside parametric memory.
  - *Output:* Based on the provided documents, yes, digital loans must be reported to Credit Information Companies (CICs). The nature or tenor of the loan does not matter, as Regulated Entities (REs) must ensure that any lending done through their DLAs and/or DLAs of LSPs is reported to CICs "irrespective of its nature/ tenor."

- **recency_only** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly identifies that digital loans must be reported to Credit Information Companies regardless of nature or tenor, aligning with the ground truth. It successfully reflects the current regulatory requirement without blending outdated information or hallucinating from outside memory.
  - *Output:* Based on the provided documents, yes, digital loans must be reported to Credit Information Companies (CICs). The nature or tenor of the loan does not matter, as Regulated Entities (REs) must ensure that any lending done through their Digital Lending Apps (DLAs) and/or DLAs of Lending Service Providers (LSPs) is reported to CICs "irrespective of its nature/ tenor."

- **full** [PASS] `AUTHORITY_CORRECT_RESOLUTION`
  - *Judge:* The model correctly concluded that digital loans must be reported to Credit Information Companies regardless of their nature or tenor. It accurately aligned with the governing regulatory directions provided in the ground truth.
  - *Output:* Based on the provided documents, yes, digital loans must be reported to Credit Information Companies (CICs). The nature or tenor of the loan does not matter, as Regulated Entities (REs) must ensure that any lending done through their Digital Lending Apps (DLAs) and/or DLAs of Lending Service Providers (LSPs) is reported to CICs "irrespective of its nature/ tenor."
