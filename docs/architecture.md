# Project Spine Viewer – Architecture Overview (Draft 0.1)

This document describes the **core system architecture** of Project Spine Viewer.  
It defines how data flows through the system, how nodes are modeled, and how the UI layers interact 
to support planning, dependency visualization, and workload analysis.

---

# 1. Architectural Goals

Project Spine Viewer aims to be:

- **Lightweight** – minimal backend, fast load, simple deployment  
- **Extensible** – future migration to Django/Insight backend  
- **Graph‑driven** – supports dependency graphs at all levels  
- **Hierarchical** – allows infinite nesting of project → tasks → WRs → objectives  
- **Predictive** – shadow pipeline and dependency analysis  
- **Actionable** – provides weekly planning, load maps, and structured execution  

---

# 2. High‑Level Architecture

```
 ┌───────────────────────────────┐
 │         React Frontend        │
 │     (Vite + MUI + React)      │
 └───────────────┬───────────────┘
                 │
                 ▼
 ┌───────────────────────────────┐
 │        Data Layer (JSON)      │
 │  - nodes.json (graph model)   │
 │  - people.json (champions)    │
 │  - settings.json              │
 └───────────────┬───────────────┘
                 │
                 ▼
 ┌───────────────────────────────┐
 │        Node Graph Engine      │
 │  - hierarchy (parent/child)   │
 │  - dependency graph (DAG)     │
 │  - status/priority logic      │
 │  - load aggregation           │
 │  - weekly objective filters   │
 └───────────────┬───────────────┘
                 │
                 ▼
 ┌──────────────────────────────────────────┐
 │                 Views                     │
 │  - Projects Overview                       │
 │  - Task Flow Graph (React Flow)           │
 │  - Team Load Map                           │
 │  - Weekly Goals                            │
 └──────────────────────────────────────────┘
```

Spine Viewer is **frontend‑only** for MVF, using static JSON as the backing store.

---

# 3. Node‑Based Data Model (Core of Spine)

Everything in Spine Viewer is represented as a **Node** within a dependency graph:

```
Node {
  id: string,
  type: project | task | wr | objective | milestone | pipeline,
  name: string,
  description: string,
  parent: string | null,
  children: [string],
  dependencies: [string],
  dependents: [string],        // derived, optional
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

This **single schema** supports:

- unlimited nesting  
- WR → tasks → objectives  
- shadow pipeline modeling  
- dependency graphs at all levels  
- future integration into Django models  

---

# 4. Internal Engines

### 4.1 Hierarchy Engine
Builds the parent/child tree:

- Projects at the top  
- Tasks underneath  
- Work Requests under tasks  
- Objectives under WRs  
- Any node type may contain children  

Produces a nested structure consumable by:

- Projects Overview  
- Load Map  
- Weekly Planner  

---

### 4.2 Dependency Graph Engine
Builds a **Directed Acyclic Graph (DAG)** from:

```
node.dependencies → edges
```

Used by:

- Task Flow Graph (React Flow)
- Blocked item detection
- Critical path analysis
- Parallel vs sequential work analysis

---

### 4.3 Load Aggregation Engine

Aggregates work across:

- champion
- assignee
- project
- task groupings

Using:

```
estimateHours
actualHours
status
```

Outputs:

- Fragmentation map  
- Workload heatmap  
- Per‑person task counts  
- "At risk" load warnings  

---

### 4.4 Weekly Goals Engine

Filters all nodes of type `"objective"` where:

```
status = active | in-progress
or
dueDate ∈ this week
or
parent.status = active
```

This powers:

- Weekly Goals view  
- Weekly planning summaries  
- Personal task lists  

---

# 5. View Architecture

## 5.1 Projects Overview
- Left: list of project nodes  
- Center: hierarchical expansion of tasks → WRs → objectives  
- Right (optional): metadata + actions  
- Shows pipeline, dependencies, progress  

Uses:  
Hierarchy Engine + Node Graph metadata

---

## 5.2 Task Flow Graph (React Flow)
- Converts dependency DAG into a visual graph  
- Each node becomes a card  
- Expandable groups (project → task → WR)  
- Supports parallel paths and branches  

Uses:  
Dependency Graph Engine

---

## 5.3 Team Load Map
- Aggregates active work by person  
- Highlights fragmentation  
- Provides load distribution insight  

Uses:
Load Aggregation Engine

---

## 5.4 Weekly Goals
- Flatten all active objective nodes  
- Organize by project or by person  
- Provides execution‑ready view  

Uses:
Weekly Goals Engine

---

# 6. Data Files Structure

```
/data/
  nodes.json        # All nodes (projects, tasks, WRs, objectives)
  people.json       # Champions, owners, assignees
  settings.json     # Optional global config
```

---

# 7. Migration Path to Backend (Future Option)

Eventually, Spine Viewer can integrate with:

### **Django API (Insight)**
Tables:
- Projects  
- WorkRequests  
- Tasks  
- Objectives  
- People  
- Dependencies  

Every table corresponds directly to a Node type.

### Benefits of future backend:
- Authentication  
- Persistence  
- Multi‑user editing  
- File attachments  
- Real dashboards  
- Integration with orchestrator  

But MVF stays frontend‑only for now.

---

# 8. Extensibility

This architecture supports future additions:

- Gantt/timeline view  
- Auto‑detect critical path  
- AI‑generated shadow pipelines  
- Load forecasting  
- WR → experiment linking  
- Multi‑project dashboards  
- Slack/Teams integrations  

Nothing in the architecture limits future growth.

---

# 9. Summary

Project Spine Viewer uses:

- A **unified Node model**  
- A **DAG + hierarchy engine**  
- A modular, React‑based UI  
- All data stored in JSON for MVF  

This provides a strong architectural foundation for:
- planning  
- dependency visualization  
- real team load insight  
- weekly execution  

The architecture is intentionally simple, flexible, and future‑ready.
