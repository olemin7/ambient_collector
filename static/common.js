const PRESURE_MIN = 700
const PRESURE_MAX = 1100

function between(x, min, max) {
  return x >= min && x <= max;
}

function getLastElement(vals,field) {
    pos=vals.length
    while(pos--){
        row=vals[pos]
        if( field in row){
            return row
        }
    }
    return null
}

function getLastVal(vals,field) {
    row =getLastElement(vals,field)
    if (row){
       return row[field]
    }
    return null
}

function ts_to_date(ts){
        date =new Date(ts*1000)
        return dateFormat(date,"isoDateTime")
}

function ts_to_passed(ts){
        event_date =new Date(ts*1000)
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