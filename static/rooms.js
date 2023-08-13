
function getLastVal(vals) {
    if(vals.length){
        return vals[vals.length-1].value
    }else{
        return 0
    }
}

function update_room(room) {
        console.log(`temperature_${room.id}`)
     if(room.temperature){
        let temperatureDiv = document.getElementById(`temperature_${room.id}`)
        temperatureDiv.innerHTML =getLastVal(room.temperature).toFixed(1) + " C"
     }
     if(room.humidity){
       let humidityDiv = document.getElementById(`humidity_${room.id}`)
       humidityDiv.innerHTML =getLastVal(room.humidity).toFixed(1) + " %"
    }
}
/*
  SocketIO Code
*/
var socket = io.connect();

//receive details from server
socket.on("update_room", function (msg) {
  console.log(msg)
  var room = JSON.parse(msg);
  update_room(room);
});

socket.on("update", function (msg) {
  console.log(msg)
  var data = JSON.parse(msg);
  if (data.rooms){
      data.rooms.forEach((val) => {
        update_room(val);
    })
  }
});