const today = new Date();
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

    var temperatures=history.values
    var hour=today.getHours();
    var it=temperatures.length
    var data_today={mode:'lines+markers'}
    data_today.x=[]
    data_today.y=[]

    while(it && hour>=0){
        data_today.x.push(hour--)
        data_today.y.push(temperatures[--it])
    }

    var data_yesterday={mode:"lines"}
    data_yesterday.x=[]
    data_yesterday.y=[]
    hour=23
    while(it && hour>=0){
        data_yesterday.x.push(hour--)
        data_yesterday.y.push(temperatures[--it])
    }
 //   console.log(data_today)
 //   console.log(data_yesterday)
    Plotly.newPlot( temperatureHistoryDiv,  [data_today, data_yesterday],  temperatureLayout,  graphConfig);
}

function history_pressure(history){
    var humidityDiv = document.getElementById("humidity-history");
    var layout = {
      title: {
        text: "Pressure",
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
        autorange: true,
        type: 'linear'
      },
      showlegend:false,
    };

    var it=0
    var data={mode:'lines+markers' }
    data.x=[]
    data.y=[]
    hour=history.values.length*-1
    while(it<history.values.length){
        data.x.push(++hour)
        data.y.push((history.values[it++]))
    }
    console.log(data)
    Plotly.newPlot( humidityDiv, [data],  layout,  graphConfig);
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
  if (weather.history_pressure){
    history_pressure(weather.history_pressure)
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

});

socket.on("update", function (msg) {
  console.log(msg)
  var data = JSON.parse(msg);
  if (data.weather){
    updateWeatherData(data.weather);
  }
});

updateWeatherData({"pressure": 973.2601318, "pressure_time": 1691392977, "history_pressure": {"period_sec": 604800, "step_sec": 3600, "values": [978.6389363666667, 978.4580688499999, 978.0746001999998, 977.7390899750001, 977.3520355249999, 976.892517075, 976.3505249250001, 975.59550475, 974.919372525, 974.3355102600001, 974.0034179500001, 973.6764221, 973.3241577250001, 973.2507019249999, 973.2289733499999]}, "temperature": 28.10000038, "temperature_time": 1691392977, "humidity": 58.79999924, "humidity_time": 1691392977, "history_temperature": {"period_sec": 172800, "step_sec": 3600, "values": [30.633333840000002, 30.17500019, 29.874999525, 29.625000475, 29.44999981, 29.25, 29.10000038, 28.874999525, 28.675000665000002, 28.560000228, 28.474999905, 29.224999904999997, 29.849999904999997, 28.724999904999997, 28.150000570000003]}, "battery": 4.144042969, "battery_time": 1691392977, "lighting": 350, "lighting_time": 1691392977, "rssi": -45, "rssi_time": 1691392977});
