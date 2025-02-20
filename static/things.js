//https://github.com/jonmiles/bootstrap-treeview
tree = [];

function add_to_tree(things_tree,name,value){
    const keys = name.split('.');
    let nodes = things_tree;
    let created_new=false
    let current=undefined;
    keys.forEach(key=>{
         current = nodes.find((element) => element.text.startsWith(key));
         console.log(nodes);
         if(!current){
            new_node={"text":key,"nodes":[]}
            nodes.push(new_node);
            current=nodes.at(-1);
            created_new=true;
         }
      nodes = current.nodes;
    });
   current.text=keys.at(-1)+" : "+value;
   console.log(value,created_new);
}

function update_thing(thing) {


}

function get_tree(){
    return tree;
}

function update_value(name,value){
    add_to_tree(tree,name,value);
 //   console.log(tree)
   //console.log(get_tree())
    $('#tree').treeview({data: get_tree()});
}
