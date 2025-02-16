
import yaml
import logging
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

def get(filename:str)->{}:
    log.info(f"load config from file={filename}")
    config={}
    with open(filename, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    for thing in config["things"]:
        _parameters_populate("config",thing)

    log.debug(f"config={config}")
    return  config

def get_parameter_name(thing_name:str,parameter)->str:
    return r"{thing_name}.{name}".format(thing_name=thing_name,name=parameter["name"])


if __name__ == "__main__":
    logging.basicConfig(format=' %(levelname)s %(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)
    config=get("config/config.yaml")
    for thing in config["things"]:
        for parameter in thing["parameters"]:
            log.info(get_parameter_name(thing["name"],parameter))
