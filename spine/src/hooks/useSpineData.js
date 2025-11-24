// src/hooks/useSpineData.js

import nodesData from "../data/nodes.json";
import people from "../data/people.json";
import settings from "../data/settings.json";

function buildMaps(nodes) {
  const nodeMap = new Map();
  const childrenMap = new Map();
  const parentMap = new Map();
  const dependencyMap = new Map();
  const dependentsMap = new Map();

  nodes.forEach((node) => {
    nodeMap.set(node.id, node);
    childrenMap.set(node.id, node.children || []);
    parentMap.set(node.id, node.parent || null);

    const deps = node.dependencies || [];
    dependencyMap.set(node.id, deps);

    deps.forEach((depId) => {
      if (!dependentsMap.has(depId)) {
        dependentsMap.set(depId, []);
      }
      dependentsMap.get(depId).push(node.id);
    });
  });

  return { nodeMap, childrenMap, parentMap, dependencyMap, dependentsMap };
}

function classifyNodes(nodes) {
  const projects = [];
  const tasks = [];
  const workRequests = [];
  const objectives = [];

  nodes.forEach((node) => {
    switch (node.type) {
      case "project":
        projects.push(node);
        break;
      case "task":
        tasks.push(node);
        break;
      case "wr":
        workRequests.push(node);
        break;
      case "objective":
        objectives.push(node);
        break;
      default:
        break;
    }
  });

  return { projects, tasks, workRequests, objectives };
}

function buildPersonAssignments(nodes) {
  const assignments = new Map();

  nodes.forEach((node) => {
    if (!node.assignee) return;
    if (!assignments.has(node.assignee)) {
      assignments.set(node.assignee, []);
    }
    assignments.get(node.assignee).push(node.id);
  });

  return assignments;
}

function getStatus(map, id) {
  const n = map.get(id);
  return n ? n.status : undefined;
}

function isDependencySatisfied(map, id) {
  return getStatus(map, id) === "completed" || getStatus(map, id) === "done";
}

function buildBlockedNodes(nodes, dependencyMap, nodeMap) {
  return nodes.filter((node) => {
    const deps = dependencyMap.get(node.id) || [];
    return deps.some((depId) => !isDependencySatisfied(nodeMap, depId));
  });
}

function buildActiveObjectives(objectives) {
  return objectives.filter((obj) =>
    ["active", "in-progress"].includes(obj.status)
  );
}

function buildHierarchyTree(rootId, childrenMap, nodeMap) {
  const node = nodeMap.get(rootId);
  if (!node) return null;

  const childrenIds = childrenMap.get(rootId) || [];
  const children = childrenIds
    .map((id) => buildHierarchyTree(id, childrenMap, nodeMap))
    .filter(Boolean);

  return { ...node, children };
}

// ⭐️ FIXED VERSION: accepts override nodes
export default function useSpineData(overrideNodes = null) {
  const nodes = overrideNodes || nodesData;

  const {
    nodeMap,
    childrenMap,
    parentMap,
    dependencyMap,
    dependentsMap,
  } = buildMaps(nodes);

  const {
    projects,
    tasks,
    workRequests,
    objectives,
  } = classifyNodes(nodes);

  const personAssignments = buildPersonAssignments(nodes);
  const blockedNodes = buildBlockedNodes(nodes, dependencyMap, nodeMap);
  const activeObjectives = buildActiveObjectives(objectives);

  const getNode = (id) => nodeMap.get(id) || null;

  const getChildren = (id) => {
    const childIds = childrenMap.get(id) || [];
    return childIds.map((cid) => nodeMap.get(cid)).filter(Boolean);
  };

  const getHierarchyTree = (projectId) =>
    buildHierarchyTree(projectId, childrenMap, nodeMap);

  const getProjectNodes = (projectId) => {
    const tree = getHierarchyTree(projectId);
    if (!tree) return [];

    const acc = [];
    const recurse = (n) => {
      acc.push(n);
      (n.children || []).forEach(recurse);
    };
    recurse(tree);

    return acc;
  };

  return {
    // raw
    nodes,
    people,
    settings,

    // maps
    nodeMap,
    childrenMap,
    parentMap,
    dependencyMap,
    dependentsMap,
    personAssignments,

    // classified
    projects,
    tasks,
    workRequests,
    objectives,

    // computed
    blockedNodes,
    activeObjectives,

    // helpers
    getNode,
    getChildren,
    getHierarchyTree,
    getProjectNodes,
  };
}
