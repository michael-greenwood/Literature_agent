import React from "react";
import projectData from "../data/projects.json";
import { Card, CardContent, Typography, List, ListItem } from "@mui/material";

export default function ProjectsOverview() {
  const { projects } = projectData;

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom>
        Projects Overview
      </Typography>

      {projects.map((p) => (
        <Card key={p.id} sx={{ marginBottom: 2 }}>
          <CardContent>
            <Typography variant="h5">{p.name}</Typography>

            <Typography variant="subtitle1" sx={{ marginTop: 2 }}>
              Shadow Pipeline
            </Typography>

            <List dense>
              {p.shadowPipeline.map((item, idx) => (
                <ListItem key={idx}>• {item}</ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
