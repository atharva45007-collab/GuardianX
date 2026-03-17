const express = require("express");
const app = express();

// Root route
app.get("/", (req, res) => {
  res.send("GuardianX is live on Railway!");
});

// Example API route
app.get("/api/status", (req, res) => {
  res.json({ message: "GuardianX API working fine!" });
});

// Bind to Railway's PORT
const PORT = process.env.PORT || 5000;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});
