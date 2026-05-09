const API_BASE_URL = "http://127.0.0.1:8000";

const plusBtn = document.getElementById("plusBtn");
const pdfInput = document.getElementById("pdfInput");
const questionInput = document.getElementById("questionInput");
const sendBtn = document.getElementById("sendBtn");
const chatBox = document.getElementById("chatBox");

const docName = document.getElementById("docName");
const uploadStatus = document.getElementById("uploadStatus");
const floatingDocName = document.getElementById("floatingDocName");
const removeFileBtn = document.getElementById("removeFileBtn");

let uploadedFileName = "";
let pdfReady = false;
let currentFileId = "";

plusBtn.addEventListener("click", () => {
  pdfInput.click();
});

pdfInput.addEventListener("change", async () => {
  const file = pdfInput.files[0];
  if (!file) return;

  uploadedFileName = file.name;
  pdfReady = false;
  currentFileId = "";

  document.body.classList.add("pdf-uploaded");

  docName.textContent = file.name;
  floatingDocName.textContent = file.name;
  uploadStatus.textContent = "Uploading...";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Upload failed");
    }

    pdfReady = true;
    currentFileId = data.file_id;

    uploadStatus.textContent = "PDF ready ✅";
    floatingDocName.textContent = data.filename || file.name;
  } catch (error) {
    pdfReady = false;
    currentFileId = "";

    uploadStatus.textContent = "Upload failed ❌";
    showToast("PDF upload failed. Please check your backend server.");
  }
});

sendBtn.addEventListener("click", askQuestion);

questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    askQuestion();
  }
});

removeFileBtn.addEventListener("click", () => {
  pdfInput.value = "";
  uploadedFileName = "";
  pdfReady = false;

  document.body.classList.remove("pdf-uploaded");

  docName.textContent = "No PDF uploaded";
  floatingDocName.textContent = "No PDF uploaded";
  uploadStatus.textContent = "PDF";
});

async function askQuestion() {
  const question = questionInput.value.trim();

  if (!question) return;

  if (!pdfReady) {
    addMessage("bot", "Please upload a PDF first using the + button.");
    return;
  }

  document.body.classList.add("chat-started");

  addMessage("user", question);
  questionInput.value = "";

  const loadingMessage = addMessage("bot", "Thinking...");

  try {
    const response = await fetch(
      `${API_BASE_URL}/ask?question=${encodeURIComponent(question)}&file_id=${encodeURIComponent(currentFileId)}`
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to get answer");
    }

loadingMessage.textContent = data.answer || "No answer found.";

setTimeout(() => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: "smooth",
  });
}, 100);
  } catch (error) {
    loadingMessage.textContent = "Failed to get answer. Check backend.";
  }
}

function addMessage(type, text) {
  const message = document.createElement("div");
  message.className = `message ${type}`;
  message.textContent = text;

  chatBox.appendChild(message);

  setTimeout(() => {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth",
    });
  }, 100);

  return message;
}

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 5000);
}