import Chart from "https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.esm.js";
import { getAquisitionsByYear } from "./api.js";

(async function () {
  const data = await getAquisitionsByYear();

  new Chart(document.getElementById("acquisitions"), {
    type: "bar",
    data: {
      labels: data.map((row) => row.year),
      datasets: [
        {
          label: "Acquisitions by year",
          data: data.map((row) => row.count),
        },
      ],
    },
    options: {
      animation: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          enabled: false,
        },
      },
    },
  });
})();
