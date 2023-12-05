function history(vals){
    var historyDiv = document.getElementById('psu_history');
    var graphConfig = { displayModeBar: false, responsive: true,};
    var layout = {
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

    var data={
        mode:'lines',
        line: {shape: 'vh'},
        type: 'scatter'
    }

    data.x=[]
    data.y=[]
    last_state=null;
    vals.forEach((row) => {
        if("state" in row){
            last_state=row.state
            data.x.push(ts_to_date(row.ts))
            data.y.push(row.state)
        }
    })
    if(last_state!=null){
        data.x.push(ts_to_date((new Date()).getTime()/1000))
        data.y.push(last_state)
    }

    Plotly.newPlot( historyDiv,  [data],  layout,  graphConfig);
}

function update_thing(thing) {
     if(thing.masks.indexOf("power220")!=-1){
        collector=thing.collector
        state=getLastVal(collector,"state")
        $("#V220").html((state==null)?"null":(state ?" норма":" відсутня"))
        history(collector)
     }
 }