const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
require("dotenv").config();

const detectionRoutes = require("./routes/detectionRoutes");

const app = express();

app.use(cors());
app.use(express.json());

// DB
mongoose.connect(process.env.MONGO_URI, {
  dbName: "cinnamonData",
})
  .then(() => console.log("MongoDB Connected"))
  .catch(err => console.log(err));

// Routes
app.get("/", (req, res) => {
  res.send("Cinnamon Backend Running...");
});

app.use("/", detectionRoutes);

// Server
const PORT = 9000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});