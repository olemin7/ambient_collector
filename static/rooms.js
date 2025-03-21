var graphConfig = { displayModeBar: false,staticPlot: false , autoscaleYAxis: true};

function history(parameter,  rooms){
    const place_holder_div = document.getElementById("id_graph_"+parameter);
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
      xaxis: {
        autorange: true,
        type: 'date'
        },
      showlegend:true,
    };

    Plotly.newPlot( place_holder_div, [],  layout,  graphConfig);
    const d_start_s=parseInt((new Date())/1000)-24*60*60*10;
    rooms.forEach((room) => {
        const key=room+"."+parameter;

        socket.emit("history",{key: key, begin:d_start_s}, (response) => {
            var data={
                name: key,
                mode:'lines',
                x:[],
                y:[]
            }
             response.forEach((element) => {
                data.x.push(ts_to_date(element.ts))
                data.y.push(element.value)
            });
            Plotly.addTraces( place_holder_div, [data]);
        });
     } );
}


function update_thing(thing) {
     if(thing.masks.indexOf("room")!=-1){
        collector=thing.collector
        let temperatureDiv = document.getElementById(`temperature_${thing.id}`)
        temperatureDiv.innerHTML =to_str_temperature(getLastVal(collector,"temperature"))
        let humidityDiv = document.getElementById(`humidity_${thing.id}`)
        humidityDiv.innerHTML = to_str_humidity(getLastVal(collector,"humidity"))
    }
}

function update_value(name,value){
     let div = document.getElementById(name)

     if(div){
        div.innerHTML = to_str_by_name(name.split(".")[1],value)
    }
}

function page_start_up(){
     console.log(rooms,graphs);
     graphs.forEach((paramentr) => {
        history(paramentr,rooms);
     } );
}