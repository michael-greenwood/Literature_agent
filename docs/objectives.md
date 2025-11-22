# Project Spine Viewer – Objectives

## 1. Goals

- Add true hierarchical structure to the existing work-request system
- Prevent task drift by explicitly capturing internal tasks and subtasks
- Reveal dependencies and sequencing that currently exist only mentally
- Provide team load visibility (fragmentation + workload)
- Provide forward-looking planning (shadow pipeline)
- Increase execution speed and reduce cognitive load
- Provide a foundation for future integration with Insight

## 2. Scope

### In Scope (MVF)
- Shadow pipeline
- Team load visualization
- Work Request → Task → Subtask structure
- Task flow graph (simple arrows)
- Manual dependency definition
- Weekly goals (optional but recommended)
- Read-only import of existing Work Request sheet

### Out of Scope (for now)
- Full Gantt charts
- Automation of scheduling
- Calendar integration
- API sync with Pace or Insight
- Multi-user realtime collaboration
- Authentication

## 3. Non-Goals

- This tool is *not* a replacement for the Work Request tracker
- Not designed to enforce process change on project leads
- Not intended as a full orchestration engine (yet)
- Not performing automated scheduling or resource allocation

## 4. Minimal Viable Requirements

- Display projects and associated work requests
- Allow tasks and subtasks to be defined under each WR
- Show a dependency graph for tasks
- Compute fragmentation per person
- Show predicted upcoming tasks (shadow pipeline)

## 5. Future Extensions

- Work Package level detail  
- Auto-ingest from Pace API  
- Integration with Insight backend  
- Timeline visualizations  
- Automated dependency resolution  
- Risk scoring  
- Milestone tracking  
- Tagging and categorization  

## 6. Risks & Assumptions

- Assumes user manually maintains shadow pipeline  
- Assumes Work Request tracker remains in current form  
- Assumes limited time investment for MVP  
- Design must remain flexible for Insight integration  

This document will evolve as project scope expands and requirements solidify.
