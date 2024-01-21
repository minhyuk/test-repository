// JavaScript for stopwatch
let stopwatchInterval;
let stopwatchTime;
let clockTime;

let recording = false;
const timeList = [];
const valueList = [];
const recordedData = [];

const stopwatch = document.getElementById("stopwatch");
const startStopButton = document.getElementById("startStopButton");
const saveButton = document.getElementById("saveButton");
const discardButton = document.getElementById("discardButton");
const csvInput = document.getElementById("csvInput");
const timeInput = document.getElementById("timeInput");

function formatTime(milliseconds) {
    const seconds = milliseconds / 1000;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = (seconds % 60).toFixed(2);
    return `${seconds.toFixed(2)}`;
}

startStopButton.addEventListener("click", () => {
    if (recording) {
        const csvContent = recordedData.map(data => data.join(",")).join("\n");
        csvInput.value = encodeURI(csvContent);
        timeInput.value = stopwatch.innerText;

        clearInterval(stopwatchInterval);
        startStopButton.innerText = "Start Recording";
        saveButton.disabled = false;

        var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
        plotModal();
        myModal.show();
    } else {
        // Clear previous data
        timeList.length = 0;
        valueList.length = 0;
        clockTime = new Date().getTime();

        // Start interval
        stopwatchInterval = setInterval(() => {
            stopwatchTime = new Date().getTime() - clockTime;
            let time = (stopwatchTime / 1000).toFixed(2);
            let value = slider.value;

            stopwatch.innerText = formatTime(stopwatchTime);

            timeList.push(time);
            valueList.push(value);
            recordedData.push([time, value]);
        }, 50);

        startStopButton.innerText = "Stop Recording";
        saveButton.disabled = true;

        if (modalChart) {
            modalChart.destroy();
        }
    }
    recording = !recording;
});

discardButton.addEventListener("click", () => {
    stopwatch.innerText = "0.00";
});

var modalChart;

function plotModal() {
    // Take input from html
    const Chart = window.Chart;

    color = Math.floor(Math.random() * 240);
    light = Math.floor(Math.random() * 80);

    GRAPH = document.getElementById('plotting-modal');

    modalChart = new Chart(GRAPH, {
        type: 'line',
        data: {
            labels: timeList,
            datasets: [{
                data: valueList,
                fill: false,
                borderColor: `hsl(${color}, 100%, ${light}%)`,
                tension: 0.1
            }]
        },
        options: {
            elements: {
                point: {
                    pointStyle: false
                },
            },
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                x: {
                    type: 'linear'
                },
                y: {
                    display: false,
                    min: -5,
                    max: 105
                },
            },
        },
        plugins: []
    });
}
