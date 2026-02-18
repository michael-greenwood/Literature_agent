import React, { useEffect, useState } from "react";
import { Box, Typography, Grid, Card, CardContent } from "@mui/material";
import { useNavigate } from "react-router-dom";

const API_URL = "http://127.0.0.1:8001";

function ProjectsView() {
  const [projects, setProjects] = useState({});
  const navigate = useNavigate();

  const fetchState = async () => {
    try {
      const res = await fetch(`${API_URL}/engine/state`);
      const data = await res.json();
      if (data?.projects) {
        setProjects(data.projects);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchState();
    const interval = setInterval(fetchState, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Projects
      </Typography>

      <Grid container spacing={3}>
        {Object.entries(projects).map(([name, proj]) => (
          <Grid item xs={12} md={6} lg={4} key={name}>
            <Card
              sx={{ cursor: "pointer" }}
              onClick={() => navigate(`/project/${encodeURIComponent(name)}`)}
            >
              <CardContent>
                <Typography variant="h6">{name}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Papers Identified: {proj.total_papers}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default ProjectsView;
