import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { keyframes } from "@mui/system";
import ArchitecturePreview from "./components/ArchitecturePreview";

const pulse = keyframes`
  0% { opacity: 0.4; }
  50% { opacity: 1; }
  100% { opacity: 0.4; }
`;

const API_URL = "http://127.0.0.1:8001";
//const API_URL = "http://132.156.103.106:8001"
function ResearchDashboard() {
  const [state, setState] = useState(null);
  const navigate = useNavigate();

  const fetchState = async () => {
    try {
        const res = await fetch(`${API_URL}/engine/state`);
        const data = await res.json();
        if (data) {
        setState(data);
        }
    } catch (err) {
        console.error(err);
    }
    };


  const startEngine = async () => {
    await fetch(`${API_URL}/engine/start`, { method: "POST" });
    fetchState(); // immediately refresh state
    };

  const resetEngine = async () => {
  await fetch(`${API_URL}/engine/reset`, { method: "POST" });
  fetchState();
};


  // Always fetch once on mount
useEffect(() => {
  fetchState();
}, []);

// Poll ONLY if backend says running
useEffect(() => {
  if (state?.engine?.status !== "running") return;

  const interval = setInterval(() => {
    fetchState();
  }, 1500);

  return () => clearInterval(interval);
}, [state?.engine?.status]);


  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" sx={{ marginBottom: 2 }}>
        Research Intelligence Platform — Live Literature Triage Demo
      </Typography>
        <ArchitecturePreview status={state?.engine?.status} />
        {state?.engine?.status !== "running" && (
  <Card sx={{ marginBottom: 4 }}>
    <CardContent>
      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
        Research Intelligence Platform — Demonstration Layer
      </Typography>

      <Typography variant="body2" sx={{ marginBottom: 2 }}>
        This demo represents the first operational layer of a persistent,
        agent-driven Research Intelligence Platform. The system continuously
        ingests scientific literature, decomposes each publication into structured
        scientific signals (problem, materials, methods, findings), and evaluates
        alignment against active research programs.
      </Typography>

      <Typography variant="body2" sx={{ marginBottom: 2 }}>
        Unlike traditional literature tools that summarize papers in isolation,
        this platform performs structured triage — identifying strategic
        relevance, surfacing high-signal work, and building a living,
        machine-readable representation of research activity over time.
      </Typography>

      <Typography variant="subtitle2" gutterBottom>
        How to Interact
      </Typography>

      <Typography variant="body2" component="ul" sx={{ paddingLeft: 3 }}>
        <li>
          Click <strong>Start Engine</strong> to initiate continuous ingestion.
        </li>
        <li>
          Observe live extraction and project-level scoring.
        </li>
        <li>
          Explore routed papers by project.
        </li>
        <li>
          Inspect full AI reasoning and signal alignment at the paper level.
        </li>
      </Typography>

      <Typography variant="body2" sx={{ marginTop: 2, fontStyle: "italic" }}>
        This is not a chatbot. It is an autonomous literature intelligence layer.
      </Typography>
    </CardContent>
  </Card>
)}

{/* Suggested Paper */}
            {state?.papers && Object.keys(state.papers).length > 0 && (() => {
            const suggested = Object.entries(state.papers)
                .flatMap(([id, paper]) =>
                Object.entries(paper.project_scores)
                    .filter(([_, score]) => score.recommendation === "include")
                    .map(([projectName, score]) => ({
                    id,
                    title: paper.metadata.title,
                    projectName,
                    score: score.score,
                    processed_at: paper.processed_at
                    }))
                )
                .sort((a, b) =>
                b.score - a.score ||
                new Date(b.processed_at) - new Date(a.processed_at)
                )[0];

            if (!suggested) return null;

            return (
                <Card sx={{ marginBottom: 4 }}>
                <CardContent>
                    <Typography variant="h6" gutterBottom>
                    📌 Suggested Paper to Read
                    </Typography>

                    <Typography variant="subtitle1" fontWeight="bold">
                    {suggested.title}
                    </Typography>

                    <Typography variant="body2" sx={{ marginTop: 1 }}>
                    Top Match for: {suggested.projectName}
                    </Typography>

                    <Typography variant="body2">
                    Relevance Score: {suggested.score}
                    </Typography>

                    <Button
                    variant="outlined"
                    sx={{ marginTop: 2 }}
                    component={Link}
                    to={`/paper/${suggested.id}`}
                    >
                    View Paper
                    </Button>
                </CardContent>
                </Card>
            );
            })()}
      {/* Controls */}
      <Box sx={{ marginBottom: 3 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={startEngine}
          sx={{ marginRight: 2 }}
        >
          ▶ Start Engine
        </Button>

        <Button
          variant="outlined"
          color="secondary"
          onClick={resetEngine}
        >
          🔁 Reset
        </Button>
      </Box>

      {/* Idle State */}
      {!state && (

        <Typography variant="body1">
          Press Start to begin ingestion.
        </Typography>
      )}

      {/* Main State View */}
      {state && (
        <>
          {/* Engine Status */}
          <Card sx={{ marginBottom: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Engine Status
              </Typography>

              <Chip
                label={state.engine.status}
                color={state.engine.status === "running" ? "success" : "default"}
                sx={{ marginBottom: 2 }}
              />
            {state.engine.status === "running" && (
            <Typography
                variant="body2"
                sx={{
                color: "#38bdf8",
                animation: `${pulse} 1.5s infinite`,
                fontWeight: 500
                }}
            >
                ● AI actively analyzing incoming literature
            </Typography>
            )}

              <Typography>
                Total Processed: {state.engine.total_processed}
              </Typography>
              <Typography>
                Total Routed: {state.engine.total_routed}
              </Typography>
              <Typography>
                Total Discarded: {state.engine.total_discarded}
              </Typography>
            </CardContent>
          </Card>

          {/* Current Processing */}
          {state.current_processing && (
            <Card sx={{ marginBottom: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Currently Processing
                </Typography>

                <Typography variant="subtitle1" fontWeight="bold">
                  {state.current_processing.title}
                </Typography>

                <Typography>
                  Stage: {state.current_processing.stage}
                </Typography>
              </CardContent>
            </Card>
          )}
            

          {/* Project Summary */}
          <Typography variant="h6" sx={{ marginBottom: 2 }}>
            Project Summary
          </Typography>

          <Grid container spacing={2}>
            {Object.entries(state.projects).map(([name, proj]) => (
              <Grid item xs={12} md={6} lg={4} key={name}>
                <Card
                    sx={{
                    cursor: "pointer",
                    transition: "0.2s",
                    "&:hover": {
                        transform: "scale(1.02)",
                        boxShadow: 6,
                    },
                    }}
                    onClick={() => navigate(`/project/${encodeURIComponent(name)}`)}
                >
                    <CardContent>
                    <Typography variant="subtitle1" fontWeight="bold">
                        {name}
                    </Typography>

                    <Typography>
                        Papers: {proj.total_papers}
                        </Typography>

                        {proj.paper_ids?.length > 0 && (
                        <Typography variant="body2" sx={{ marginTop: 1 }}>
                            High Confidence: {
                            proj.paper_ids.filter(pid =>
                                state.papers[pid].project_scores[name].confidence > 75
                            ).length
                            }
                        </Typography>
                        )}

                    </CardContent>
                </Card>
                </Grid>

            ))}
          </Grid>

          {/* Activity Feed */}
            {state.event_log?.length > 0 && (
            <>
                <Typography variant="h6" sx={{ marginTop: 4, marginBottom: 2 }}>
                Recent Activity
                </Typography>

                <Card>
                <CardContent>
                    {state.event_log.slice(0, 5).map((event, index) => (


                    <Box
                        key={index}
                        sx={{
                        paddingY: 1,
                        borderBottom:
                            index !== state.event_log.length - 1
                            ? "1px solid #334155"
                            : "none",
                        }}
                    >
                        <Typography variant="body2">
                        <strong>{event.title}</strong>
                        </Typography>

                        <Typography variant="caption" sx={{ opacity: 0.7 }}>
                        {event.action === "routed"
                            ? `Routed to ${event.best_project} (score: ${event.best_score})`
                            : "Discarded"}
                        </Typography>
                    </Box>
                    ))}
                </CardContent>
                </Card>
            </>
            )}

        </>
      )}
    </Box>
  );
}

export default ResearchDashboard;


