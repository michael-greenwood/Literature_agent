// src/views/ProjectsOverview.jsx

import React, { useState } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Button,
  Stack,
  Divider,
  Menu,
  MenuItem,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useSpineDataContext } from "../context/SpineDataContext";

// Small colored dot component
function Dot({ color }) {
  return (
    <Box
      component="span"
      sx={{
        display: "inline-block",
        width: 10,
        height: 10,
        borderRadius: "50%",
        bgcolor: color,
        mr: 0.5,
      }}
    />
  );
}

function StatusChip({ status, settings }) {
  return (
    <Chip
      label={status}
      size="small"
      sx={{
        bgcolor: settings.statusColors[status] || "#9E9E9E",
        color: "#fff",
        textTransform: "capitalize",
      }}
    />
  );
}

// Editable priority chip
function PriorityChip({ node }) {
  const { settings, updateNode } = useSpineDataContext();
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleClick = (e) => setAnchorEl(e.currentTarget);
  const handleClose = () => setAnchorEl(null);

  const changePriority = (value) => {
    updateNode(node.id, { priority: value });
    handleClose();
  };

  return (
    <>
      <Chip
        label={node.priority}
        size="small"
        onClick={handleClick}
        sx={{
          bgcolor: settings.priorityColors[node.priority],
          color: "#fff",
          cursor: "pointer",
          textTransform: "capitalize",
        }}
      />
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        <MenuItem onClick={() => changePriority("high")}>High</MenuItem>
        <MenuItem onClick={() => changePriority("medium")}>Medium</MenuItem>
        <MenuItem onClick={() => changePriority("low")}>Low</MenuItem>
      </Menu>
    </>
  );
}

export default function ProjectsOverview() {
  const navigate = useNavigate();

  const {
    projects,
    getProjectNodes,
    settings,
  } = useSpineDataContext();

  // Filter out completed projects for overview
  const activeProjects = projects.filter(
    (proj) => proj.status !== "completed"
  );

  const computeBreakdown = (projectId) => {
    const nodes = getProjectNodes(projectId);

    const group = (type, status) =>
      nodes.filter((n) => n.type === type && n.status === status).length;

    return {
      tasks: {
        active: group("task", "active"),
        planned: group("task", "planned"),
        completed: group("task", "completed"),
      },
      wrs: {
        active: group("wr", "active"),
        planned: group("wr", "planned"),
        completed: group("wr", "completed"),
      },
      objs: {
        active: group("objective", "active"),
        planned: group("objective", "planned"),
        completed: group("objective", "completed"),
      },
    };
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Projects Overview
      </Typography>

      <Stack spacing={3}>
        {activeProjects.map((proj) => {
          const breakdown = computeBreakdown(proj.id);

          return (
            <Card key={proj.id} sx={{ borderLeft: "6px solid #1976d2" }}>
              <CardContent>
                {/* Header */}
                <Stack
                  direction="row"
                  justifyContent="space-between"
                  alignItems="center"
                >
                  <Typography variant="h5">{proj.name}</Typography>

                  <Stack direction="row" spacing={1}>
                    <StatusChip status={proj.status} settings={settings} />
                    <PriorityChip node={proj} />
                  </Stack>
                </Stack>

                <Divider sx={{ my: 2 }} />

                {/* Breakdown rows */}
                <Stack spacing={1}>
                  {/* Tasks */}
                  <Typography variant="body2">
                    <strong>Tasks:</strong>{" "}
                    <Dot color={settings.statusColors.active} />
                    {breakdown.tasks.active} active{" "}
                    <Dot color={settings.statusColors.planned} />
                    {breakdown.tasks.planned} planned{" "}
                    <Dot color={settings.statusColors.completed} />
                    {breakdown.tasks.completed} completed
                  </Typography>

                  {/* WRs */}
                  <Typography variant="body2">
                    <strong>Work Requests:</strong>{" "}
                    <Dot color={settings.statusColors.active} />
                    {breakdown.wrs.active} active{" "}
                    <Dot color={settings.statusColors.planned} />
                    {breakdown.wrs.planned} planned{" "}
                    <Dot color={settings.statusColors.completed} />
                    {breakdown.wrs.completed} completed
                  </Typography>

                  {/* Objectives */}
                  <Typography variant="body2">
                    <strong>Objectives:</strong>{" "}
                    <Dot color={settings.statusColors.active} />
                    {breakdown.objs.active} active{" "}
                    <Dot color={settings.statusColors.planned} />
                    {breakdown.objs.planned} planned{" "}
                    <Dot color={settings.statusColors.completed} />
                    {breakdown.objs.completed} completed
                  </Typography>
                </Stack>

                <Divider sx={{ my: 2 }} />

                {/* View Project */}
                <Button
                  variant="contained"
                  onClick={() => navigate(`/project/${proj.id}`)}
                >
                  View Project
                </Button>
              </CardContent>
            </Card>
          );
        })}
      </Stack>
    </Box>
  );
}
