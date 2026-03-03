window.addEventListener("DOMContentLoaded", () => {
  const currentPath = window.location.pathname;
  if (currentPath.includes("/index.html")) {
    loadPredictionPage();
  }
});


function loadPredictionPage() {
  document
    .getElementById("predictForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = {
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
