import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  Divider
} from "@mui/material";
import { useParams } from "react-router-dom";

const API_URL = "http://127.0.0.1:8001";

function PaperDetailView() {
  const { id } = useParams();
  const [paper, setPaper] = useState(null);

  const fetchPaper = async () => {
    try {
      const res = await fetch(`${API_URL}/engine/state`);
      const data = await res.json();
      if (data?.papers?.[id]) {
        setPaper(data.papers[id]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchPaper();
  }, [id]);

  if (!paper) {
    return (
      <Box sx={{ padding: 4 }}>
        <Typography>Loading paper...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ padding: 4 }}>
      {/* ---------------- */}
      {/* Metadata Section */}
      {/* ---------------- */}
     <Typography variant="h4" gutterBottom>
    {paper.metadata.title}
    </Typography>

    <Card sx={{ marginBottom: 4 }}>
    <CardContent>
        <Typography variant="subtitle1" gutterBottom>
        Publication Details
        </Typography>

        <Typography variant="body2">
        <strong>Authors:</strong>{" "}
        {paper.metadata.authors?.length
            ? paper.metadata.authors.join(", ")
            : "N/A"}
        </Typography>

        <Typography variant="body2">
        <strong>Year:</strong> {paper.metadata.year || "N/A"}
        </Typography>

        <Typography variant="body2">
        <strong>Source:</strong> {paper.metadata.source || "N/A"}
        </Typography>

        {paper.metadata.doi && (
        <Typography variant="body2">
            <strong>DOI:</strong>{" "}
            <a
            href={`https://doi.org/${paper.metadata.doi}`}
            target="_blank"
            rel="noopener noreferrer"
            >
            {paper.metadata.doi}
            </a>
        </Typography>
        )}

        {paper.metadata.arxiv_id && (
        <Typography variant="body2">
            <strong>arXiv:</strong>{" "}
            <a
            href={`https://arxiv.org/abs/${paper.metadata.arxiv_id}`}
            target="_blank"
            rel="noopener noreferrer"
            >
            {paper.metadata.arxiv_id}
            </a>
        </Typography>
        )}

        <Divider sx={{ marginY: 2 }} />

        <Typography variant="subtitle2" gutterBottom>
        Abstract
        </Typography>

        <Typography variant="body2">
        {paper.metadata.abstract}
        </Typography>
    </CardContent>
    </Card>


      {/* ---------------- */}
      {/* Extraction Block */}
      {/* ---------------- */}
      <Card sx={{ marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Extraction
          </Typography>

          <Typography><strong>Problem:</strong> {paper.extraction.problem}</Typography>

          <Typography sx={{ marginTop: 1 }}>
            <strong>Materials:</strong> {paper.extraction?.materials?.join(", ") || "—"}
          </Typography>

          <Typography sx={{ marginTop: 1 }}>
            <strong>Methods:</strong> {paper.extraction?.materials?.join(", ") || "—"}
          </Typography>

          <Typography sx={{ marginTop: 1 }}>
            <strong>Findings:</strong> {paper.extraction?.materials?.join(", ") || "—"}
          </Typography>

          <Typography sx={{ marginTop: 1 }}>
            <strong>Limitations:</strong> {paper.extraction?.materials?.join(", ") || "—"}
          </Typography>
        </CardContent>
      </Card>

      {/* ---------------- */}
      {/* Project Scoring  */}
      {/* ---------------- */}
      <Typography variant="h6" sx={{ marginBottom: 2 }}>
        Project Evaluations
      </Typography>

      <Grid container spacing={2}>
        {Object.entries(paper.project_scores).map(([projectName, scoreObj]) => (
          <Grid item xs={12} md={6} key={projectName}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1" fontWeight="bold">
                  {projectName}
                </Typography>

               <Chip
                label={`${scoreObj.score} (${scoreObj.recommendation})`}
                color={
                    scoreObj.recommendation === "include"
                    ? "success"
                    : scoreObj.recommendation === "watch"
                    ? "warning"
                    : "default"
                }
                sx={{ marginTop: 1 }}
                />

                {/* Score Bar */}
                <Box sx={{ width: "100%", marginTop: 1, marginBottom: 2 }}>
                <Box
                    sx={{
                    height: 6,
                    borderRadius: 3,
                    backgroundColor: "#334155",
                    }}
                >
                    <Box
                    sx={{
                        width: `${scoreObj.score}%`,
                        height: "100%",
                        borderRadius: 3,
                        backgroundColor:
                        scoreObj.score > 70
                            ? "#22c55e"
                            : scoreObj.score > 40
                            ? "#facc15"
                            : "#ef4444",
                    }}
                    />
                </Box>
                </Box>

                <Typography variant="body2">
                <strong>Confidence:</strong> {scoreObj.confidence}
                </Typography>


                <Typography variant="body2">
                  <strong>Confidence:</strong> {scoreObj.confidence}
                </Typography>

                <Divider sx={{ marginY: 2 }} />

                <Typography variant="body2">
                  <strong>Why Relevant:</strong> {scoreObj.why_relevant || "—"}
                </Typography>

                <Typography variant="body2" sx={{ marginTop: 1 }}>
                  <strong>Why Not Relevant:</strong> {scoreObj.why_not_relevant || "—"}
                </Typography>

                {scoreObj.matched_signals?.length > 0 && (
                  <Typography variant="body2" sx={{ marginTop: 1 }}>
                    <strong>Matched Signals:</strong>{" "}
                    {scoreObj.matched_signals.join(", ")}
                  </Typography>
                )}

                {scoreObj.missing_signals?.length > 0 && (
                  <Typography variant="body2" sx={{ marginTop: 1 }}>
                    <strong>Missing Signals:</strong>{" "}
                    {scoreObj.missing_signals.join(", ")}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default PaperDetailView;
