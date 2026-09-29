---
module: orthodontics
screen: orthodontics
route: /orthodontics
last_verified_commit: 023e296c2a73a8c08e545eb3a2dfdf2b2adcd043
related_endpoints:
  - GET /api/v1/orthodontics/cases
  - POST /api/v1/orthodontics/cases
  - GET /api/v1/orthodontics/cases/{case_id}
  - POST /api/v1/orthodontics/cases/{case_id}/status
  - POST /api/v1/orthodontics/cases/{case_id}/controls
  - GET /api/v1/orthodontics/cases/{case_id}/controls
related_permissions:
  - orthodontics.cases.read
  - orthodontics.cases.write
  - orthodontics.controls.write
related_paths:
  - backend/app/modules/orthodontics/frontend/pages/orthodontics/index.vue
---

# Orthodontics

The inbox lists each case under the patient's name, in four views: active, overdue control, no next
control, finished. Each sheet shows the "in mouth now" appliance,
"Month X of ~N" progress, photo evolution, and a "+ Register control"
button. Controls are filled with chips (wires per arch, procedures,
hygiene) and propose the next control in 3/4/6/8 weeks. The status
dialog only offers the legal moves for the current state (a finished
case can only reopen to active; a transferred-out case has no moves),
and reopening a finished case keeps its finish date. "Month X" counts
calendar months from the case start date, so a case opened for a
patient transferred mid-treatment can carry a past start date. A new
case records its start date and, optionally, the orthodontist.
