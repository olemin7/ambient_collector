
function update_thing(thing) {
     if(thing.masks.indexOf("room")!=-1){
        collector=thing.collector
        let temperatureDiv = document.getElementById(`temperature_${thing.id}`)
        temperatureDiv.innerHTML =to_str_temperature(getLastVal(collector,"temperature"))
        let humidityDiv = document.getElementById(`humidity_${thing.id}`)
        humidityDiv.innerHTML = to_str_humidity(getLastVal(collector,"humidity"))
    }
}
