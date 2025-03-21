function add_to_tree_(name,value){
    const keys = name.split('.');
    const instance=$('#tree_id').jstree(true) ;// Get the jsTree instance

    if (instance.get_node(name)===false){
      let node_id="";
      let par_id="#"
      keys.forEach(key=>{
        node_id=node_id+key;
        node=instance.get_node(node_id);
        if (node===false){
            console.log({"par_id":par_id,"id":node_id, "text":key});
            console.log(instance.create_node(par_id,{id:node_id, text:key}));
            console.log(instance.last_error());
        }
        par_id=node_id;
        node_id=node_id+"."
      });
      instance.hide_icon(name);
    }
    instance.rename_node(name, keys.at(-1)+" : "+value);
}


function update_value(name,value){
    if (typeof value === 'object'){
        for (const [k, v] of Object.entries(value)) {
           add_to_tree_(name+"."+k,v);
        }
    }else{
      add_to_tree_(name,value);
    }
}


var graphConfig = { displayModeBar: false,staticPlot: false , autoscaleYAxis: true};

function history(parameters){
    const place_holder_div = document.getElementById("id_graphs");
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
        type: 'date'
        },
      showlegend:true,
    };

    Plotly.newPlot( place_holder_div, [],  layout,  graphConfig);
    parameters.forEach((key) => {
        socket.emit("history",{key: key}, (response) => {
            if(response!=undefined){
                var data={
                    name: key,
                    mode:'lines',
                    x:[],
                    y:[]
                }
                 response.forEach((element) => {
                    data.x.push(ts_to_date(element.ts))
                    data.y.push(element.value)
                });
                Plotly.addTraces( place_holder_div, [data]);
            }
        });
     } );
}

function page_start_up(){
    $('#tree_id').jstree({ 'core' : {
        "check_callback": true,
        "animation" : 0,
        "plugins" : [ "sort" ],
    } });
    $('#tree_id').on("changed.jstree", function (e, data) {
      console.log(data.selected); ///todo optimasation
      history(data.selected);
    });
}