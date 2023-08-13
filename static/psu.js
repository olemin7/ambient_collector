function ts_to_date(ts){
        date =new Date(ts*1000)
        return dateFormat(date,"isoDateTime")
}

function populate_graph(plots,values){
    plots.x=[]
    plots.y=[]
    if(values && values.length){
        var last=values[0];
        values.forEach((element) => {
            plots.x.push(ts_to_date(element.ts))
            plots.y.push(last)
            plots.x.push(ts_to_date(element.ts))
            plots.y.push(element.value)
            last=element.value
        })
        plots.x.push(ts_to_date((new Date()).getTime()/1000))
        plots.y.push(last)
    }
}

function history(vals){
    var historyDiv = document.getElementById('psu_history');
    var graphConfig = { displayModeBar: false, responsive: true,};
    var layout = {
      title: {
        text: name,
      },
      font: {
        size: 14,
        color: "#7f7f7f",
      },
      colorway: ['#00FF00', '#0000FF'],
      margin: { t: 30, b: 20, l: 30, r: 20, pad: 0 },
      yaxis: {
        autorange: true,
      },
      xaxis: {
        autorange: true,
      },
      showlegend:false,
    };

    var data_V220={mode:'lines'}
    populate_graph(data_V220,vals.V220)
    var data_BAT_OK={mode:'lines'}
    populate_graph(data_BAT_OK,vals.BAT_OK)

    Plotly.newPlot( historyDiv,  [data_V220, data_BAT_OK],  layout,  graphConfig);
}


function getLastValStr(vals) {
    if(vals.length){
        return (vals[vals.length-1].value)?"Ok":"Fail"
    }else{
        return '-'
    }
}

function update(psu) {
    if(psu.V220){
        $("#V220").html(getLastValStr(psu.V220))
    }
    if(psu.BAT_OK){
        $("#BAT_OK").html(getLastValStr(psu.BAT_OK))
    }
    history(psu)
}
/*
  SocketIO Code
*/
var socket = io.connect();

//receive details from server
socket.on("update_psu", function (msg) {
  console.log(msg)
  update(msg);
});

socket.on("update", function (msg) {
  console.log(msg)
  if (msg.psu){
    update(msg.psu);
  }
});