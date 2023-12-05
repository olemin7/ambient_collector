ts_map = new Map();
var refresh_ts_timer=null;

function refresh_ts(){
    if(refresh_ts_timer){
        clearInterval(refresh_ts_timer)
    }
    ts_map.forEach((ts, id) => {
        document.getElementById(`updated_${id}`).innerHTML =ts_to_passed(ts);
    })

    refresh_ts_timer = setInterval(function() {
      refresh_ts();
    }, 1000);
}

function update_thing(thing) {
    let misk=""
     if(thing.wifi){
        document.getElementById(`ip_${thing.id}`).innerHTML =thing.wifi.ip
        document.getElementById(`rssi_${thing.id}`).innerHTML =thing.wifi.rssi;
     }
     if(thing.topic){
        document.getElementById(`topic_${thing.id}`).innerHTML =thing.topic
     }
     if(thing.updated){
        ts_map.set(thing.id, thing.updated);
        refresh_ts()
     }
     if(thing.upd_period){
        misk+=`період=${thing.upd_period}с`
     }
     battery=getLastVal(thing.collector,"battery")
     if(battery!=null){
         if (misk.length){
            misk+=", "
         }
         misk+=`батарея=${battery}%`
     }
     document.getElementById(`misk_${thing.id}`).innerHTML =misk
}
