function history(thing){
    var historyDiv = document.getElementById('psu_history');
    var graphConfig = { displayModeBar: false, staticPlot: true,};
    var layout = {
      font: {
        size: 14,
        color: "#f0f0f0",
      },
      title: {
         text: "Мережа",
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

    var data={
        mode:'lines',
        line: {shape: 'vh'},
        type: 'scatter'
    }

    data.x=[]
    data.y=[]
    last_state=null;
    thing.collector.forEach((row) => {
        if("state" in row){
            last_state=row.state
            data.x.push(ts_to_date(row.ts))
            data.y.push(row.state)
        }
    })
    if("state"in thing){
        data.x.push(ts_to_date((new Date()).getTime()/1000))
        data.y.push(thing.state)
        if (thing.state) {
             layout.title.text="Мережа норма"
             layout.font.color="#000f00"
        }else{
                layout.title.text="Мережа відсутня"
             layout.font.color="#FF0000"
        }
    }
    Plotly.newPlot( historyDiv,  [data],  layout,  graphConfig);
}

function update_thing(thing) {
     if(thing.masks.indexOf("power220")!=-1){
        history(thing)
     }
 }