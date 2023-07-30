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
