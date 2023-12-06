import time
from datetime import datetime
import logging
import os
import csv
import json
log= logging.getLogger('logger')


class collector:
	def __init__(self,  filename:str, buff: list = []):
		self._filename = filename
		self._fields = {"ts"}
		self._data = buff
		self._is_finalised = False
		self._period_hours = 1

	def set_period(self, period_hours:int):
		if self._is_finalised :
			log.error("finalised")
			return
		self._period_hours = period_hours

	def add_field(self, fields: set):
		if self._is_finalised :
			log.error("finalised")
			return
		self._fields.update(fields)

	def finalise(self):
		if self._is_finalised :
			log.error("finalised")
			return
		self._is_finalised=True
		log.debug(f"_filename={self._filename}, _fields={self._fields}, _period_hours={self._period_hours}")
		dir_path = os.path.dirname(os.path.realpath(self._filename))
		if not os.path.isdir(dir_path):
			os.mkdir(dir_path)
		if os.path.isfile(self._filename):
			with open(self._filename, newline='') as csvfile:
				reader = csv.DictReader(csvfile, quoting = csv.QUOTE_NONNUMERIC)
				for row in reader:
					#log.debug(f"row{row}")
					self._data.append(row)
				self.__prune()
		with open(self._filename, 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=self._fields, quoting = csv.QUOTE_NONNUMERIC)
			writer.writeheader()
			writer.writerows(self._data)
		log.debug(f"loaded rows={len(self._data)}")


	def __prune(self):
		cut_ts= self._get_cur_ts() - self._period_hours * 60 * 60
		while len(self._data) and self._data[0]["ts"]<cut_ts:
			self._data.pop(0)

	def _get_cur_ts(self):
		return int(time.time())

	def add(self, value:dict):
		if not self._is_finalised :
			log.error("is not finalised")
			return
		row = value
		row["ts"] = self._get_cur_ts()
		self.__prune()
		self._data.append(row)
		if len(self._fields):
			with open(self._filename, 'a', newline='') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=self._fields, quoting = csv.QUOTE_NONNUMERIC,extrasaction='ignore')
				writer.writerow(row)

	def get_data(self):
		return self._data



def create_val(val):
	try:
		val_=int(val*100)/100
	except(ValueError,TypeError):
		val_=val
	return {'value':val_,'ts':int(time.time())}

def set_value(to_dict,to_field,from_dict,from_field):
	if from_field in from_dict:
		to_dict[to_field]=[create_val(from_dict[from_field])]
		pass
	pass

def set_if_present4(to_dict:dict, to_field:str, from_dict:dict, from_field:str):
	if from_field in from_dict:
		to_dict[to_field]=from_dict[from_field]
		pass
	pass

def set_if_present(to_dict:dict, to_field:str, from_dict:dict):
	return set_if_present4(to_dict, to_field, from_dict,to_field)

if __name__ == "__main__":
	logging.basicConfig(format=' %(levelname)s %(asctime)s:%(filename)s:%(lineno)d: %(message)s', level = logging.DEBUG)
	data=[]
	ct=collector("./test/test.csv",data)
	ct.add_field({"fld","fld2"})
	ct.set_period(24)
	ct.finalise()
	tt ={}
	tt["fld2"]="1asd11";
	tt["fld3"]="ss1asd11";

	ct.add(tt)
	print(data)
