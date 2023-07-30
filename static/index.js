var temperatureHistoryDiv = document.getElementById("temperature-history");
var humidityHistoryDiv = document.getElementById("humidity-history");

var graphConfig = {
  displayModeBar: false,
  responsive: true,
};

// History Data
var temperatureTrace = {
  x: [],
  y: [],
  name: "Temperature",
  mode: "lines+markers",
  type: "line",
};
var humidityTrace = {
  x: [],
  y: [],
  name: "Humidity",
  mode: "lines+markers",
  type: "line",
};

var temperatureLayout = {
  autosize: true,
  title: {
    text: "Temperature",
  },
  font: {
    size: 14,
    color: "#7f7f7f",
  },
  colorway: ["#B22222"],
  //   width: 450,
  //   height: 260,
  margin: { t: 30, b: 20, l: 30, r: 20, pad: 0 },
};
var humidityLayout = {
  autosize: true,
  title: {
    text: "Humidity",
  },
  font: {
    size: 14,
    color: "#7f7f7f",
  },
  colorway: ["#00008B"],
  //   width: 450,
  //   height: 260,
  margin: { t: 30, b: 20, l: 30, r: 20, pad: 0 },
};
var config = { responsive: true };

Plotly.newPlot(
  temperatureHistoryDiv,
  [temperatureTrace],
  temperatureLayout,
  graphConfig
);
Plotly.newPlot(
  humidityHistoryDiv,
  [humidityTrace],
  humidityLayout,
  graphConfig
);

// Gauge Data
var temperatureData = [
  {
    domain: { x: [0, 1], y: [0, 1] },
    value: 0,
    title: { text: "Temperature" },
    type: "indicator",
    mode: "gauge+number+delta",
    delta: { reference: 30 },
    gauge: {
      axis: { range: [null, 50] },
      steps: [
        { range: [0, 20], color: "lightgray" },
        { range: [20, 30], color: "gray" },
      ],
      threshold: {
        line: { color: "red", width: 4 },
        thickness: 0.75,
        value: 30,
      },
    },
  },
];

var humidityData = [
  {
    domain: { x: [0, 1], y: [0, 1] },
    value: 0,
    title: { text: "Humidity" },
    type: "indicator",
    mode: "gauge+number+delta",
    delta: { reference: 50 },
    gauge: {
      axis: { range: [null, 100] },
      steps: [
        { range: [0, 20], color: "lightgray" },
        { range: [20, 30], color: "gray" },
      ],
      threshold: {
        line: { color: "red", width: 4 },
        thickness: 0.75,
        value: 30,
      },
    },
  },
];

var layout = { width: 350, height: 250, margin: { t: 0, b: 0, l: 0, r: 0 } };

// Temperature
let newTempXArray = [];
let newTempYArray = [];
// Humidity
let newHumidityXArray = [];
let newHumidityYArray = [];

// The maximum number of data points displayed on our scatter/line graph
let MAX_GRAPH_POINTS = 12;
let ctr = 0;

function updateCharts(lineChartDiv, xArray, yArray, sensorRead) {
  var today = new Date();
  var time =
    today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
  if (xArray.length >= MAX_GRAPH_POINTS) {
    xArray.shift();
  }
  if (yArray.length >= MAX_GRAPH_POINTS) {
    yArray.shift();
  }
  xArray.push(ctr++);
  yArray.push(sensorRead);

  var data_update = {
    x: [xArray],
    y: [yArray],
  };

  Plotly.update(lineChartDiv, data_update);
}

function updateWeatherData(weather) {
  $("#temperature").html(weather.temperature.toFixed(1) + " C")
  $("#humidity").html(weather.humidity.toFixed(1) + " %")
  $("#pressure").html(weather.pressure.toFixed(0) + " mPa")

  $("#lighting").html(weather.lighting.toFixed(0) + " Lux")
  $("#battery").html(weather.battery.toFixed(2)+" V" )
  $("#rssi").html(weather.rssi)

  // Update Temperature Line Chart
  updateCharts(
    temperatureHistoryDiv,
    newTempXArray,
    newTempYArray,
    temperature
  );
  // Update Humidity Line Chart
  updateCharts(
    humidityHistoryDiv,
    newHumidityXArray,
    newHumidityYArray,
    humidity
  );
}
/*
  SocketIO Code
*/
var socket = io.connect();

//receive details from server
socket.on("update_weather", function (msg) {
  console.log(msg)
  var weather_data = JSON.parse(msg);
  updateWeatherData(weather_data);
});

socket.on("update", function (msg) {
  console.log(msg)
  var data = JSON.parse(msg);
  if (data.weather){
    updateWeatherData(data.weather);
  }
});
