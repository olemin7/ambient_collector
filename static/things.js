
function update_thing(thing) {
    let misk=""
     if(!isElementEmpty(thing.wifi)){
        let wifi =getLastElement(thing.wifi)
        document.getElementById(`ip_${thing.id}`).innerHTML =wifi.value.ip
        document.getElementById(`rssi_${thing.id}`).innerHTML =wifi.value.rssi;
        document.getElementById(`updated_${thing.id}`).innerHTML =ts_to_passed(wifi.ts);
     }

     if(!isElementEmpty(thing.battery)){
         document.getElementById(`battery_${thing.id}`).innerHTML =getLastElement(thing.battery).value+"%"
     }
     if(thing.mqtt_period){
       misk+=" mqtt_period="+thing.mqtt_period+"c"
     }
     document.getElementById(`misk_${thing.id}`).innerHTML =misk

}