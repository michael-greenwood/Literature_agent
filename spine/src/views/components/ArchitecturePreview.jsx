import React from "react";
import { Box, Card, Typography } from "@mui/material";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";

function Stage({ title, active }) {
  return (
    <Card
      sx={{
        padding: 3,
        minWidth: 180,
        textAlign: "center",
        background: active
          ? "linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)"
          : "#1e293b",
        transition: "all 0.6s ease",
        boxShadow: active
          ? "0 0 20px rgba(56,189,248,0.7)"
          : "0 0 10px rgba(0,0,0,0.5)",
        transform: active ? "scale(1.05)" : "scale(1)"
      }}
    >
      <Typography variant="subtitle1" fontWeight="bold">
        {title}
      </Typography>
    </Card>
  );
}

function ArchitecturePreview({ status }) {
  const running = status === "running";

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: 3,
        marginBottom: 5,
        flexWrap: "wrap"
      }}
    >
      <Stage title="Literature Sources" active={running} />

      <ArrowForwardIcon sx={{ fontSize: 40, opacity: 0.7 }} />

      <Stage title="LLM Extraction" active={running} />

      <ArrowForwardIcon sx={{ fontSize: 40, opacity: 0.7 }} />

      <Stage title="Relevance Scoring" active={running} />

      <ArrowForwardIcon sx={{ fontSize: 40, opacity: 0.7 }} />

      <Stage title="Project Memory" active={running} />
    </Box>
  );
}

export default ArchitecturePreview;
