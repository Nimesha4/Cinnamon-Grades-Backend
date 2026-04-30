const express = require("express");
const router = express.Router();
const multer = require("multer");
const path = require("path");

const { uploadImage } = require("../controllers/detectionController");

// multer config 
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads/");
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  },
});

const upload = multer({ storage });

// route
router.post("/upload", upload.single("image"), uploadImage);

module.exports = router;