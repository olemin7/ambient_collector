const today = new Date();

var humidityHistoryDiv = document.getElementById("humidity-history");
var graphConfig = { displayModeBar: false, responsive: true,};

function temperature_history(history){
    var temperatureHistoryDiv = document.getElementById("temperature-history");
    var temperatureLayout = {
      title: {
        text: "Temperature",
      },
      font: {
        size: 14,
        color: "#7f7f7f",
      },
      colorway: ['#000000', '#808080'],
      margin: { t: 30, b: 20, l: 30, r: 20, pad: 0 },
      yaxis: {
        autorange: true,
      },
      xaxis: {
        autorange: false,
        range: [0, 23],
        type: 'linear'
      },
      showlegend:false,
    };

    var hour=today.getHours();
    var it=0
    var data_today={mode:'lines+markers'}
    data_today.x=[]
    data_today.y=[]
    var temperatures=history.values
    while(it<temperatures.length && hour>=0){
        data_today.x.push(hour)
        data_today.y.push(temperatures[it])
        hour--
        it++
    }

    var data_yesterday={mode:"lines"}
    data_yesterday.x=[]
    data_yesterday.y=[]
    hour=23
    while(it<temperatures.length && hour>=0){
        data_yesterday.x.push(hour)
        data_yesterday.y.push(temperatures[it])
        hour--
        it++
    }
    console.log(data_today)
    console.log(data_yesterday)
    Plotly.newPlot( temperatureHistoryDiv,  [data_today, data_yesterday],  temperatureLayout,  graphConfig);
}

function updateWeatherData(weather) {
  $("#temperature").html(weather.temperature.toFixed(1) + " C")
  $("#humidity").html(weather.humidity.toFixed(1) + " %")
  $("#pressure").html(weather.pressure.toFixed(0) + " mPa")

  $("#lighting").html(weather.lighting.toFixed(0) + " Lux")
  $("#battery").html(weather.battery.toFixed(2)+" V" )
  $("#rssi").html(weather.rssi)
  if (weather.history_temperature){
    temperature_history(weather.history_temperature)
  }
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
