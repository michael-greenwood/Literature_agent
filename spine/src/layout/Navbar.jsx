import React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <Box sx={{ flexGrow: 1, marginBottom: 2 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography
            variant="h6"
            sx={{ flexGrow: 1, fontWeight: 500 }}
          >
            Research Intelligence Platform
          </Typography>

          <Button color="inherit" component={Link} to="/">
            Dashboard
          </Button>


          <Button color="inherit" component={Link} to="/papers">
            Papers
          </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

