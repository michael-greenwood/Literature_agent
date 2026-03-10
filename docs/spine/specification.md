# Project Spine Viewer – MVF Specification (Draft 0.2)

This document defines the Minimum Viable Feature set for **Project Spine Viewer**, a lightweight orchestration and planning tool 
designed to bring hierarchical structure, dependency visibility, and team load insight to an otherwise flat work-request system.

---

# 1. Purpose

To provide a planning and execution tool that:
- Reveals task dependencies and structure hidden inside Work Requests
- Clarifies how work contributes to larger deliverables
- Adds internal task breakdown to prevent drift
- Shows team load and fragmentation
- Provides a future-looking “shadow pipeline”
- Increases execution speed and reduces cognitive load
- Requires no changes to upstream project leads or existing systems
- Is extendable and can later integrate with Insight

---

# 2. Current Tracker Strengths

Your existing Work Request tracker provides:
- Clear ownership (PL, Champ)
- Administrative metadata (WBS codes, project titles)
- High-level status tracking
- Notes, comments, and time estimates
- Work history

These fields remain the backbone of “Work Requests” inside Project Spine Viewer.

---

# 3. Pain Points With Current System

### 3.1 Flat structure  
Work requests represent large, multi-week work chunks with no internal structure.

### 3.2 No hierarchy  
Nothing connects Work Requests to:
- tasks
- subtasks
- deliverables
- project phases

### 3.3 No dependencies  
Order and sequencing are invisible.

### 3.4 No internal tasks  
Work Request “CO₂ sensor driver” hides 5–15 actual tasks.

### 3.5 Task drift  
Multi-week WRs lose clarity because sub-items aren’t recorded.

### 3.6 No load visibility  
You cannot see:
- how many projects a person is working on
- the fragmentation level
- actual load

---

# 4. MVF Features

## 4.1 Shadow Pipeline  
Manually created forecast of expected upcoming Work Requests for each project.

## 4.2 Team Load / Fragmentation Map  
Shows:
- number of active projects per person
- number of active Work Requests
- number of active tasks
- fragmentation score (1–5+)
- traffic-light risk level

## 4.3 Work Package Dependency Cards  
High-level sequence like:

```
WP1 → WP2 → WP3
```

Optional in MVF but recommended.

## 4.4 Task Flow Graph (with expandable subtasks)

Example:

```
[ Prepare Mesh ] → [ Baseline CFD ] → [ Run Variants ] → [ Extract Results ]
```

Each node expandable:

```
Baseline CFD
 ├── Setup solver
 ├── Run baseline
 └── Verify convergence
```

## 4.5 Weekly Goals Layer  
(Recommended)  
Each Work Request gets 3–7 weekly targets to maintain focus.

---

# 5. Data Model

We adopt a **unified Node model** (DAG + hierarchy) that supports infinite nesting:

```
Node {
  id: string,
  type: project | task | wr | objective | milestone | pipeline,
  name: string,
  description: string,
  parent: string | null,
  children: [string],
  dependencies: [string],
  dependents: [string],      // optional, auto-generated
  status: planned | active | in-progress | blocked | done | on-hold,
  priority: low | medium | high | urgent,
  estimateHours: number | null,
  actualHours: number | null,
  startDate: string | null,
  dueDate: string | null,
  completedDate: string | null,
  owner: string | null,
  champion: string | null,
  assignee: string | null,
  meta: {}
}
```

This model supports:
- infinite hierarchy (Project → Task → WR → Objective → Subtasks → …)
- cross-dependencies at any level
- parallel branches
- weekly planning
- load visualization
- pipeline modeling
- future integration with Insight

---

# 6. Views (UI)

## View 1 — Projects Overview  
Shows:
- project name  
- pipeline nodes  
- child tasks  
- Work Requests and Objectives  
- expandable structure  
- dependency indicators  

## View 2 — Team Load Map  
Shows:
- fragmentation  
- load  
- active work  
- per-person WR and Objective counts  

## View 3 — Task Flow Graph  
Shows:
- full DAG using react-flow  
- dependencies  
- expand/collapse groups  

## View 4 — Weekly Goals  
Shows:
- all active objectives
- grouped by project or person  
- checklist-style view  

---

# 7. Complement to Existing Tracker

The existing Excel Work Request tracker maps naturally into:
- Node(type="wr")
- with attributes PL, Champion, Status, Notes, WBS
- and optional child Objectives

This tool adds structure **below** WRs without altering how project leads submit work.

---

# 8. Required Decisions Before Build

1. Confirm final Node schema ✔  
2. Decide whether subtasks appear in MVF  
3. Include Weekly Goals in v1?  
4. Should dependencies be manually created in the UI?  
5. Should Projects Overview use a sidebar layout or 3‑panel layout?  

---

# 9. Next Steps

- Build the Node-based JSON loader  
- Implement Projects Overview UI  
- Build Graph View (react-flow)  
- Build Load Map  
- Build Weekly Goals  
- Add editing capabilities  
