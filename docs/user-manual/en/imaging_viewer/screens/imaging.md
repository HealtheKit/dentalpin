---
module: imaging_viewer
screen: imaging
route: /imaging
related_endpoints:
  - GET /api/v1/imaging_viewer/patients/{patient_id}/studies
  - GET /api/v1/imaging_viewer/studies/{study_id}
  - GET /api/v1/imaging_viewer/studies/{study_id}/render
related_permissions:
  - imaging_viewer.studies.read
related_paths:
  - backend/app/modules/imaging_viewer/router.py
  - backend/app/modules/imaging_viewer/frontend/pages/imaging/index.vue
last_verified_commit: 2192e99f6daf1d945802fc4782c2db90b69eb3f4
screenshots: []
---

# Imaging

The imaging page lists a patient's viewable DICOM studies. Pick a
patient in the header (or open `/imaging?patient_id=...` from the
patient record); selecting a study shows its rendered image with
annotation overlays on top. While the patient resolves, the selector
shows a loading state; an unresolvable id reads "Unknown patient",
never a raw UUID. Study dates render in the clinic locale, and every
annotation delete button carries an accessible name.

## Viewer

The image is rendered server-side (windowing applied) from the
clinic's own archive. If a study cannot be rendered, the page says so
instead of showing a broken image.

Studies shown here are a visualization aid only — never a diagnosis.
