function isElementEmpty(vals) {
    if(vals && vals.length){
        return false
    }else{
        return true
    }
}

function getLastElement(vals) {
    return vals[vals.length-1]
}

function getLastVal(vals) {
    if(isElementEmpty(vals)){
        return 0
    }
    return getLastElement(vals).value
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

/*
  SocketIO Code
*/
var socket = io.connect();

//receive details from server
socket.on("thing", function (msg) {
  console.log(msg)
  update_thing(msg);
});

socket.on("update", function (msg) {
  console.log(msg)
  if (msg.things){
      msg.things.forEach((val) => {
        update_thing(val);
    })
  }
});
