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
  //   console.log(instance.get_node(""));
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

function page_start_up(){
    $('#tree_id').jstree({ 'core' : {
        "check_callback": true,
        "animation" : 0,
        "plugins" : [ "sort" ],
    } });
    $('#tree_id').on("changed.jstree", function (e, data) {
      console.log(data.selected);
    });

}