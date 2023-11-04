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
    populate_graph(data_V220,vals)

    Plotly.newPlot( historyDiv,  [data_V220],  layout,  graphConfig);
}

function update_thing(thing) {
     if(thing.masks.indexOf("power220")!=-1){
        if(!isElementEmpty(thing.state))
            $("#V220").html(getLastElement(thing.state).value?" норма":" відсутня")
            history(thing.state)
     }
 }