
function update_thing(thing) {
     if(thing.masks.indexOf("room")!=-1){
         if(thing.temperature){
            let temperatureDiv = document.getElementById(`temperature_${thing.id}`)
            temperatureDiv.innerHTML =getLastVal(thing.temperature).toFixed(1) + " C"
         }
         if(thing.humidity){
           let humidityDiv = document.getElementById(`humidity_${thing.id}`)
           humidityDiv.innerHTML =getLastVal(thing.humidity).toFixed(1) + " %"
        }
    }
}
