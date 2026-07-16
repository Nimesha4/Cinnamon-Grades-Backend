const Detection = require("../models/Detection");
const { runYOLO } = require("../services/yoloService");

exports.uploadImage = async (req, res) => {
  try {
    const imagePath = req.file.path;

    // call service
    const result = await runYOLO(imagePath);

    // save to DB
    const newDetection = new Detection({
      image: imagePath,
      status: result.status,
      final_grade: result.final_grade,
      details: result.details,

      // Save Market Price Forecast
      market_price_forecast: result.market_price_forecast || null,
    });

    await newDetection.save();

    res.json({
      message: "Saved successfully",
      data: result,
    });

  } catch (error) {
    res.status(500).json({
      error: error.message || "Something went wrong",
      raw: error.raw || null,
    });
  }
};