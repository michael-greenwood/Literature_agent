// src/context/SpineDataContext.jsx

import React, { createContext, useContext, useMemo, useState } from "react";
import useSpineData from "../hooks/useSpineData";

const SpineDataContext = createContext(null);

export function SpineDataProvider({ children }) {

  // 1. Load initial JSON
  const initial = useSpineData();

  // 2. Hold nodes in React state
  const [nodes, setNodes] = useState(initial.nodes);

  // 3. Recompute all derived structures when nodes change
  const spineData = useMemo(() => {
    return useSpineData(nodes);   // <-- IMPORTANT: pass override nodes
  }, [nodes]);

  // 4. Update any node in the system
  const updateNode = (id, updates) => {
    setNodes(prev =>
      prev.map(n => (n.id === id ? { ...n, ...updates } : n))
    );
  };

  // 5. Expose data + updater
  const value = useMemo(() => ({
    ...spineData,
    updateNode,
  }), [spineData]);

  return (
    <SpineDataContext.Provider value={value}>
      {children}
    </SpineDataContext.Provider>
  );
}

export function useSpineDataContext() {
  const ctx = useContext(SpineDataContext);
  if (!ctx) {
    throw new Error("useSpineDataContext must be used inside SpineDataProvider");
  }
  return ctx;
}
