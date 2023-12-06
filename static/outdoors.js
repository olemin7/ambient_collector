var graphConfig = { displayModeBar: false,staticPlot: true};

function history_temperature_comparation(div_name, vals){
    var temperatureHistoryDiv = document.getElementById(div_name);

    var d_start = new Date();
    d_start.setUTCHours(0,0,0,0);
    var d_end = new Date();
    d_end.setUTCHours(23,59,59,999);

    var temperatureLayout = {
      font: {
        size: 14,
        color: "#7f7f7f",
      },
      colorway: ['#000000', '#808080'],
      margin: { t: 30, b: 20, l: 30, r: 20, pad: 0 },
      yaxis: {
        title: {
            text: "Температура",
        },
        autorange: true,
      },
      xaxis: {
        autorange: false,
        range:[d_start,d_end]
      },
      showlegend:true,
      legend: {
        x: 1,
        xanchor: 'right',
        y: 1
      },
    };

    var date= new Date()
    const today = date.getDate();
    var data_today={
        mode:'lines+markers',
        name:'сьогодні'
    }
    date.setDate(date.getDate() - 1)
    const yesterday = date.getDate();
    data_today.x=[]
    data_today.y=[]
    var data_yesterday={
        mode:"lines",
        name: 'вчора',
        line: {
            dash: 'dot',
        }
    }
    data_yesterday.x=[]
    data_yesterday.y=[]
    vals.forEach((element) => {
        if ("temperature" in element){
            var day=(new Date(element.ts*1000)).getDate()
            console.log(day)
            if(day==today){
                data_today.x.push(ts_to_date(element.ts))
                data_today.y.push(element.temperature)
            }else if(day==yesterday){
                data_yesterday.x.push(ts_to_date(element.ts+24*60*60))
                data_yesterday.y.push(element.temperature)
            }
        }
    });
    Plotly.newPlot( temperatureHistoryDiv,  [data_today, data_yesterday],  temperatureLayout,  graphConfig);
}

function history_wide(div_name,  vals){
    var layout = {
      font: {
        size: 14,
        color: "#7f7f7f",
      },
      colorway: ['#000000', '#808080'],
      margin: { t: 30, b: 20, l: 30, r: 20, pad: 0 },
      yaxis: {
        autorange: true,
        title: {
            text: "Температура",
        },
      },
      yaxis2: {
        autorange: true,
        title: {
            text: "Тиск",
        },
        overlaying: 'y',
        side: 'right'
      },
      xaxis: {
        autorange: true,
      },
      showlegend:true,
      legend: {
        x: 1,
        xanchor: 'right',
        y: 1
      },
    };

    var temperature={mode:'lines' , name: "Температура",}
    temperature.x=[]
    temperature.y=[]
    var pressure={mode:'lines' ,name: "Тиск", yaxis: 'y2',}
    pressure.x=[]
    pressure.y=[]

    vals.forEach((row) => {
        if("temperature" in row){
            temperature.x.push(ts_to_date(row.ts))
            temperature.y.push(row.temperature)
        }
        if("pressure" in row){
            pressure.x.push(ts_to_date(row.ts))
            pressure.y.push(row.pressure)
        }
    });
    Plotly.newPlot( document.getElementById(div_name), [temperature,pressure],  layout,  graphConfig);
}

function update_thing(thing) {
     if(thing.masks.indexOf("weather")!=-1){
        collector=thing.collector
        $("#temperature").html(to_str_temperature(getLastVal(collector,"temperature")))
        $("#humidity").html(to_str_humidity(getLastVal(collector,"humidity")))

        pressure=getLastVal(collector,"pressure")
        if (pressure!=null){
            $("#pressure").html(pressure.toFixed(0) + " mPa")
        }
        ambient_light=getLastVal(collector,"ambient_light")
        if(ambient_light!=null){
            $("#ambient_light").html(ambient_light.toFixed(0) + " Lux")
        }
        battery=getLastVal(collector,"battery")
        if(battery!=null){
            $("#battery").html(battery.toFixed(0)+" %" )
        }
        history_temperature_comparation("temperature_cmp",collector)
        history_wide("history",collector)

    }
}
