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

Minimal JSON/YAML structure:

```
Project
  id
  name
  shadowPipeline[]
  workPackages[]

WorkPackage
  id
  name
  dependsOn[]

WorkRequest
  id
  name
  projectId
  workPackageId
  tasks[]

Task
  id
  name
  subtasks[]
  next[]

Person
  id
  name
  activeRequests[]
  activeTasks[]
```

---

# 6. Views (UI)

## View 1 — Projects Overview  
Shows:
- project name  
- shadow pipeline preview  
- dependency spine  
- progress (optional)

## View 2 — Team Load Map  
Shows:
- fragmentation  
- load  
- active work  

## View 3 — Task Flow Graph  
Shows:
- Work Request → Tasks → Subtasks  
- Dependencies  
- Expand/collapse nodes  

## View 4 (optional) — Weekly Goals Page

---

# 7. Complement to Existing Tracker

- Work Requests come directly from your current Excel tracker
- They become the third level in the hierarchy
- No interruptions to current workflow
- The tool adds structure, not bureaucracy

---

# 8. Required Decisions Before Build

1. Confirm hierarchy:
   `Project → Work Package → Work Request → Task → Subtask`

2. Subtasks in MVF?
3. Include Work Packages in v1 or v2?
4. Include Weekly Goals in v1?
5. Should dependencies be manually defined?

---

# 9. Next Steps

- Finalize design decisions
- Implement data loader for existing tracker
- Build UI scaffolding
- Implement Task Flow Graph
- Implement Load Map
- Extend incrementally

This document will evolve as the design matures.
