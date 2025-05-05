const express = require("express");
const axios = require("axios");
const path = require("path");

const app = express();
const port = 3000;

// Set up EJS
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Serve static files
app.use(express.static(path.join(__dirname, "public")));

// Middleware to parse form data
app.use(express.urlencoded({ extended: true }));

// Route to render the main page
app.get("/", async (req, res) => {
  try {
    // Fetch Q&As from FastAPI backend
    const response = await axios.get("http://localhost:8000/qna");
    const qnaData = response.data;
    res.render("index", { qnaData, answer: null });
  } catch (error) {
    console.error("Error fetching Q&As:", error.message);
    res.render("index", { qnaData: [], answer: "Error fetching Q&As" });
  }
});

// Route to handle question submission
app.post("/submit", async (req, res) => {
  const question = req.body.question;
  try {
    // Send question to FastAPI backend
    const response = await axios.post("http://localhost:8000/submit", { question }, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    const answer = response.data.answer;
    // Fetch Q&As again to re-render the page
    const qnaResponse = await axios.get("http://localhost:8000/qna");
    res.render("index", { qnaData: qnaResponse.data, answer });
  } catch (error) {
    console.error("Error submitting question:", error.message);
    const qnaResponse = await axios.get("http://localhost:8000/qna");
    res.render("index", { qnaData: qnaResponse.data, answer: "Error processing question" });
  }
});

app.listen(port, () => {
  console.log(`Frontend running at http://localhost:${port}`);
});