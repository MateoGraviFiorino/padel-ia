import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import PadelAnalyticsPage from "./pages/PadelAnalyticsPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/home" />} />
        <Route path="/home" element={<PadelAnalyticsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
