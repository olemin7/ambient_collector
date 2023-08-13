var graphConfig = { displayModeBar: false, responsive: true,};

function ts_to_date(ts){
        date =new Date(ts*1000)
        return dateFormat(date,"isoDateTime")
}

function history_comparation(div_name, name, vals){
    var temperatureHistoryDiv = document.getElementById(div_name);
    var temperatureLayout = {
      title: {
        text: name,
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
      },
      showlegend:false,
    };

    var date= new Date()
    const today = date.getDay();
    var data_today={mode:'lines+markers'}
    date.setDate(date.getDate() - 1)
    const yesterday = date.getDay();
    data_today.x=[]
    data_today.y=[]
    var data_yesterday={mode:"lines"}
    data_yesterday.x=[]
    data_yesterday.y=[]
    vals.forEach((element) => {
        data_today.x.push(ts_to_date(element.ts))
        data_today.y.push(element.value)
        if((new Date(element.ts*1000)).getDay()==yesterday){
            data_yesterday.x.push(ts_to_date(element.ts+24*60*60))
            data_yesterday.y.push(element.value)
        }
    });
 //   console.log(data_today)
 //   console.log(data_yesterday)
    Plotly.newPlot( temperatureHistoryDiv,  [data_today, data_yesterday],  temperatureLayout,  graphConfig);
}

function history_single(div_name, name, vals){
    var layout = {
      title: {
        text: name,
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
      },
      showlegend:false,
    };

    var it=0
    var data={mode:'lines' }
    data.x=[]
    data.y=[]
    vals.forEach((element) => {
        data.x.push(ts_to_date(element.ts))
        data.y.push(element.value)
    });

    console.log(data)
    Plotly.newPlot( document.getElementById(div_name), [data],  layout,  graphConfig);
}

function getLastVal(vals) {
    if(vals.length){
        return vals[vals.length-1].value
    }else{
        return 0
    }
}

function updateWeatherData(weather) {
    if(weather.temperature){
        $("#temperature").html(getLastVal(weather.temperature).toFixed(1) + " C")
        history_comparation("temperature-history","Temperature",weather.temperature)
    }
    if(weather.humidity){
        $("#humidity").html(getLastVal(weather.humidity).toFixed(1) + " %")
    }
    if(weather.pressure){
        $("#pressure").html(getLastVal(weather.pressure).toFixed(0) + " mPa")
         history_single("pressure-history","Pressure",weather.pressure)
    }
    if(weather.lighting){
        $("#lighting").html(getLastVal(weather.lighting).toFixed(0) + " Lux")
    }
    if(weather.battery){
        $("#battery").html(getLastVal(weather.battery).toFixed(2)+" V" )
    }
}
/*
  SocketIO Code
*/
var socket = io.connect();

//receive details from server
socket.on("update_weather", function (msg) {
  console.log(msg)
  var weather = JSON.parse(msg);
  updateWeatherData(weather);
});

socket.on("update", function (msg) {
  console.log(msg)
  var data = JSON.parse(msg);
  if (data.weather){
    updateWeatherData(data.weather);
  }
});

