import time
from datetime import datetime
import logging
import os
import csv
import sys
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
        return f"{self.__collector_dir}/{key}.cvs"

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


    # def get_range(self, key: str,) -> [{}]:
    #     if key in self.__fields:
    #         item = ITEM(0,10)
    #         return [{item}]
    #     pass
    #
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
            prune(self.get_file_name(k),v["retention"])




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

#     def set_period(self, period_hours: int):
#         if self._is_finalised:
#             log.error("finalised")
#             return
#         self._period_hours = period_hours
#
#     def add_field(self, fields: set):
#         if self._is_finalised:
#             log.error("finalised")
#             return
#         self._fields.update(fields)
#
#     def finalise(self):
#         if self._is_finalised:
#             log.error("finalised")
#             return
#         self._is_finalised = True
#         log.debug(f"_filename={self._filename}, _fields={self._fields}, _period_hours={self._period_hours}")
#         dir_path = os.path.dirname(os.path.realpath(self._filename))
#         if not os.path.isdir(dir_path):
#             os.mkdir(dir_path)
#         if os.path.isfile(self._filename):
#             with open(self._filename, newline='') as csvfile:
#                 reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
#                 for row in reader:
#                     # log.debug(f"row{row}")
#                     self._data.append(row)
#                 self.__prune()
#         with open(self._filename, 'w', newline='') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=self._fields, quoting=csv.QUOTE_NONNUMERIC)
#             writer.writeheader()
#             writer.writerows(self._data)
#         log.debug(f"loaded rows={len(self._data)}")
#
#     def __prune(self):
#         cut_ts = self._get_cur_ts() - self._period_hours * 60 * 60
#         while len(self._data) and self._data[0]["ts"] < cut_ts:
#             self._data.pop(0)
#
#     def _get_cur_ts(self):
#         return int(time.time())
#
#     def add(self, value: dict):
#         if not self._is_finalised:
#             log.error("is not finalised")
#             return
#         row = value
#         row["ts"] = self._get_cur_ts()
#         self.__prune()
#         self._data.append(row)
#         if len(self._fields):
#             with open(self._filename, 'a', newline='') as csvfile:
#                 writer = csv.DictWriter(csvfile, fieldnames=self._fields, quoting=csv.QUOTE_NONNUMERIC,
#                                         extrasaction='ignore')
#                 writer.writerow(row)
#
#     def get_data(self):
#         return self._data
#
#
# def set_if_present4(to_dict: dict, to_field: str, from_dict: dict, from_field: str):
#     if from_field in from_dict:
#         to_dict[to_field] = from_dict[from_field]
#
#
# def set_if_present(to_dict: dict, to_field: str, from_dict: dict):
#     return set_if_present4(to_dict, to_field, from_dict, to_field)
#
#
# def getLastElement(vals: list, field: str):
#     for row in reversed(vals):
#         if field in row:
#             return row
#     return None
#
#
# class collector_utils:
#     def __init__(self):
#         pass
#
#     def _get_cur_ts(self):
#         return int(time.time())
#
#     def open(self, filename):
#         if os.path.isfile(filename):
#             self._filename = filename
#             return 0
#         else:
#             return 1
#
#     def info(self):
#         with open(self._filename, newline='') as csvfile:
#             reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
#             rows = 0
#             for row in reader:
#                 rows += 1
#         print(f"Fields:{reader.fieldnames}")
#         print(f"Rows:{rows}")
#
#     def prune(self, hours, field=None):
#         cut_ts = self._get_cur_ts() - hours * 60 * 60
#         with open(self._filename, newline='') as csvfile:
#             reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
#             if field and (field not in reader.fieldnames):
#                 log.error(f"no field={field} in {reader.fieldnames}")
#                 return 1
#             writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames, quoting=csv.QUOTE_NONNUMERIC)
#             writer.writeheader()
#             pruned_cnt = 0
#             total_cnt = 0
#             for row in reader:
#                 total_cnt += 1
#                 if row["ts"] < cut_ts:
#                     log.debug(f"prune={row}")
#                     pruned_cnt += 1
#                     if field:
#                         row[field] = None
#                         log.debug(f"after={row}")
#                     else:
#                         continue
#                 writer.writerow(row)
#
#         log.debug(f"pruned={pruned_cnt}/{total_cnt}")
#         return 0
#

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
