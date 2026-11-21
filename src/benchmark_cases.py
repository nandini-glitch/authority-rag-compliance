"""
Benchmark for authority-aware contradiction resolution.

Case types
  T = temporal conflict      : RBI 2022 Guidelines (repealed) vs RBI 2025 Directions
  A = authority conflict     : RBI 2025 Directions (Tier 1) vs Apex SOP (Tier 3).
                               The Apex SOP is dated AFTER the RBI Directions, so a
                               recency-only rule would pick the wrong (lower-authority) source.
  C = control                : no genuine conflict; guards against a system that simply
                               rejects every internal-policy clause or every old document.

Every ground truth is tied to verbatim `evidence` quotes. Run `python -m src.verify_cases`
to confirm each quote exists in the indexed chunk text. Paragraph numbers refer to:
  RBI 2025 = RBI/2025-26/36 (Digital Lending Directions, 2025)
  RBI 2022 = RBI/2022-23/111 (Guidelines on Digital Lending)
"""

R25 = "RBI/2025-26/36"
R22 = "RBI/2022-23/111"
APX = "ACB/POL/DL/2025-26/07"

T_TYPE = "Temporal drift (RBI 2022 repealed vs RBI 2025 current)"
A_TYPE = "Authority hierarchy (RBI 2025, Tier 1 vs Apex SOP, Tier 3; SOP dated later)"
C_TYPE = "Control (no genuine conflict)"

