/* =========================================================
   AGRISENSE AI - FRONTEND JAVASCRIPT
   ========================================================= */

// FastAPI backend
const API_BASE_URL = "http://127.0.0.1:8000";

let temperatureChart = null;
let humidityChart = null;
let soilChart = null;


// =========================================================
// ELEMENTS
// =========================================================

const temperatureElement =
    document.getElementById("temperature");

const humidityElement =
    document.getElementById("humidity");

const soilElement =
    document.getElementById("soil");

const recommendationElement =
    document.getElementById("recommendation");

const confidenceElement =
    document.getElementById("confidence");

const lastUpdatedElement =
    document.getElementById("last-updated");

const historyBody =
    document.getElementById("history-body");


// =========================================================
// FETCH AND STORE NEW SENSOR READING
// =========================================================

async function fetchAndStore() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/fetch-and-store`,
            {
                method: "POST"
            }
        );

        if (!response.ok) {

            throw new Error(
                `HTTP error: ${response.status}`
            );

        }

        const result = await response.json();

        console.log(
            "Fetch and store:",
            result
        );

    } catch (error) {

        console.error(
            "Error fetching and storing sensor data:",
            error
        );

    }

}


// =========================================================
// FETCH IRRIGATION PREDICTION
// =========================================================

async function fetchIrrigationPrediction() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/irrigation-prediction`
        );

        if (!response.ok) {

            throw new Error(
                `HTTP error: ${response.status}`
            );

        }

        const result = await response.json();

        if (result.status !== "success") {

            throw new Error(
                "Unable to fetch irrigation prediction"
            );

        }

        const sensorData =
            result.sensor_data;

        const prediction =
            result.irrigation_prediction;


        // -------------------------------------------------
        // SENSOR VALUES
        // -------------------------------------------------

        temperatureElement.textContent =
            `${Number(sensorData.temperature).toFixed(1)} °C`;

        humidityElement.textContent =
            `${Number(sensorData.humidity).toFixed(1)} %`;

        soilElement.textContent =
            sensorData.soil_moisture;


        // -------------------------------------------------
        // IRRIGATION RECOMMENDATION
        // -------------------------------------------------

        recommendationElement.textContent =
            prediction.recommendation;


        // -------------------------------------------------
        // PREDICTION CONFIDENCE
        // -------------------------------------------------

        let probability =
            prediction.probability;


        // Convert decimal probability to percentage
        // Example: 1 -> 100%

        if (probability <= 1) {

            probability =
                probability * 100;

        }


        confidenceElement.textContent =
            `${Number(probability).toFixed(0)}%`;


        // -------------------------------------------------
        // LAST UPDATED
        // -------------------------------------------------

        if (sensorData.created_at) {

            lastUpdatedElement.textContent =
                formatDate(sensorData.created_at);

        } else {

            lastUpdatedElement.textContent =
                "Just now";

        }


        // -------------------------------------------------
        // CHANGE RECOMMENDATION COLOR
        // -------------------------------------------------

        updateRecommendationStyle(
            prediction.prediction
        );

    } catch (error) {

        console.error(
            "Error fetching irrigation prediction:",
            error
        );

        recommendationElement.textContent =
            "Unavailable";

        confidenceElement.textContent =
            "--";

        lastUpdatedElement.textContent =
            "Connection error";

    }

}


// =========================================================
// UPDATE RECOMMENDATION STYLE
// =========================================================

function updateRecommendationStyle(prediction) {

    if (prediction === 1) {

        recommendationElement.style.color =
            "#a66a18";

    } else {

        recommendationElement.style.color =
            "#247a50";

    }

}


// =========================================================
// FETCH IRRIGATION HISTORY
// =========================================================

