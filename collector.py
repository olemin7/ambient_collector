import time
def update_helper4(to_dict,to_field,from_dict,from_field):
	if from_field in from_dict:
		to_dict[to_field]=from_dict[from_field]
		to_dict[to_field+"_time"]=int(time.time())
		pass
	pass

def update_helper(to_dict,from_dict,field):
	update_helper4(to_dict,field,from_dict,field)
	pass

def update_history(to_dict,to_field,from_dict,from_field,period_sec):
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
	if from_field in from_dict:
		history_data.append({'val':from_dict[from_field],'ts':ts})
		pass
	to_dict[to_field]=history_data
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
	print("sorted", tmp)
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
	print( "values:", result)
	return result
