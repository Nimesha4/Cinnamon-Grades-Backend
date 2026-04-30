const mongoose = require("mongoose");

const detectionSchema = new mongoose.Schema({
  image: String,
  status: String,
  final_grade: String,
  details: Object,
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model("Detection", detectionSchema);