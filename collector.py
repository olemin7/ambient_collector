import time
import logging
import os
import csv
import config

log = logging.getLogger('logger')

def prune(filename: str, retention_period_sec: int):
    """Remove outdated items from file."""
    if not os.path.isfile(filename):
        log.info(f"no file {filename}")
        return

    cut_ts = int(time.time()) - retention_period_sec

    kept_list = []
    fields = None
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        need_prune = False
        try:
            for row in reader:
                if row["ts"] < cut_ts:
                    need_prune = True
                else:
                    kept_list.append(row)
        except Exception as e:
            log.error(e)
            need_prune=True
        if not need_prune:
            log.debug("nothing to prune")
            return
        fields = reader.fieldnames
    if len(kept_list) == 0:
        log.debug("delete empty file")
        os.remove(filename)
        return
    tempfile = filename + ".tmp"
    with open(tempfile, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(kept_list)
    os.replace(tempfile, filename)


class Collector:
    CSV_FIELDS = ["ts", "value"]

    def __init__(self, configuration: object):
        self.__collector_dir = configuration["persistence_dir"]
        self.__fields = {}
        for thing in configuration["things"]:
            name = thing["name"]
            for parameter in thing["parameters"]:
                if "retention" in parameter and parameter["retention"]:
                    definition = {}
                    definition["retention"] = parameter["retention"]
                    self.__fields[config.get_parameter_name(name, parameter)] = definition
        log.debug(f"collected field {self.__fields}")

    @staticmethod
    def _get_cur_ts():
        return int(time.time())

    def get_cut_ts(self, key: str) -> int:
        if self.__fields[key]["retention"] == -1:
            return 0
        return self._get_cur_ts() - self.__fields[key]["retention"]

    def get_fields(self):
        return self.__fields

    def get_available_fields(self):
        """Return keys for existing files."""
        available = {}
        for key, v in self.__fields.items():
            if os.path.isfile(self.get_file_name(key)):
                ts, value = self.get_tail(key)
                if ts is not None and value is not None:
                    available[key] = v
        return available

    def get_file_name(self, key: str) -> str:
        return f"{self.__collector_dir}/{key}.csv"

    def set(self, key: str, value: object):
        if key in self.__fields:
            filename = self.get_file_name(key)
            dir_path = os.path.dirname(os.path.realpath(filename))
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
            if not os.path.isfile(filename):
                log.info(f"create {filename}")
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=Collector.CSV_FIELDS, quoting=csv.QUOTE_NONNUMERIC)
                    writer.writeheader()
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=Collector.CSV_FIELDS, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow({"ts": self._get_cur_ts(), "value": value})
        else:
            log.debug(f"out of scope {key}")

    def get_range(self, key: str, beg, end) -> list[dict]:
        log.debug(f"get_range for {key} [{beg},{end}]")
        if key in self.__fields:
            items = []
            filename = self.get_file_name(key)
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
                for row in reader:
                    ts = row["ts"]
                    if (beg is None or beg <= ts) and (end is None or end >= ts):
                        items.append(row)
                return items
        return None

    def get_tail(self, key: str):
        log.debug(f"key={key}")
        if key in self.__fields:
            filename = self.get_file_name(key)
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
                last=None
                try:
                    for row in reader:
                        last=row   #to do check on old?
                except Exception as e:
                    log.error(e)

                if last:
                    return int(last["ts"]), last["value"]
        return None, None

    def prune(self):
        for k, v in self.get_available_fields().items():
            retention = v["retention"]
            log.debug(f"prune {k}, retention {retention}")
            if retention != -1:
                prune(self.get_file_name(k), retention)


if __name__ == "__main__":
    logging.basicConfig(format=' %(levelname)s %(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)
