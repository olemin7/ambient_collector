import time
import logging
import os
import csv
import config
import pytest

log = logging.getLogger('logger')

def prune(filename:str, retention_period_sec:int):
    """
    remove outdated items from file
    """
    if not os.path.isfile(filename):
        log.info(f"no file{filename}")
        return

    cut_ts=int(time.time())-retention_period_sec

    pruned_list=[]
    fields=None
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        need_prune = False
        for row in reader:
            if row["ts"]<cut_ts:
                need_prune=True
            else:
                pruned_list.append(row)
        if not need_prune:
            log.debug(f"nothing to prune")
            return
        fields=reader.fieldnames
    tempfile=filename+".tmp"
    with open(tempfile, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(pruned_list)
    os.remove(filename)
    os.rename(tempfile, filename)



class COLLECTOR:
    CVS_FIELDS=["ts","value"]
    def __init__(self, configuration:object):
        self.__collector_dir = configuration["persistence_dir"]
        self.__fields ={}
        for thing in configuration["things"]:
            name = thing["name"]
            for parameter in thing["parameters"]:
                if "retention" in parameter and parameter["retention"]:
                    definition={}
                    definition["retention"]=parameter["retention"]
                    self.__fields[config.get_parameter_name(name,parameter)]=definition
        log.debug(f"collected field{self.__fields}")

    @staticmethod
    def _get_cur_ts():
        return int(time.time())

    def get_cut_ts(self,key:str)->int:
        if self.__fields[key]["retention"]==-1:
            return 0
        return _get_cur_ts() - self.__fields[key]["retention"]

    def get_fields(self):
        return self.__fields

    def get_available_fields(self):
        """
        return keys for exiting file
        """
        available={}
        for key,v in self.__fields.items():
            if os.path.isfile(self.get_file_name(key)):
                available[key]=v
        return available

    def get_file_name(self, key:str)->str:
        return f"{self.__collector_dir}/{key}.csv"

    def set(self, key:str, value:object):
        if key in self.__fields:
            filename=self.get_file_name(key)
            dir_path = os.path.dirname(os.path.realpath(filename))
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
            if not os.path.isfile(filename):
                log.info(f"create {filename}")
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=COLLECTOR.CVS_FIELDS, quoting=csv.QUOTE_NONNUMERIC)
                    writer.writeheader()
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=COLLECTOR.CVS_FIELDS, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow({"ts":self._get_cur_ts(),"value":value})
        else:
            log.debug(f"out of scope {key}")

    def get_range(self, key: str, beg, end) -> [{}]:
        log.debug(f"get_range for{key} [{beg},{end}]")
        if key in self.__fields:
            items=[]
            filename = self.get_file_name(key)
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
                for row in reader:
                    ts=row["ts"]
                    if (beg is None or beg <=ts) and (end is None or end>=ts):
                        items.append(row)
                    last = row  # to do check on old?
                return items
        return None

    def get_tail(self, key: str):
        if key in self.__fields:
            filename = self.get_file_name(key)
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
                last=None
                for row in reader:
                    last=row   #to do check on old?
                return int(last["ts"]),last["value"]
        return None

    def prune(self):
        for k,v in self.get_available_fields().items():
            retention=v["retention"]
            log.debug(f"prune {k}, retention {retention}")
            if retention!=-1:
              prune(self.get_file_name(k),retention)




if __name__ == "__main__":
    logging.basicConfig(format=' %(levelname)s %(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)

@pytest.fixture
def default_cfg():
    parameters=[{ "name": "par0"},{ "name": "pers0","retention":100}]
    things=[{"name":"name0","parameters": parameters}]

    cfg= {"persistence_dir": "./test",
          "things": things
          }

    return cfg

def test_basic(default_cfg):

    collector=COLLECTOR(default_cfg)
    print(collector)

def test_write_new(default_cfg):

    collector=COLLECTOR(default_cfg)
    collector.set()
    print(collector)

# if __name__ == "__main__":
#     import argparse
#
#     logging.basicConfig(format=' %(levelname)s %(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)
#     arg_parse = argparse.ArgumentParser()
#     arg_parse.add_argument('filename')
#     arg_parse.add_argument('-p', '--prune', metavar='N', type=int, help='prune after days')
#     arg_parse.add_argument('-f', '--field', default=None, help='field name to prune, or all if none')
#     args = arg_parse.parse_args()
#     log.debug(args)
#     pruner = collector_utils()
#     if (pruner.open(args.filename)):
#         exit(1)
#     if (args.prune is not None):
#         exit(pruner.prune(args.prune * 24, args.field))
#
#     pruner.info()
