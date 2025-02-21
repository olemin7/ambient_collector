
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
}