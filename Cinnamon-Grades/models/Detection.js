const mongoose = require("mongoose");

const detectionSchema = new mongoose.Schema({
  image: String,
  status: String,
  final_grade: String,
  details: Object,

  //  Market Price Forecast
  market_price_forecast: {
    type: Object,
    default: null,
  },

  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model("Detection", detectionSchema);