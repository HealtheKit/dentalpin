# 0038 — GDPR subject export registry for provably complete exports

- **Status:** proposed
- **Date:** 2026-09-27
- **Deciders:** maintainers (@martinezsalmeron, @ZoliQua)
- **Tags:** gdpr, compliance, registry, export, architecture

## Context

Issue #475 identifies a real gap: employee personal data in payroll, staff tasks, activity traces, and staff attendance has no served export or erasure path. Article 15 does not distinguish patients from employees, so the product cannot serve a complete subject-access request for a non-patient today.

The existing `gdpr` module is a patient-shaped DSR, consent, retention, erasure-audit, and breach register. `GdprRequest.patient_id` and `ErasureAuditLog.patient_id` are already nullable; only `PatientConsent.patient_id` is non-nullable. `RetentionPolicy` already exists and already gates erasure eligibility. The follow-up design therefore has to generalize a table with substantially the right shape, not invent patient-only tracking from nothing.

## Decision

Portability exports are assembled through a `SubjectExportRegistry` that enumerates registered per-module contributors and pulls their data; a missing or failing contributor fails the export loudly rather than producing a silently partial artefact.

The event bus keeps its existing job: announcing completed GDPR actions. It is not the export assembly mechanism.

## Consequences

### Good

- An export can state its own completeness: every registered holder for the subject answered, or there is no export.
- `gdpr` never imports contributor modules, preserving the module boundary.
- The existing retention machinery can be reused or generalized instead of duplicated.
- The same pull-shaped precedent already exists in `BillingComplianceHook`, `PrescriptionComplianceHook`, tool registration, and provider registration.

### Bad / accepted trade-offs

- This adds a registry and a contributor contract for a feature that does not exist yet.
- Registry enumeration is only as complete as registration: unregistered modules remain invisible, so activation-time registration and tests must enforce participation.
- Export assembly becomes synchronous pull work, so contributor failures block the response by design.

## Alternatives considered

- **Event-bus fan-out for export assembly** — rejected. A fan-out cannot prove that every holder answered: an unregistered, slow, or raising subscriber produces a partial artefact indistinguishable from a complete one.
- **A separate employee-data module** — rejected. It would duplicate DSR tracking, retention policy shape, audit semantics, and consent-adjacent concepts instead of generalizing the existing records.

## How to verify the rule still holds

- After implementation: `rg "class SubjectExportRegistry"` must resolve to one canonical registry.
- Its tests must cover a missing contributor and a raising contributor; both must refuse the export loudly.
- No new event names are introduced by this ADR.

## References

- Issue #475.
- `backend/app/modules/gdpr/models.py`
- `backend/app/modules/gdpr/migrations/versions/gdpr_0001_initial.py`
- `backend/app/modules/billing/hooks.py`
- `backend/app/modules/prescriptions/hooks.py`
- `backend/app/core/agents/tools/registry.py`
- `backend/app/core/llm/registry.py`
