import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./layout/Navbar";
import ProjectsOverview from "./views/ProjectsOverview";
import TeamLoadMap from "./views/TeamLoadMap";
import TaskFlowGraph from "./views/TaskFlowGraph";
import WeeklyGoals from "./views/WeeklyGoals";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<ProjectsOverview />} />
        <Route path="/load" element={<TeamLoadMap />} />
        <Route path="/flow" element={<TaskFlowGraph />} />
        <Route path="/goals" element={<WeeklyGoals />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
