import time
from datetime import datetime
import logging
log= logging.getLogger('logger')

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

def set_if_present(to_dict, to_field, from_dict, from_field):
	if from_field in from_dict:
		to_dict[to_field]=from_dict[from_field]
		pass
	pass

def add_record(to_dict, to_field, value, period_sec):
	ts=int(time.time())
	history_data=[]
	if to_field in to_dict:
		oldest = ts - period_sec
		for el in to_dict[to_field]:
			if(el['ts']>=oldest):
				history_data.append(el)
				pass
			pass
		pass
	if value is not None:
		history_data.append(create_val(value))
		pass
	to_dict[to_field]=history_data
	pass

def get_latest_record(from_dict, from_field):
	if from_field in from_dict and len(from_dict[from_field]):
		return from_dict[from_field][-1]
	return None

def ts_to_str(ts:int):
	delta = int(time.time()) - ts;
	if delta < 60:
		return f"{delta}s"
	elif delta < 60 * 60:
		return f"{int(delta/60)}m"
	else:
		return f"{datetime.fromtimestamp(ts).strftime('%d %b %Y %H:%M')}"

def get_value(from_dict,from_field):
	res=f"{from_field}="
	if from_field in from_dict:
		if len(from_dict[from_field]) == 0:
			res=res+"empty"
		else:
			last_element = from_dict[from_field][-1]
			res=res+str(last_element["value"])
	else:
		res=res+ 'none'
	return res

def get_value_ts(from_dict,from_field):
	res=get_value(from_dict,from_field)
	if from_field in from_dict:
		if len(from_dict[from_field]) != 0:
			last_element = from_dict[from_field][-1]
			res = res + f" ({ts_to_str(last_element['ts'])})"
	return res

def add_value_dict(to_dict, to_field, from_dict, from_field, period_sec):
	if from_field in from_dict:
		add_record(to_dict, to_field, from_dict[from_field], period_sec)
		pass
	else:
		add_record(to_dict, to_field, None, period_sec)
		pass
	pass

def history_pack(from_dict,from_field,period_sec,step_sec):
	oldest=int(time.time())-period_sec
	tmp=dict()
	if from_field in from_dict:
		for el in from_dict[from_field]:
			if el['ts']>=oldest:
				index=int(el['ts']/step_sec)
				if index not in tmp:
					tmp[index]=[]
					pass
				tmp[index].append(el['val'])
				pass
			pass
		pass
	log.info("sorted", tmp)
	values=[]
	for key in tmp:
		summ=0
		accum=tmp[key]
		for val in accum:
			summ=summ+val
			pass
		values.append(summ/len(accum))
		pass
	result={'period_sec':period_sec,'step_sec':step_sec,'values':values}
	log.info( "values:", result)
	return result
