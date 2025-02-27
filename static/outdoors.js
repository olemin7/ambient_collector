var graphConfig = { displayModeBar: false,staticPlot: true , autoscaleYAxis: true};

function history_comparation(key,  name, mark_max=false){
    function _addTraces(id, data, vals){
        vals.forEach((element) => {
            data.x.push(ts_to_date(element.ts))
            data.y.push(element.value)
        });
        Plotly.addTraces( id, [data]);
    }
    const d_start = (new Date()).setHours(0,0,0,0)
    const d_end = (new Date()).setHours(23,59,59,999)
    const yesterday = new Date(d_start - 1000*60*60*24)
    const place_holder_div = document.getElementById("id_comp_"+key);
    console.log(d_start,yesterday)

    var layout = {
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
      showlegend:true,
      legend: {
        x: 1,
        xanchor: 'right',
        y: 1
      },
    };
    Plotly.newPlot( place_holder_div,  [],  layout,  graphConfig);

    const d_start_s=parseInt(d_start/1000);
    socket.emit("history",{key: key,begin:d_start_s}, (response) => {
        var data_today={
            mode:'lines+markers',
            name:'сьогодні',
            line: {
                width: 2,
                color: 'black'
            },
            x:[],
            y:[]
        }

        _addTraces(place_holder_div, data_today, response)
    });

    socket.emit("history",{key: key,begin:d_start_s-24*60*60,end:d_start_s}, (response) => {
        var data_yesterday={
            mode:"lines",
            name: 'вчора',
            line: {
                dash: 'dot',
                width: 1,
                color: 'gray'
            },
            x:[],
            y:[]
        }
        response.forEach((element) => {
            element.ts=element.ts+24*60*60
        });
        _addTraces(place_holder_div, data_yesterday, response)
    });

    const min_max_period=d_start_s-7*24*60*60
    socket.emit("history",{key: key,begin:min_max_period,end:d_start_s,transformation:{mode:["max","min"]}}, (response) => {
        response.forEach((element) => {
            element.ts=d_start_s+(element.ts-min_max_period)%(24*60*60)
        });
        var day_max = new Map();
        var day_min = new Map();

        response.forEach((element) => {
            if((!day_max.has(element.ts))||(day_max.get(element.ts)<element.max)) {
                day_max.set(element.ts,element.max)
            }
             if((!day_min.has(element.ts))||(day_min.get(element.ts)>element.min)) {
                day_min.set(element.ts,element.min)
            }
        });

        var data_max={
            mode:"lines+text",
            name: 'макс',
            line: {
                shape: 'hv',
                dash: 'dot',
                width: 1,
                color: 'red'
            },
            x:[],
            y:[],
            text:[],
            textposition: 'top right',
        };

        var data_min={
            mode:"lines+text",
            name: 'мін',
            line: {
                shape: 'hv',
                dash: 'dot',
                width: 1,
                color: 'blue'
            },
            x:[],
            y:[],
            text:[],
            textposition: 'bottom right',
        };

        var ts_min=-1;
        var ts_max=-1;
        if(mark_max){
            ts_min=[...day_min.entries()].reduce((a, e ) => e[1] < a[1] ? e : a)[0];
            ts_max=[...day_max.entries()].reduce((a, e ) => e[1] > a[1] ? e : a)[0];
        }
        [...day_min.keys()].sort().forEach((k)=>{
            data_min.x.push(ts_to_date(k));
            const val=day_min.get(k);
            data_min.y.push(val);
            data_min.text.push(k==ts_min?val:"");
        });

        [...day_max.keys()].sort().forEach((k)=>{
            data_max.x.push(ts_to_date(k));
            const val=day_max.get(k);
            data_max.y.push(val);
            data_max.text.push(k==ts_max?val:"");
        });

        Plotly.addTraces( place_holder_div, [data_min,data_max]);
    });
}

function history(key,  name, begin ,MIN, MAX){
    const place_holder_div = document.getElementById("id_h_"+key);
    const d_start_s=parseInt((new Date())/1000)-begin;
    socket.emit("history",{key: key, begin:d_start_s, transformation:{mode:["avr"],span:30*60}}, (response) => {
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

            var data={mode:'lines'}
            data.x=[]
            data.y=[]

        response.forEach((element) => {
                if(between(element.avr, MIN, MAX)){
                    data.x.push(ts_to_date(element.ts))
                    data.y.push(element.avr)
                }else{
                    console.log(element.avr,MIN,MAX)
                }
        });
        Plotly.newPlot( place_holder_div, [data],  layout,  graphConfig);
    });

}

function history_min_max(key,  name){
    const place_holder_div = document.getElementById("id_min_max_"+key);


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

    Plotly.newPlot( place_holder_div, [],  layout,  graphConfig);

    socket.emit("history",{key: key,transformation:{mode:["avr"]}}, (response) => {
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
        Plotly.addTraces( place_holder_div, [data]);
    });
    socket.emit("history",{key: key,transformation:{mode:["min","max"],span:24*60*60}}, (response) => {
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
            ts=ts_to_date(element.ts)
            data_max.x.push(ts)
            data_max.y.push(element.max)
            data_max.text.push(element.max.toFixed(1))
            data_min.x.push(ts)
            data_min.y.push(element.min)
            data_min.text.push(element.min.toFixed(1))
        });
        Plotly.addTraces( place_holder_div, [data_min,data_max]);
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
