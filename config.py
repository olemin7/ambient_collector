
import yaml
import logging
import os
log = logging.getLogger('logger')

def _parameters_populate(base_folder:str,thing:{}):
    log.info(f"_parameters_populate for ={thing}")
    if "file" in thing:
        parameters=[]
        with open(base_folder+ "/"+thing["file"], "r") as f:
            parameters = yaml.load(f, Loader=yaml.FullLoader)
        log.debug(f"parameters={parameters}")
        mac=thing.get("mac","")
        name = thing.get("name", "")
        for parameter in parameters:
            parameter["topic"]=parameter["topic"].format(mac=mac,name=name)
        thing["parameters"]=parameters
    else:
        log.warning(r"no parameters")

def get(config_filename:str)->{}:
    log.info(f"load config from file={config_filename}")
    config={}
    with open(config_filename, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    base_folder=os.path.dirname(config_filename)
    for thing in config["things"]:
        _parameters_populate(base_folder,thing)

    log.debug(f"config={config}")
    return  config

def get_parameter_name(thing_name:str,parameter)->str:
    return r"{thing_name}.{name}".format(thing_name=thing_name,name=parameter["name"])


def things_parameters_name(thing:object)->[str]:
    parameters_name = []
    if "parameters" in thing:
        name=thing["name"]
        for parameter in thing["parameters"]:
            parameters_name.append( get_parameter_name(name,parameter))
    return parameters_name

def get_thing_by_parameters_name(things:[{}],parameter_name:str)->{}:
    return {}


if __name__ == "__main__":
    logging.basicConfig(format=' %(levelname)s %(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)
    config=get("config/config.yaml")
    for thing in config["things"]:
        log.info(thing["name"])
        log.info(things_parameters_name(thing))