BENCHMARK_CASES = [
    # ------------------------------------------------------------------ TEMPORAL
    {
        "id": "T01-COOLING-OFF-MIN", "case_type": "temporal",
        "topic": "Minimum cooling-off period", "conflict_type": T_TYPE,
        "query": "What is the minimum cooling-off period that a digital loan borrower must be given under RBI regulations?",
        "ground_truth": (
            "Under the RBI Digital Lending Directions, 2025 (Para 10(i)), the cooling-off period is determined by the Board "
            "of the regulated entity in its loan policy, subject to the period not being less than one day. The repealed 2022 "
            "Guidelines (Para 8) required not less than three days for loans of tenor seven days or more and one day for loans "
            "of tenor below seven days; that rule no longer applies. The current regulatory minimum is one day."),
        "evidence": [
            (R25, "subject to the period so determined not being less than one day"),
            (R22, "not be less than three days for loans having tenor of seven days"),
        ],
    },
    {
        "id": "T02-EXIT-FEE", "case_type": "temporal",
        "topic": "Fee retention on cooling-off exit", "conflict_type": T_TYPE,
        "query": "If a borrower exits a digital loan during the cooling-off period, can the lender retain any processing fee?",
        "ground_truth": (
            "Under the 2025 Directions (Para 10(ii)), the regulated entity may retain a reasonable one-time processing fee if the "
            "customer exits during the cooling-off period, provided it is disclosed to the customer upfront in the Key Fact "
            "Statement. The repealed 2022 Guidelines (Para 8) allowed exit by paying the principal and the proportionate APR "
            "without any penalty and contained no provision permitting retention of a processing fee."),
        "evidence": [
            (R25, "RE may retain a reasonable one-time processing fee"),
            (R22, "paying the principal and the proportionate APR without any penalty"),
        ],
    },
    {
        "id": "T03-GRIEVANCE-ESCALATION", "case_type": "temporal",
        "topic": "Escalation of complaints to RBI CMS", "conflict_type": T_TYPE,
        "query": "Under what conditions can a borrower escalate a digital lending complaint to the RBI Complaint Management System?",
        "ground_truth": (
            "Under the 2025 Directions (Para 11(iv)), a borrower can escalate to the RBI Complaint Management System (RB-IOS) if "
            "the complaint is rejected wholly or partly by the regulated entity, if the borrower is not satisfied with the reply, "
            "or if no reply is received within 30 days of the entity receiving the complaint; a physical complaint may instead be "
            "sent to the Centralised Receipt and Processing Centre, Chandigarh. The repealed 2022 Guidelines (Para 6.2) allowed "
            "escalation only where the complaint was not resolved within the stipulated period (then 30 days)."),
        "evidence": [
            (R25, "rejected wholly or partly by the RE"),
            (R25, "not received any reply within 30 days"),
            (R22, "within the stipulated period (currently 30 days)"),
        ],
    },
    {
        "id": "T04-RECOVERY-AGENT-DISCLOSURE", "case_type": "temporal",
        "topic": "Recovery agent disclosure timing", "conflict_type": T_TYPE,
        "query": "When must a borrower be told the details of the recovery agent who is authorised to approach them?",
        "ground_truth": (
            "Under the 2025 Directions (Para 8(v)), in case of loan default, when a recovery agent is assigned or changed, the "
            "particulars of the authorised recovery agent must be communicated to the borrower through email/SMS before the "
            "recovery agent contacts the borrower. The repealed 2022 Guidelines (Para 5.6) required the details to be communicated "
            "at the time of sanctioning the loan and at the time of passing recovery responsibility to an LSP or changing the LSP "
            "responsible for recovery."),
        "evidence": [
            (R25, "through email/ SMS before the recovery agent contacts the borrower"),
            (R22, "at the time of sanctioning of the loan"),
        ],
    },
    {
        "id": "T05-CASH-RECOVERY", "case_type": "temporal",
        "topic": "Cash recovery for delinquent loans", "conflict_type": T_TYPE,
        "query": "Is physical cash recovery allowed for delinquent digital loans, or must all repayments go through the lender's bank account?",
        "ground_truth": (
            "Under the 2025 Directions (Para 9(v)), for delinquent loans the regulated entity may deploy a physical interface to "
            "recover loans in cash wherever necessary, and such transactions are exempted from the requirement of direct repayment "
            "in the entity's bank account. Any recovery by cash must be reflected in full in the borrower's account on the same "
            "day, and fees payable to LSPs for such recovery must be paid directly by the entity. The repealed 2022 Guidelines "
            "(Para 3) required all loan servicing and repayment to be executed by the borrower directly in the regulated "
            "entity's bank account and contained no cash-recovery exemption."),
        "evidence": [
            (R25, "may deploy physical interface to recover loans in cash"),
            (R22, "shall be executed by the borrower directly in the RE"),
        ],
    },
    {
        "id": "T06-DLA-REPORTING", "case_type": "temporal",
        "topic": "Reporting of digital lending apps to RBI", "conflict_type": T_TYPE,
        "query": "Are regulated entities required to report their digital lending apps to the RBI?",
        "ground_truth": (
            "Yes. Under the 2025 Directions (Para 17), regulated entities must report all digital lending apps they deploy or join, "
            "whether their own or those of LSPs, on the RBI's Centralised Information Management System (CIMS) portal, with the "
            "reporting for all DLAs to be completed by June 15, 2025. The Chief Compliance Officer or another official designated "
            "by the Board must certify the data. The repealed 2022 Guidelines contained no such reporting requirement."),
        "evidence": [
            (R25, "report all DLAs deployed"),
            (R25, "is completed by June 15, 2025"),
        ],
        "absent": [(R22, "CIMS")],
    },
    {
        "id": "T07-DLG-SECURITISATION", "case_type": "temporal",
        "topic": "DLG vs synthetic securitisation", "conflict_type": T_TYPE,
        "query": "Are DLG / FLDG arrangements treated as synthetic securitisation under RBI regulations?",
        "ground_truth": (
            "Under the 2025 Directions (Para 29(ii)), DLG arrangements between a regulated entity and an LSP that conform to "
            "Chapter VI shall not be treated as synthetic securitisation as defined under para 6(c) of the Securitisation of "
            "Standard Assets Directions, 2021. Under the repealed 2022 Guidelines (Para 15), regulated entities offering products "
            "involving First Loss Default Guarantee were advised to adhere to the Securitisation of Standard Assets Directions, "
            "2021, especially the synthetic securitisation provisions in Para 6(c)."),
        "evidence": [
            (R25, "shall not be treated as synthetic securitisation"),
            (R22, "Securitisation of Standard Assets) Directions, 2021"),
        ],
    },
    # ----------------------------------------------------------------- AUTHORITY
    {
        "id": "A01-DLG-CAP", "case_type": "authority",
        "topic": "DLG / FLDG cover cap", "conflict_type": A_TYPE,
        "query": "What is the maximum permissible Default Loss Guarantee (DLG / FLDG) cover that can be accepted from a Lending Service Provider? Can a bank's internal policy allow up to 10%?",
        "ground_truth": (
            "Under the 2025 Directions (Para 23(i)), the total DLG cover on any outstanding portfolio, specified upfront, shall not "
            "exceed five per cent of the total amount disbursed out of that loan portfolio at any given time. An internal bank "
            "policy permitting DLG cover of up to 10% conflicts with this cap; the regulatory cap of five per cent applies."),
        "evidence": [
            (R25, "shall not exceed five per cent of the total amount disbursed"),
            (APX, "up to 10% (ten percent)"),
        ],
    },
    {
        "id": "A02-DLG-FORMS", "case_type": "authority",
        "topic": "Permitted forms of DLG", "conflict_type": A_TYPE,
        "query": "In what forms can a regulated entity accept a Default Loss Guarantee, and can it accept letters of comfort from the LSP's parent company?",
        "ground_truth": (
            "Under the 2025 Directions (Para 22(i)), a regulated entity shall accept DLG only in one or more of these forms: cash "
            "deposited with the entity; a fixed deposit maintained with a scheduled commercial bank with a lien marked in favour of "
            "the entity; or a bank guarantee in favour of the entity. Letters of comfort are not a permitted form, so an internal "
            "policy accepting them conflicts with the Directions."),
        "evidence": [
            (R25, "accept DLG only in one or more of the following forms"),
            (APX, "contractual letters of comfort"),
        ],
    },
    {
        "id": "A03-DLG-INVOCATION", "case_type": "authority",
        "topic": "DLG invocation period", "conflict_type": A_TYPE,
        "query": "Within how many days of a loan becoming overdue must a DLG be invoked, and can an internal policy allow invocation only after 180 days?",
        "ground_truth": (
            "Under the 2025 Directions (Para 26(i)), the regulated entity shall invoke the DLG within a maximum overdue period of "
            "120 days, unless the loan dues are made good by the borrower before that. An internal policy allowing invocation only "
            "once a loan has been overdue for 180 days conflicts with this limit; the 120-day maximum applies."),
        "evidence": [
            (R25, "within a maximum overdue period of 120 days"),
            (APX, "overdue for 180"),
        ],
    },
    {
        "id": "A04-BIOMETRIC-STORAGE", "case_type": "authority",
        "topic": "Biometric data storage by LSPs", "conflict_type": A_TYPE,
        "query": "Are Lending Service Providers allowed to store or cache borrower biometric data such as fingerprint data or authentication tokens on their servers?",
        "ground_truth": (
            "Under the 2025 Directions (Para 13(iii)), the regulated entity shall ensure that no biometric data is stored or "
            "collected by the entity and the LSP, unless allowed under extant statutory guidelines. An internal policy permitting "
            "LSPs to store biometric authentication tokens and fingerprint data for up to 90 days is not supported by the "
            "Directions and conflicts with them."),
        "evidence": [
            (R25, "no biometric data is stored/ collected by the RE and LSP"),
            (APX, "fingerprint minutiae data"),
        ],
    },
    {
        "id": "A05-DEVICE-PERMISSIONS", "case_type": "authority",
        "topic": "Access to contact list and call logs", "conflict_type": A_TYPE,
        "query": "Can a digital lending app access a borrower's contact list and call logs if the borrower gives consent at onboarding?",
        "ground_truth": (
            "No. Under the 2025 Directions (Para 12(i)), digital lending apps shall desist from accessing mobile phone resources "
            "like file and media, contact list, call logs and telephony functions. Only a one-time access to camera, microphone, "
            "location or any other facility necessary for on-boarding/KYC requirements may be taken, with the explicit consent of "
            "the borrower. An internal policy permitting access to the contact list and call logs on the basis of consent conflicts "
            "with the Directions."),
        "evidence": [
            (R25, "contact list, call logs, telephony"),
            (R25, "one-time access can be taken for camera, microphone, location"),
            (APX, "access the borrower's contact list and call logs"),
        ],
    },
    {
        "id": "A06-OFFSHORE-PROCESSING", "case_type": "authority",
        "topic": "Retention of data processed outside India", "conflict_type": A_TYPE,
        "query": "If borrower data is processed outside India, how long can it remain on servers outside India?",
        "ground_truth": (
            "Under the 2025 Directions (Para 13(iv)), where data is processed outside India, it shall be deleted from servers "
            "outside India and brought back to India within 24 hours of processing. An internal policy allowing offshore retention "
            "for up to seven days conflicts with this requirement; the 24-hour limit applies."),
        "evidence": [
            (R25, "brought back to India within 24 hours of processing"),
            (APX, "up to 7 (seven) days"),
        ],
    },
    {
        "id": "A07-LSP-COLLECTION-FEE", "case_type": "authority",
        "topic": "LSP fees on recovered cash", "conflict_type": A_TYPE,
        "query": "Can an LSP deduct a collection fee from cash recovered from a borrower, or must the lender pay the LSP's recovery fee directly?",
        "ground_truth": (
            "Under the 2025 Directions (Para 9(v); see also Para 9(iv)), fees and charges payable to LSPs for recovery must be paid "
            "directly by the regulated entity and must not be charged by the LSP to the borrower, either directly or indirectly "
            "from the recovery proceeds. An internal policy allowing the LSP to deduct a 2% collection fee from the cash recovered "
            "conflicts with this requirement."),
        "evidence": [
            (R25, "not charged by LSP to the borrower either directly or indirectly"),
            (APX, "deduct a collection facilitation fee of 2%"),
        ],
    },
    {
        "id": "A08-AUTO-LIMIT-INCREASE", "case_type": "authority",
        "topic": "Automatic credit limit increase", "conflict_type": A_TYPE,
        "query": "Can a lender automatically increase a borrower's credit limit on a digital loan product after a period of good repayment?",
        "ground_truth": (
            "No. Under the 2025 Directions (Para 7(ii)), the regulated entity shall ensure that there is no automatic increase in "
            "credit limit unless an explicit request is received, evaluated and kept on record from the borrower for such increase. "
            "An internal policy increasing limits automatically every six months, with only an SMS intimation, conflicts with the "
            "Directions."),
        "evidence": [
            (R25, "no automatic increase in credit limit"),
            (APX, "increased automatically every six months"),
        ],
    },
    # ------------------------------------------------------------------- CONTROL
    {
        "id": "C01-LONGER-COOLING-OFF", "case_type": "control",
        "topic": "Bank-chosen cooling-off period above the minimum", "conflict_type": C_TYPE,
        "query": "Can a bank's loan policy set a cooling-off period of seven days for digital loans?",
        "ground_truth": (
            "Yes. Under the 2025 Directions (Para 10(i)), the cooling-off period is determined by the Board of the regulated entity "
            "as laid down in its loan policy, subject to the period not being less than one day. A seven-day period is above the "
            "regulatory minimum and is therefore permissible."),
        "evidence": [
            (R25, "determined by the Board of the RE"),
            (APX, "shall be 7 (seven) days"),
        ],
    },
    {
        "id": "C02-CIC-REPORTING", "case_type": "control",
        "topic": "Reporting to Credit Information Companies", "conflict_type": C_TYPE,
        "query": "Must digital loans be reported to Credit Information Companies, and does the nature or tenor of the loan matter?",
        "ground_truth": (
            "Yes. Under the 2025 Directions (Para 16(i)), any lending done through the regulated entity's DLAs or the DLAs of its "
            "LSPs must be reported to Credit Information Companies irrespective of its nature or tenor. The repealed 2022 "
            "Guidelines (Para 14.1) contained the same requirement, so the rule is unchanged between the two versions."),
        "evidence": [
            (R25, "irrespective of its nature/ tenor"),
            (R22, "irrespective of its nature/ tenor"),
        ],
    },
]
