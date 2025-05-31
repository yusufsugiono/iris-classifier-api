const savedUsername = localStorage.getItem("username");
let username = "";
if (savedUsername) {
  username = savedUsername;
}

window.addEventListener("DOMContentLoaded", () => {
  const currentPath = window.location.pathname;
  if (currentPath.includes("/index.html")) {
    loadPredictionPage();
  } else if (currentPath.includes("/history.html")) {
    loadHistoryPage();
  }

  document.getElementById("reset").addEventListener("click", logout);
});

function setupUsername() {
  const usernameModal = new bootstrap.Modal(
    document.getElementById("usernameModal")
  );
  usernameModal.show();

  document.getElementById("usernameForm").addEventListener("submit", (e) => {
    e.preventDefault();
    username = document.getElementById("usernameInput").value;
    localStorage.setItem("username", username);
    usernameModal.hide();
  });
}

function loadPredictionPage() {
  if (!savedUsername) {
    setupUsername();
  }
  document.getElementById("displayUsername").textContent = username;
  document
    .getElementById("predictForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = {
        username,
        sepal_length: document.getElementById("sepal_length").value,
        sepal_width: document.getElementById("sepal_width").value,
        petal_length: document.getElementById("petal_length").value,
        petal_width: document.getElementById("petal_width").value,
      };

      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      alert(`Predicted Label: ${result.prediction}`);
    });
}

async function loadHistoryPage() {
  if (!savedUsername) {
    setupUsername();
  }
  document.getElementById("displayUsername").textContent = username;
  const response = await fetch(
    `http://localhost:5000/history?username=${username}`
  );
  const json = await response.json();
  let rows = "";
  if (json.history) {
    rows = json.history
      .map(
        (item) => `
            <tr>
              <td>${item.id}</td>
              <td>${item.sepal_length}</td>
              <td>${item.sepal_width}</td>
              <td>${item.petal_length}</td>
              <td>${item.petal_width}</td>
              <td>${item.predicted_label}</td>
              <td>${item.timestamp}</td>
            </tr>
          `
      )
      .join("");
  } else {
    rows = `<tr><td colspan="7" style="text-align:center;">${json.message}</td></tr>`;
  }

  document.getElementById("history_result").innerHTML = rows;
}

function logout() {
  if (savedUsername) {
    localStorage.removeItem("username");
    alert("Reset username berhasil! Silakan input kembali");
    window.location.href = "index.html";
  }
}
