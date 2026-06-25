var graphConfig = { displayModeBar: false,staticPlot: true , autoscaleYAxis: true};

// has_data, hide_graph_block and history_comparation are defined in common.js (shared).

function history(key,  name, begin ,MIN, MAX){
    const place_holder_div = document.getElementById("id_h_"+key);
    const d_start_s=parseInt((new Date())/1000)-begin;
    socket.emit("history",{key: key, begin:d_start_s, transformation:{mode:["avr"],span:30*60}}, (response) => {
        if(!has_data(response)){
            hide_graph_block(place_holder_div);
            return;
        }
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
              showlegend:false,
            };

            var data={
            mode:'lines',
            x:[],
            y:[],
            line: {shape: 'spline'},
            }


        response.forEach((element) => {
                if(between(element.avr, MIN, MAX)){
                    data.x.push(ts_to_date(element.ts))
                    data.y.push(element.avr)
                }else{
                    console.log(element.avr,MIN,MAX)
                }
        });
        if(data.x.length === 0){
            hide_graph_block(place_holder_div);
            return;
        }
        Plotly.newPlot( place_holder_div, [data],  layout,  graphConfig);
    });

}

function history_min_max(key,  name){
    const place_holder_div = document.getElementById("id_min_max_"+key);
    let plot_created = false;
    let pending = 2; // avr + min/max requests


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
      showlegend:false,
    };

    function ensure_plot(){
        if(!plot_created){
            Plotly.newPlot( place_holder_div, [],  layout,  graphConfig);
            plot_created = true;
        }
    }

    function request_done(){
        pending -= 1;
        if(pending === 0 && !plot_created){
            hide_graph_block(place_holder_div);
        }
    }

    socket.emit("history",{key: key,transformation:{mode:["avr"]}}, (response) => {
        if(!has_data(response)){
            request_done()
            return
        }
        var data={
            mode:'lines',
            line: {dash: 'dot', width: 1},
            x:[],
            y:[]
        }
         response.forEach((element) => {
            data.x.push(ts_to_date(element.ts))
            data.y.push(element.avr)
        });
        ensure_plot();
        Plotly.addTraces( place_holder_div, [data]);
        request_done()
    });
    socket.emit("history",{key: key,transformation:{mode:["min","max"],span:24*60*60}}, (response) => {
        if(!has_data(response)){
            request_done()
            return
        }
        var data_max={
            mode:"lines+text",
            name: 'макс',
            line: {
                shape: 'hv',
                color: 'red'
            },
            x:[],
            y:[],
            text:[],
            textposition: 'top right',
        }
        var data_min={
            mode:"lines+text",
            name: 'мін',
            line: {
                shape: 'hv',
                color: 'blue'
            },
            x:[],
            y:[],
            text:[],
            textposition: 'bottom right',
        }
         response.forEach((element) => {
            let ts=ts_to_date(element.ts)
            data_max.x.push(ts)
            data_max.y.push(element.max)
            data_max.text.push(element.max.toFixed(1))
            data_min.x.push(ts)
            data_min.y.push(element.min)
            data_min.text.push(element.min.toFixed(1))
        });
        ensure_plot();
        Plotly.addTraces( place_holder_div, [data_min,data_max]);
        request_done()
    });
}

function light_integration(div_name, vals, field){
     var layout = {
     title: "Освітлення",
     font: {
        size: 14,
        color: "#7f7f7f",
     },
     colorway: ['#000000', '#808080'],
     margin: { t: 30, b: 20, l: 30, r: 20, pad: 0 },
     yaxis: {
        autorange: true,
     },
     yaxis2: {
        autorange: true,
        overlaying: 'y',
     },
    xaxis: {
        autorange: true,
        rangeselector: {buttons: [
        {
        count: 7,
        label: 'week',
        step: 'day',
        stepmode: 'backward'
        },
        {step: 'all'}
        ]},
        type: 'date'
    },
    showlegend: false,
    };

    var data={
        mode:'lines',
        x:[],
        y:[],
        }

    var day_symm = new Map();
    vals.forEach((row) => {
        if(field in row){
            var ts = ts_to_date(row.ts);
            var value = row[field]
            data.x.push(ts)
            data.y.push(value)
            var h_ts = dateFormat((new Date(ts)).setHours(12,0,0,0),"isoDateTime")
            var summ = day_symm.has(h_ts)?day_symm.get(h_ts):0;
            day_symm.set(h_ts,summ+value)
        }
    });

    var data_symm = {
        type: 'bar',
        name: 'макс',
        opacity: 0.5,
        x:[],
        y:[],
        yaxis: 'y2',
    }

    day_symm.forEach((value, key) => {
       data_symm.x.push(key)
       data_symm.y.push(value)
    })

    Plotly.newPlot( document.getElementById(div_name), [ data_symm, data],  layout,  graphConfig);
}

function update_thing(thing) {
}

function update_value(name,value){
     let div = document.getElementById(name);
     if(div){
        div.innerHTML = to_str_by_name(name.split(".")[1],value);
    }
}

function page_start_up(){
    history_comparation("outdoor.temperature", "Температура", true);
    history_comparation("outdoor.light", "Освітлення");
    history_min_max("outdoor.temperature", "Температура");
    history("outdoor.pressure", "Тиск", 7*24*60*60, PRESURE_MIN, PRESURE_MAX);
}
