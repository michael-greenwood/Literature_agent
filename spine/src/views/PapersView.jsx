import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Chip,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const API_URL = "http://127.0.0.1:8001";

function PapersView() {
  const [state, setState] = useState(null);
  const [filter, setFilter] = useState("all");
  const navigate = useNavigate();

  const fetchState = async () => {
    try {
      const res = await fetch(`${API_URL}/engine/state`);
      const data = await res.json();
      setState(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchState();
  }, []);

  if (!state) {
    return (
      <Box sx={{ padding: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  const papers = Object.entries(state.papers || {}).map(([id, paper]) => ({
    id,
    ...paper
  }));

  const filtered = papers.filter((paper) => {
    if (filter === "all") return true;
    if (filter === "discarded")
      return state.discarded.includes(paper.id);
    return paper.assigned_projects.includes(filter);
  });

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" sx={{ marginBottom: 3 }}>
        All Processed Papers
      </Typography>

      {/* Filter */}
      <Box sx={{ marginBottom: 2 }}>
        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Filter</InputLabel>
          <Select
            value={filter}
            label="Filter"
            onChange={(e) => setFilter(e.target.value)}
          >
            <MenuItem value="all">All</MenuItem>
            <MenuItem value="discarded">Discarded</MenuItem>
            {Object.keys(state.projects).map((proj) => (
              <MenuItem key={proj} value={proj}>
                {proj}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Title</TableCell>
            <TableCell>Year</TableCell>
            <TableCell>Source</TableCell>
            <TableCell>Projects</TableCell>
            <TableCell>Status</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {filtered.map((paper) => {
            const isDiscarded = state.discarded.includes(paper.id);

            return (
              <TableRow
                key={paper.id}
                hover
                sx={{ cursor: "pointer" }}
                onClick={() => navigate(`/paper/${paper.id}`)}
              >
                <TableCell>{paper.metadata.title}</TableCell>
                <TableCell>{paper.metadata.year}</TableCell>
                <TableCell>{paper.metadata.source}</TableCell>

                <TableCell>
                  {paper.assigned_projects.map((proj) => (
                    <Chip
                      key={proj}
                      label={proj}
                      size="small"
                      sx={{ marginRight: 1 }}
                    />
                  ))}
                </TableCell>

                <TableCell>
                  {isDiscarded ? (
                    <Chip label="Discarded" color="error" size="small" />
                  ) : (
                    <Chip label="Routed" color="success" size="small" />
                  )}
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </Box>
  );
}

export default PapersView;