updateWeatherData({"pressure": [{"value": 992.3433228, "ts": 1691780239}, {"value": 992.2914429, "ts": 1691781113}, {"value": 992.2445679, "ts": 1691781988}, {"value": 992.2699585, "ts": 1691782866}, {"value": 992.295166, "ts": 1691783742}, {"value": 992.2167969, "ts": 1691784619}, {"value": 992.2197876, "ts": 1691785498}, {"value": 992.1641846, "ts": 1691786376}, {"value": 992.005127, "ts": 1691787253}, {"value": 991.9840088, "ts": 1691788132}, {"value": 992.0280762, "ts": 1691789011}, {"value": 992.0081787, "ts": 1691789888}, {"value": 991.9771118, "ts": 1691790769}, {"value": 991.8626099, "ts": 1691791648}, {"value": 991.7808228, "ts": 1691792528}, {"value": 991.7034302, "ts": 1691793406}, {"value": 991.6160889, "ts": 1691794286}, {"value": 991.6082153, "ts": 1691795162}, {"value": 991.6864624, "ts": 1691796040}, {"value": 991.630188, "ts": 1691796918}, {"value": 991.6860352, "ts": 1691797798}, {"value": 991.7924805, "ts": 1691798676}, {"value": 991.739502, "ts": 1691799555}, {"value": 991.7032471, "ts": 1691800434}, {"value": 991.6633911, "ts": 1691801313}, {"value": 991.5639648, "ts": 1691802191}, {"value": 991.6320801, "ts": 1691803070}, {"value": 991.5652466, "ts": 1691803948}, {"value": 991.4779053, "ts": 1691804827}, {"value": 991.4213257, "ts": 1691805705}, {"value": 991.5597534, "ts": 1691806583}, {"value": 991.6038208, "ts": 1691807462}, {"value": 991.4214478, "ts": 1691808340}, {"value": 991.5015259, "ts": 1691809218}, {"value": 991.4853516, "ts": 1691810097}, {"value": 991.5578613, "ts": 1691810975}, {"value": 991.5098877, "ts": 1691811855}, {"value": 991.4609375, "ts": 1691812734}, {"value": 991.571106, "ts": 1691813613}, {"value": 991.4909668, "ts": 1691814493}, {"value": 991.5549927, "ts": 1691815372}, {"value": 991.6322632, "ts": 1691816249}, {"value": 991.6277466, "ts": 1691817129}, {"value": 991.6616211, "ts": 1691818007}, {"value": 991.8101196, "ts": 1691818885}, {"value": 991.7611694, "ts": 1691819766}, {"value": 991.8721313, "ts": 1691820141}, {"value": 991.7440796, "ts": 1691820166}, {"value": 991.7842407, "ts": 1691820556}, {"value": 991.7293091, "ts": 1691820566}, {"value": 991.7225342, "ts": 1691820613}], "humidity": [{"value": 47.5, "ts": 1691820613}], "temperature": [{"value": 25.5, "ts": 1691780239}, {"value": 24.89999962, "ts": 1691781113}, {"value": 24.39999962, "ts": 1691781988}, {"value": 24.29999924, "ts": 1691782866}, {"value": 23.70000076, "ts": 1691783742}, {"value": 23.29999924, "ts": 1691784619}, {"value": 23.10000038, "ts": 1691785498}, {"value": 22.89999962, "ts": 1691786376}, {"value": 22.5, "ts": 1691787253}, {"value": 22.70000076, "ts": 1691788132}, {"value": 22.79999924, "ts": 1691789011}, {"value": 22.60000038, "ts": 1691789888}, {"value": 22.29999924, "ts": 1691790769}, {"value": 23.29999924, "ts": 1691791648}, {"value": 23.79999924, "ts": 1691792528}, {"value": 24, "ts": 1691793406}, {"value": 24.10000038, "ts": 1691794286}, {"value": 23.60000038, "ts": 1691795162}, {"value": 23.70000076, "ts": 1691796040}, {"value": 22.60000038, "ts": 1691796918}, {"value": 22.10000038, "ts": 1691797798}, {"value": 22.89999962, "ts": 1691798676}, {"value": 23.39999962, "ts": 1691799555}, {"value": 23.29999924, "ts": 1691800434}, {"value": 23.20000076, "ts": 1691801313}, {"value": 23.29999924, "ts": 1691802191}, {"value": 23.39999962, "ts": 1691803070}, {"value": 23.5, "ts": 1691803948}, {"value": 23.5, "ts": 1691804827}, {"value": 23.5, "ts": 1691805705}, {"value": 23.5, "ts": 1691806583}, {"value": 23.29999924, "ts": 1691807462}, {"value": 23.20000076, "ts": 1691808340}, {"value": 23.20000076, "ts": 1691809218}, {"value": 23.10000038, "ts": 1691810097}, {"value": 22.79999924, "ts": 1691810975}, {"value": 23.39999962, "ts": 1691811855}, {"value": 23.5, "ts": 1691812734}, {"value": 23.70000076, "ts": 1691813613}, {"value": 24.20000076, "ts": 1691814493}, {"value": 24.20000076, "ts": 1691815372}, {"value": 24.10000038, "ts": 1691816249}, {"value": 24, "ts": 1691817129}, {"value": 23.79999924, "ts": 1691818007}, {"value": 24, "ts": 1691818885}, {"value": 24.60000038, "ts": 1691819766}, {"value": 25.29999924, "ts": 1691820141}, {"value": 25.20000076, "ts": 1691820166}, {"value": 25.5, "ts": 1691820556}, {"value": 25.60000038, "ts": 1691820566}, {"value": 25.60000038, "ts": 1691820613}], "battery": [{"value": 4.1484375, "ts": 1691820613}], "lighting": [{"value": 240.8333282, "ts": 1691820613}], "rssi": [{"value": -51, "ts": 1691820613}]});
