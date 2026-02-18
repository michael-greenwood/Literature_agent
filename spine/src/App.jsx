import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./layout/Navbar";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

import ResearchDashboard from "./views/ResearchDashboard";
import PapersView from "./views/PapersView";
import ProjectDetailView from "./views/ProjectDetailView";
import PaperDetailView from "./views/PaperDetailView";
const darkTheme = createTheme({
  palette: {
    mode: "dark",
    background: {
      default: "#0f172a",
      paper: "#1e293b"
    },
    primary: {
      main: "#38bdf8" // cyan accent
    }
  }
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<ResearchDashboard />} />
          <Route path="/papers" element={<PapersView />} />
          <Route path="/project/:name" element={<ProjectDetailView />} />
          <Route path="/paper/:id" element={<PaperDetailView />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}


export default App;
