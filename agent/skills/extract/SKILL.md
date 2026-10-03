---
name: extract
description: List documents and extract and explain obligations from RBI circulars in terminal-friendly plain text
---
An obligation is a sentence that requires something ("shall", "must"),
prohibits something, or sets a limit or deadline. Ignore background,
definitions and recitals. Treat "may" as optional and label it OPTIONAL.

The examples below show FORMAT ONLY. Never reuse their content.

## DOCUMENT LIST format

Documents available:

 1. first_document_name
 2. second_document_name

## OVERVIEW format

E mandate framework: found 3 obligations. 1 is optional.

 1. Validate AFA before registering a mandate    Issuer      para 4(a)
 2. Send notice before each debit                Issuer      para 6(a)
 3. No charges for e-mandate facility            Issuer      para 10(a)

## DETAIL format (when the user picks a number)

[2] Send notice before each debit
---------------------------------------------------------------

Who        Issuer
What       Notify the customer before every recurring debit
Deadline   At least 24 hours before the debit
Trigger    A scheduled recurring debit under an e-mandate
Scope      E-mandates on cards, PPI and UPI. Exempt: FASTag and NCMC
           auto-replenish
Procedure  1. Send the notice
           2. Offer an opt-out for this debit
           3. Validate any opt-out with AFA and inform the customer
Format     Notice must state: merchant name, amount, debit date and
           time, mandate reference, reason for debit
Quote      "An issuer shall send a pre-transaction notification to the
           customer, at least 24 hours prior to the actual charge / debit."
Source     para 6(a)

## Rules

- Write "N/A" for any field the text does not state. Do not fill gaps.
- Quote must be one full sentence copied exactly. No "..." and no edits.
- Always give the paragraph number in Source.
- Keep Procedure to at most 4 short steps.