async function fetchIrrigationHistory() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/irrigation-history`
        );

        if (!response.ok) {

            throw new Error(
                `HTTP error: ${response.status}`
            );

        }

        const result =
            await response.json();


        if (
            result.status !== "success" ||
            !Array.isArray(result.data)
        ) {

            throw new Error(
                "Invalid history response"
            );

        }


        renderHistory(
            result.data
        );


    } catch (error) {

        console.error(
            "Error fetching irrigation history:",
            error
        );

        historyBody.innerHTML = `
            <tr>
                <td colspan="6" class="error-state">
                    Unable to load irrigation history.
                </td>
            </tr>
        `;

    }

}


// =========================================================
// RENDER HISTORY TABLE
// =========================================================

function renderHistory(history) {

    if (history.length === 0) {

        historyBody.innerHTML = `
            <tr>
                <td colspan="6" class="loading">
                    No irrigation records available.
                </td>
            </tr>
        `;

        return;
    }


    historyBody.innerHTML = "";

    updateCharts(history);


    history.forEach(record => {

        const row =
            document.createElement("tr");


        // Recommendation badge

        const isWaterNeeded =
            record.prediction === 1;


        const badgeClass =
            isWaterNeeded
                ? "water"
                : "no-water";


        row.innerHTML = `

            <td>${record.id}</td>

            <td>
                ${Number(record.temperature).toFixed(1)} °C
            </td>

            <td>
                ${Number(record.humidity).toFixed(1)} %
            </td>

            <td>
                ${record.soil_moisture}
            </td>

            <td>
                <span class="recommendation-badge ${badgeClass}">
                    ${record.recommendation}
                </span>
            </td>

            <td>
                ${formatDate(record.timestamp)}
            </td>

        `;


        historyBody.appendChild(row);

    });

}


// =========================================================
// FORMAT DATE
// =========================================================

function formatDate(dateString) {

    if (!dateString) {

        return "--";

    }


    const date =
        new Date(dateString);


    if (isNaN(date.getTime())) {

        return dateString;

    }


    return date.toLocaleString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        }
    );

}


// =========================================================
// SENSOR TREND CHARTS
// =========================================================

function updateCharts(history) {

    if (!history || history.length === 0) {

        return;

    }


    // Reverse so oldest reading appears first

    const readings =
        [...history].reverse();


    // -------------------------------------------------
    // CHART LABELS
    // -------------------------------------------------

    const labels =
        readings.map(record => {

            const date =
                new Date(record.timestamp);

            return date.toLocaleTimeString(
                "en-IN",
                {
                    hour: "2-digit",
                    minute: "2-digit"
                }
            );

        });


    // -------------------------------------------------
    // SENSOR DATA
    // -------------------------------------------------

    const temperatures =
        readings.map(record =>
            Number(record.temperature)
        );


    const humidities =
        readings.map(record =>
            Number(record.humidity)
        );


    const soilMoisture =
        readings.map(record =>
            Number(record.soil_moisture)
        );


    // -------------------------------------------------
    // DESTROY OLD CHARTS
    // -------------------------------------------------

    if (temperatureChart) {

        temperatureChart.destroy();

    }


    if (humidityChart) {

        humidityChart.destroy();

    }


    if (soilChart) {

        soilChart.destroy();

    }


    // -------------------------------------------------
    // TEMPERATURE CHART
    // -------------------------------------------------

    const temperatureCanvas =
        document.getElementById(
            "temperatureChart"
        );


    temperatureChart =
        new Chart(
            temperatureCanvas,
            {
                type: "line",

                data: {

                    labels: labels,

                    datasets: [
                        {
                            label: "Temperature",

                            data: temperatures,

                            borderWidth: 2,

                            tension: 0.35,

                            pointRadius: 2,

                            fill: false
                        }
                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        legend: {

                            display: false

                        }

                    },

                    scales: {

                        x: {

                            ticks: {

                                maxTicksLimit: 4,

                                autoSkip: true,

                                maxRotation: 0,

                                minRotation: 0

                            }

                        },

                        y: {

                            beginAtZero: false

                        }

                    }

                }

            }
        );


    // -------------------------------------------------
    // HUMIDITY CHART
    // -------------------------------------------------

    const humidityCanvas =
        document.getElementById(
            "humidityChart"
        );


    humidityChart =
        new Chart(
            humidityCanvas,
            {
                type: "line",

                data: {

                    labels: labels,

                    datasets: [
                        {
                            label: "Humidity",

                            data: humidities,

                            borderWidth: 2,

                            tension: 0.35,

                            pointRadius: 2,

                            fill: false
                        }
                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        legend: {

                            display: false

                        }

                    },

                    scales: {

                        x: {

                            ticks: {

                                maxTicksLimit: 4,

                                autoSkip: true,

                                maxRotation: 0,

                                minRotation: 0

                            }

                        },

                        y: {

                            beginAtZero: false

                        }

                    }

                }

            }
        );


    // -------------------------------------------------
    // SOIL MOISTURE CHART
    // -------------------------------------------------

    const soilCanvas =
        document.getElementById(
            "soilChart"
        );


    soilChart =
        new Chart(
            soilCanvas,
            {
                type: "line",

                data: {

                    labels: labels,

                    datasets: [
                        {
                            label: "Soil Moisture",

                            data: soilMoisture,

                            borderWidth: 2,

                            tension: 0.35,

                            pointRadius: 2,

                            fill: false
                        }
                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        legend: {

                            display: false

                        }

                    },

                    scales: {

                        x: {

                            ticks: {

                                maxTicksLimit: 4,

                                autoSkip: true,

                                maxRotation: 0,

                                minRotation: 0

                            }

                        },

                        y: {

                            beginAtZero: false

                        }

                    }

                }

            }
        );

}


// =========================================================
// REFRESH COMPLETE DASHBOARD
// =========================================================

async function refreshDashboard() {

    console.log(
        "Refreshing dashboard..."
    );


    // 1. Fetch latest ThingSpeak reading
    //    and store it if it is new

    await fetchAndStore();


    // 2. Get current sensor data
    //    and ML prediction

    await fetchIrrigationPrediction();


    // 3. Get updated SQLite history
    //    and redraw charts

    await fetchIrrigationHistory();

}


// =========================================================
// INITIAL LOAD
// =========================================================

refreshDashboard();


// =========================================================
// AUTO REFRESH
// =========================================================

// Refresh the complete dashboard every 5 seconds

setInterval(
    refreshDashboard,
    5000
);