const root = document.getElementById("root");
document.body.className =
  "bg-neutral-950 text-white min-h-screen p-6 font-sans";

const heading = document.createElement("h1");
heading.textContent = "Forest Fire Predictions";
heading.className = "text-4xl font-extrabold text-sky-400 mb-4 text-center";
root.appendChild(heading);

const paragraph = document.createElement("p");
paragraph.textContent =
  "Live fire risk data from PyroScan-AI prediction engine.";
paragraph.className = "text-lg text-gray-300 mb-8 text-center";
root.appendChild(paragraph);

// Container for chart
const chartContainer = document.createElement("div");
chartContainer.className =
  "max-w-4xl mx-auto mb-10 bg-stone-900 p-6 rounded-2xl shadow-lg";
root.appendChild(chartContainer);

// Create canvas for Chart.js
const canvas = document.createElement("canvas");
canvas.id = "predictionChart";
chartContainer.appendChild(canvas);

// Create grid for cards
const grid = document.createElement("div");
grid.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6";
root.appendChild(grid);

fetch("http://127.0.0.1:8434/api/v1/predictions")
  .then((res) => res.json())
  .then((data) => {
    const priority = { high: 3, moderate: 2, low: 1 };
    data.sort(
      (a, b) =>
        (priority[b.Prediction.toLowerCase()] || 0) -
        (priority[a.Prediction.toLowerCase()] || 0)
    );

    // Build scatter chart data
    const scatterData = data.map((item, index) => ({
      x: index,
      y:
        item.Prediction.toLowerCase() === "high"
          ? 3
          : item.Prediction.toLowerCase() === "moderate"
          ? 2
          : 1,
      location: item.Location,
      reason: item.Reason,
      prediction: item.Prediction,
      id: index,
    }));

    // Create Chart.js scatter chart with heatmap-style gradient
    const ctx = canvas.getContext("2d");
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, "#ef4444"); // High
    gradient.addColorStop(0.5, "#eab308"); // Moderate
    gradient.addColorStop(1, "#22c55e"); // Low

    const chart = new Chart(ctx, {
      type: "scatter",
      data: {
        datasets: [
          {
            label: "Fire Risk",
            data: scatterData,
            backgroundColor: "white",
            pointRadius: 8,
            pointHoverRadius: 10,
            borderColor: "#38bdf8",
            borderWidth: 1.5,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                const d = context.raw;
                return `Location: ${d.location}\nPrediction: ${d.prediction}\nReason: ${d.reason}`;
              },
            },

            backgroundColor: "#1f2937",
            titleColor: "#fbbf24",
            bodyColor: "#f3f4f6",
          },
          legend: { display: false },
        },
        scales: {
          x: {
            type: "linear",
            title: {
              display: true,
              text: "Prediction Index",
              color: "white",
            },
            ticks: { color: "white" },
            grid: { color: "#374151" },
          },
          y: {
            min: 0,
            max: 4,
            title: {
              display: true,
              text: "Risk Level",
              color: "white",
            },
            ticks: {
              color: "white",
              stepSize: 1,
              callback: (val) =>
                val === 3
                  ? "High"
                  : val === 2
                  ? "Moderate"
                  : val === 1
                  ? "Low"
                  : "",
            },
            grid: {
              color: function (context) {
                const y = context.tick.value;
                return y === 3
                  ? "#ef4444"
                  : y === 2
                  ? "#eab308"
                  : y === 1
                  ? "#22c55e"
                  : "#374151";
              },
              lineWidth: 2,
            },
          },
        },
      },
    });

    // Create cards and connect interaction
    data.forEach((item, index) => {
      const card = document.createElement("div");
      card.className =
        "bg-stone-900 rounded-2xl shadow-lg p-6 transition-transform duration-300 hover:scale-[1.03] cursor-pointer";

      const location = document.createElement("h2");
      location.textContent = item.Location;
      location.className = "text-2xl font-semibold text-sky-300 mb-2";

      const prediction = document.createElement("p");
      prediction.innerHTML = `<span class="font-bold text-white">Prediction:</span> <span class="text-${getColor(
        item.Prediction
      )}-400">${item.Prediction}</span>`;
      prediction.className = "mb-2";

      const reason = document.createElement("p");
      reason.innerHTML = `<span class="text-gray-400 text-sm">Reason:</span> <span class="text-gray-200 text-sm">${item.Reason}</span>`;

      // Card-click → highlight point on chart
      card.addEventListener("click", () => {
        chart.setActiveElements([{ datasetIndex: 0, index: index }]);
        chart.tooltip.setActiveElements([{ datasetIndex: 0, index: index }]);
        chart.update();
        canvas.scrollIntoView({ behavior: "smooth", block: "center" });
      });

      card.appendChild(location);
      card.appendChild(prediction);
      card.appendChild(reason);
      grid.appendChild(card);
    });
  })
  .catch((err) => {
    const errorMsg = document.createElement("p");
    errorMsg.textContent = "⚠ Failed to fetch data from API.";
    errorMsg.className = "text-red-500 text-center mt-6";
    root.appendChild(errorMsg);
    console.error(err);
  });

function getColor(level) {
  switch (level.toLowerCase()) {
    case "low":
      return "green";
    case "moderate":
      return "yellow";
    case "high":
      return "red";
    default:
      return "gray";
  }
}
