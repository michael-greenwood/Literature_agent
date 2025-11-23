import React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Button from "@mui/material/Button";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <Box sx={{ flexGrow: 1, marginBottom: 2 }}>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">
            Projects
          </Button>
          <Button color="inherit" component={Link} to="/flow">
            Flow
          </Button>
          <Button color="inherit" component={Link} to="/load">
            Load Map
          </Button>
          <Button color="inherit" component={Link} to="/goals">
            Weekly Goals
          </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
