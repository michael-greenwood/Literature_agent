import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Card,
  CardContent,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Chip,
  CircularProgress
} from "@mui/material";
import { useParams, Link } from "react-router-dom";

const API_URL = "http://127.0.0.1:8001";

function ProjectDetailView() {
  const { name } = useParams();
  const [state, setState] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/engine/state`)
      .then(res => res.json())
      .then(data => setState(data))
      .catch(err => console.error(err));
  }, []);

  if (!state) {
    return (
      <Box sx={{ padding: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  const project = state.projects[name];

  if (!project) {
    return (
      <Box sx={{ padding: 4 }}>
        <Typography variant="h6">Project not found.</Typography>
      </Box>
    );
  }

  const paperIds = project.paper_ids || [];

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" sx={{ marginBottom: 2 }}>
        {name}
      </Typography>

      <Card sx={{ marginBottom: 3 }}>
  <CardContent>
    <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
      Description
    </Typography>

    <Typography variant="body2" sx={{ marginBottom: 2 }}>
      {project.description}
    </Typography>

    <Typography variant="body1" sx={{ marginBottom: 2 }}>
      Total Papers: {project.total_papers}
    </Typography>

    {/* Keywords */}
    {project.keywords?.length > 0 && (
      <>
        <Typography variant="subtitle2" gutterBottom>
          Keywords
        </Typography>
        <Box sx={{ marginBottom: 2 }}>
          {project.keywords.map((kw) => (
            <Chip
              key={kw}
              label={kw}
              size="small"
              sx={{ marginRight: 1, marginBottom: 1 }}
            />
          ))}
        </Box>
      </>
    )}

    {/* Techniques */}
    {project.techniques?.length > 0 && (
      <>
        <Typography variant="subtitle2" gutterBottom>
          Techniques
        </Typography>
        <Box>
          {project.techniques.map((tech) => (
            <Chip
              key={tech}
              label={tech}
              color="primary"
              size="small"
              sx={{ marginRight: 1, marginBottom: 1 }}
            />
          ))}
        </Box>
      </>
    )}
  </CardContent>
</Card>



      <Typography variant="h6" sx={{ marginBottom: 2 }}>
        Identified Papers
      </Typography>

      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Title</TableCell>
            <TableCell>Score</TableCell>
            <TableCell>Recommendation</TableCell>
            <TableCell>Why Relevant</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {paperIds.map((id) => {
            const paper = state.papers[id];
            const scoreObj = paper.project_scores[name];

            return (
              <TableRow key={id}>
                <TableCell>
                  <Link
                    to={`/paper/${id}`}
                    style={{ textDecoration: "none", color: "#38bdf8" }}
                  >
                    {paper.metadata.title}
                  </Link>
                </TableCell>
                <TableCell>{scoreObj.score}</TableCell>
                <TableCell>
                  <Chip
                    label={scoreObj.recommendation}
                    color={
                      scoreObj.recommendation === "include"
                        ? "success"
                        : scoreObj.recommendation === "watch"
                        ? "warning"
                        : "default"
                    }
                  />
                </TableCell>
                <TableCell>
                  {scoreObj.why_relevant?.slice(0, 100)}
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </Box>
  );
}

export default ProjectDetailView;
