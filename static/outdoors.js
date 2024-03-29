var graphConfig = { displayModeBar: false,staticPlot: true , autoscaleYAxis: true};

function history_comparation(div_name,  name, vals, field){
    var temperatureHistoryDiv = document.getElementById(div_name);

    const MIN_MAX_PERIOD_DAYS=7
    const d_start = (new Date()).setHours(0,0,0,0)
    const d_end = (new Date()).setHours(23,59,59,999)
    const yesterday = new Date(d_start - 1000*60*60*24)
    const min_max_deep= new Date(d_start - MIN_MAX_PERIOD_DAYS*1000*60*60*24)
    console.log(d_start,yesterday,min_max_deep)

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
      showlegend:true,
      legend: {
        x: 1,
        xanchor: 'right',
        y: 1
      },
    };


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

    var day_max = new Map();
    var day_min = new Map();
    vals.forEach((element) => {
        if (field in element){
            const ts=new Date(element.ts*1000)
            const value=element[field]
            if(ts>=d_start){
                data_today.x.push(ts_to_date(element.ts))
                data_today.y.push(value)
            }else{
                if(ts>=yesterday){
                data_yesterday.x.push(ts_to_date(element.ts+24*60*60))
                data_yesterday.y.push(value)
                }
                if(ts>=min_max_deep){ // do not include today
                    var hour=ts.getHours()
                    if( !day_max.has(hour) || day_max.get(hour)<value){
                        day_max.set(hour,value)
                    }
                    if( !day_min.has(hour) || day_min.get(hour)>value){
                        day_min.set(hour,value)
                    }
                }
            }
        }
    });
    var data_max={
        mode:"lines",
        name: 'макс '+MIN_MAX_PERIOD_DAYS,
        line: {
            shape: 'hv',
            dash: 'dot',
            width: 1,
            color: 'red'
        },
        x:[],
        y:[]
    }
    var data_min={
        mode:"lines",
        name: 'мін '+MIN_MAX_PERIOD_DAYS,
        line: {
            shape: 'hv',
            dash: 'dot',
            width: 1,
            color: 'blue'
        },
        x:[],
        y:[]
    }

    for (let hour = 0; hour < 24; hour++) {
        h_ts = dateFormat((new Date(d_start)).setHours(hour,0,0,0),"isoDateTime")
        if( day_max.has(hour)){
            data_max.x.push(h_ts)
            data_max.y.push(day_max.get(hour))
        }
        if( day_min.has(hour)){
            data_min.x.push(h_ts)
            data_min.y.push(day_min.get(hour))
        }

    }
    Plotly.newPlot( temperatureHistoryDiv,  [data_min,data_max,data_yesterday, data_today],  temperatureLayout,  graphConfig);
}

function history(div_name,  name, vals, field){
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
        rangeselector: {buttons: [
            {
              count: 1,
              label: '1d',
              step: 'day',
              stepmode: 'backward'
            },
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
      showlegend:false,
    };

    var data={mode:'lines'}
    data.x=[]
    data.y=[]

    vals.forEach((row) => {
        if(field in row){
            data.x.push(ts_to_date(row.ts))
            data.y.push(row[field])
        }
    });
    Plotly.newPlot( document.getElementById(div_name), [data],  layout,  graphConfig);
}

function light_integration(div_name, vals){
    const PERIOD=7*24*60*60
    const now=( new Date()).getTime()/1000
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
            text: "Світло",
        },
      },
      xaxis: {
        autorange: true,
      },
      showlegend:false,
    };

    var data_old={mode:'lines' ,
            line: {
            dash: 'dot',
        }}
    data_old.x=[]
    data_old.y=[]

    var data_cur={mode:'lines'}
    data_cur.x=[]
    data_cur.y=[]

    vals.forEach((row) => {
        if("ambient_light" in row){
            const elapsed=now-row.ts
            if(elapsed>2*PERIOD){
               //ignore
            }else{
                data_ref=(elapsed>PERIOD)?data_old:data_cur
                data_ref.x.push(ts_to_date((elapsed>PERIOD)?row.ts+PERIOD:row.ts))
                if(data_ref.y.length === 0){
                   data_ref.y.push(row.ambient_light)
                }else{
                   data_ref.y.push(data_ref.y.slice(-1)[0]+row.ambient_light)
                }
            }
        }
    });
    Plotly.newPlot( document.getElementById(div_name), [data_old, data_cur],  layout,  graphConfig);
}

function update_thing(thing) {
     if(thing.masks.indexOf("weather")!=-1){
        collector=thing.collector
        $("#temperature").html(to_str_temperature(getLastVal(collector,"temperature")))
        $("#humidity").html(to_str_humidity(getLastVal(collector,"humidity")))
        $("#pressure").html(to_str_pressure(getLastVal(collector,"pressure")))
        $("#ambient_light").html(to_str_ambient_light(getLastVal(collector,"ambient_light")))
        $("#battery").html(to_str_percent(getLastVal(collector,"battery"),0))

        history_comparation("id_h_temperature_cmp", "Температура", collector,"temperature")
        history_comparation("id_h_light_cmp", "Освітлення", collector,"ambient_light")
        history("id_h_temperature","Температура", collector,"temperature")
        history("id_h_presure","Тиск", collector,"pressure")
        history("id_h_light","Освітлення", collector,"ambient_light")
   //     light_integration("id_h_light", collector)
    }
}
