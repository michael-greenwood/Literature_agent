import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { SpineDataProvider } from "./context/SpineDataContext.jsx";
const theme = createTheme({
  palette: {
    mode: "light"
  }
});

ReactDOM.createRoot(document.getElementById("app")).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
       <SpineDataProvider>
        <App />
      </SpineDataProvider>
    </ThemeProvider>
  </React.StrictMode>
);
