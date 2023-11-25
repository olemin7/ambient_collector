var graphConfig = { displayModeBar: false,staticPlot: true};

function history_comparation(div_name, name, vals){
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
            text: name,
        },
        autorange: true,
      },
      xaxis: {
        autorange: false,
        range:[d_start,d_end]
      },
      showlegend:false,
    };

    var date= new Date()
    const today = date.getDate();
    var data_today={mode:'lines+markers', name: 'today'}
    date.setDate(date.getDate() - 1)
    const yesterday = date.getDate();
    data_today.x=[]
    data_today.y=[]
    var data_yesterday={mode:"lines", name: 'yesterday'}
    data_yesterday.x=[]
    data_yesterday.y=[]
    vals.forEach((element) => {
        var day=(new Date(element.ts*1000)).getDate()
        console.log(day)
        if(day==today){
            data_today.x.push(ts_to_date(element.ts))
            data_today.y.push(element.value)
        }else if(day==yesterday){
            data_yesterday.x.push(ts_to_date(element.ts+24*60*60))
            data_yesterday.y.push(element.value)
        }
    });
    Plotly.newPlot( temperatureHistoryDiv,  [data_today, data_yesterday],  temperatureLayout,  graphConfig);
}

function history_double(div_name, name, vals, name2, vals2){
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
            text: name,
        },
      },
    yaxis2: {
        autorange: true,
        title: {
            text: name2,
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

    var data={mode:'lines' , name: name,}
    data.x=[]
    data.y=[]
    vals.forEach((element) => {
        data.x.push(ts_to_date(element.ts))
        data.y.push(element.value)
    });

    var data2={mode:'lines' ,name: name2, yaxis: 'y2',}
    data2.x=[]
    data2.y=[]
    vals2.forEach((element) => {
        data2.x.push(ts_to_date(element.ts))
        data2.y.push(element.value)
    });

    console.log(data)
    Plotly.newPlot( document.getElementById(div_name), [data,data2],  layout,  graphConfig);
}

function update_thing(thing) {
     if(thing.masks.indexOf("weather")!=-1){
        if(thing.temperature){
            $("#temperature").html(getLastVal(thing.temperature).toFixed(1) + " C")
            history_comparation("temperature_cmp","Temperature",thing.temperature)
        }
        if(thing.humidity){
            $("#humidity").html(getLastVal(thing.humidity).toFixed(1) + " %")
        }
        if(thing.pressure){
            $("#pressure").html(getLastVal(thing.pressure).toFixed(0) + " mPa")
        }
        if(thing.ambient_light){
            $("#ambient_light").html(getLastVal(thing.ambient_light).toFixed(0) + " Lux")
        }
        if(thing.battery){
            $("#battery").html(getLastVal(thing.battery).toFixed(0)+" %" )
        }
        if(thing.temperature && thing.pressure){
            history_double("history","Temperature",thing.temperature,"Pressure",thing.pressure)
        }
    }
}
