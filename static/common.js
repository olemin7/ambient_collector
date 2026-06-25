const PRESURE_MIN = 700
const PRESURE_MAX = 1100

function between(x, min, max) {
  return x >= min && x <= max;
}

function getLastElement(vals,field) {
    let pos=vals.length
    while(pos--){
        let row=vals[pos]
        if( field in row){
            return row
        }
    }
    return null
}

function getLastVal(vals,field) {
    let row =getLastElement(vals,field)
    if (row){
       return row[field]
    }
    return null
}

function ts_to_date(ts){
        let date =new Date(ts*1000)
        return dateFormat(date,"isoDateTime")
}

function ts_to_passed(ts){
        let event_date =new Date(ts*1000)
        const passed =(Date.now()-event_date)/1000;
        if(5>passed){
            return "щойно"
        }else
        if(60>passed){
            return parseInt(passed)+"c"
        }else
        if(60*60>passed){
            return parseInt(passed/60)+"хв"
        }else
         if(12*60*60>passed){
            return parseInt(passed/60/60)+"г"
        }
        return dateFormat(event_date,"isoDateTime")
}

function to_str_temperature(temperature){
    if(temperature==null){
        return 'null'
    }
    return temperature.toFixed(1) + "&degC"
}

function to_str_percent(percent, round){
    if(percent==null){
        return 'null'
    }
    return percent.toFixed(round) + "%"
}

function to_str_humidity(humidity){
    return to_str_percent(humidity,1)
}

function to_str_pressure(pressure){
    if(pressure==null){
        return 'null'
    }
    return pressure.toFixed(0) +" mPa"
}

function to_str_ambient_light(ambient_light){
    if(ambient_light==null){
        return 'null'
    }
    return ambient_light.toFixed(0) +" Lux"
}

function to_str_by_name(name,value){
    if( name == "temperature"){
        return to_str_temperature(value)
    }
    if( name == "humidity"){
        return to_str_humidity(value)
    }
    return value
}


/*
  Shared graph helpers (used by outdoors and rooms pages)
*/

// True when the history response actually contains rows to plot.
function has_data(response){
    return Array.isArray(response) && response.length > 0;
}

// Hide the placeholder div together with its divider when no graph is drawn.
function hide_graph_block(place_holder_div){
    if(!place_holder_div){
        return;
    }
    const row = place_holder_div.closest(".row") || place_holder_div;
    row.style.display = "none";
    const prev = row.previousElementSibling;
    if(prev && prev.classList && prev.classList.contains("divider")){
        prev.style.display = "none";
    }
}

// Comparison graph: today vs yesterday vs 7-day min/max band for a given key.
// Renders into the div with id "id_comp_<key>" and hides the block if no data.
function history_comparation(key,  name, mark_max=false){
    const place_holder_div = document.getElementById("id_comp_"+key);
    let plot_created = false;
    let pending = 3; // today + yesterday + min/max requests

    const d_start = (new Date()).setHours(0,0,0,0)
    const d_end = (new Date()).setHours(23,59,59,999)
    const yesterday = new Date(d_start - 1000*60*60*24)
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

    function ensure_plot(){
        if(!plot_created){
            Plotly.newPlot( place_holder_div,  [],  layout,  graphConfig);
            plot_created = true;
        }
    }

    // After every request resolves, hide the block if nothing was ever plotted.
    function request_done(){
        pending -= 1;
        if(pending === 0 && !plot_created){
            hide_graph_block(place_holder_div);
        }
    }

    function _addTraces(id, data, vals){
        if(has_data(vals)){
            ensure_plot();
            vals.forEach((element) => {
                data.x.push(ts_to_date(element.ts))
                data.y.push(element.avr)
            });
            Plotly.addTraces( id, [data]);
        }
    }

    // Average raw samples into 5-minute buckets to keep the trace light.
    const comp_span = 5*60;
    const d_start_s=parseInt(d_start/1000);
    socket.emit("history",{key: key,begin:d_start_s,transformation:{mode:["avr"],span:comp_span}}, (response) => {
        var data_today={
            mode:'lines+markers',
            name:'сьогодні',
            line: {
                width: 2,
                color: 'black',
                shape: 'spline',
            },
            x:[],
            y:[]
        }

        _addTraces(place_holder_div, data_today, response)
        request_done()
    });

    socket.emit("history",{key: key,begin:d_start_s-24*60*60,end:d_start_s,transformation:{mode:["avr"],span:comp_span}}, (response) => {
        var data_yesterday={
            mode:"lines",
            name: 'вчора',
            line: {
                dash: 'dot',
                width: 1,
                color: 'gray',
                shape: 'spline',
            },
            x:[],
            y:[]
        }
        if(has_data(response)){
            response.forEach((element) => {
                element.ts=element.ts+24*60*60
            });
        }
        _addTraces(place_holder_div, data_yesterday, response)
        request_done()
    });

    const min_max_period=d_start_s-7*24*60*60
    socket.emit("history",{key: key,begin:min_max_period,end:d_start_s,transformation:{mode:["max","min"]}}, (response) => {
        if(!has_data(response)){
            request_done()
            return
        }
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
        // Bucket span used by the min/max request (default transformation span).
        const mm_step = 60*60;

        const min_keys=[...day_min.keys()].sort((a,b)=>a-b);
        min_keys.forEach((k)=>{
            data_min.x.push(ts_to_date(k));
            const val=day_min.get(k);
            data_min.y.push(val);
            data_min.text.push(k==ts_min?val:"");
        });
        // With shape 'hv' the value at each point is drawn horizontally up to the
        // NEXT point, so the last hour would otherwise have no horizontal segment.
        // Repeat the final value one step later so the last hour is drawn as a line.
        if(min_keys.length){
            const last=min_keys[min_keys.length-1];
            data_min.x.push(ts_to_date(last+mm_step));
            data_min.y.push(day_min.get(last));
            data_min.text.push("");
        }

        const max_keys=[...day_max.keys()].sort((a,b)=>a-b);
        max_keys.forEach((k)=>{
            data_max.x.push(ts_to_date(k));
            const val=day_max.get(k);
            data_max.y.push(val);
            data_max.text.push(k==ts_max?val:"");
        });
        if(max_keys.length){
            const last=max_keys[max_keys.length-1];
            data_max.x.push(ts_to_date(last+mm_step));
            data_max.y.push(day_max.get(last));
            data_max.text.push("");
        }

        ensure_plot();
        Plotly.addTraces( place_holder_div, [data_min,data_max]);
        request_done()
    });
}


/*
  SocketIO Code
*/
console.log('SocketIO')
var socket = io.connect();

socket.on("current_data", function (msg) {
    console.log(msg)
    for (const thing in msg) {
        for (const val in msg[thing]) {
            update_value(`${thing}.${val}`,msg[thing][val])
        }
    }
});

socket.on("event", function (msg) {
  console.log(msg)
  update_value(msg.name,msg.value)
});

console.log('page_start_up')
page_start_up();