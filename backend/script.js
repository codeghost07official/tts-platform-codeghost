// ===== THEME TOGGLE =====
const themeBtn = document.getElementById("themeToggle");

// default theme
document.body.classList.add("dark");

themeBtn.addEventListener("click", () => {
  if (document.body.classList.contains("dark")) {
    document.body.classList.remove("dark");
    document.body.classList.add("light");
    themeBtn.innerText = "☀️";
  } else {
    document.body.classList.remove("light");
    document.body.classList.add("dark");
    themeBtn.innerText = "🌙";
  }
});


// ===== LISTEN BUTTON =====
const listenBtn = document.getElementById("listen");
const downloadBtn = document.getElementById("download");

listenBtn.addEventListener("click", async () => {
  const text = document.getElementById("text").value;
  const voice = document.getElementById("voice").value;

  if (!text) return alert("Enter text first");

  listenBtn.innerText = "Loading...";
  listenBtn.disabled = true;

  try {
    const response = await fetch("http://127.0.0.1:5000/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text, voice })
    });

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    const audio = new Audio(url);
    audio.play();
  } catch (err) {
    alert("Error generating audio");
  }

  listenBtn.innerText = "Listen";
  listenBtn.disabled = false;
});


// ===== DOWNLOAD BUTTON =====
downloadBtn.addEventListener("click", async () => {
  const text = document.getElementById("text").value;
  const voice = document.getElementById("voice").value;

  if (!text) return alert("Enter text first");

  downloadBtn.innerText = "Loading...";
  downloadBtn.disabled = true;

  try {
    const response = await fetch("http://127.0.0.1:5000/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text, voice })
    });

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "voice.mp3";
    a.click();
  } catch (err) {
    alert("Error downloading audio");
  }

  downloadBtn.innerText = "Download";
  downloadBtn.disabled = false;
});