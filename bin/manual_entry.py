#!/usr/bin/python
def str2time(val):
	from datetime import datetime
	def valset(val, index=None):
		if index is None:
			_x = val[-2:]
		else:
			_x = val[index - 2: index]

		if _x is None or len(_x) == 0:
			return '0'
		else:
			return _x

	val = val.replace(':','').replace('.','')

	f = valset(val)
	s = valset(val, -2)
	m = valset(val, -4)
	h = valset(val, -6)

	return datetime.strptime("{}:{}:{}.{}".format(h,m,s,f),"%H:%M:%S.%f")

all_events = [
	"50 Free", "100 Free", "200 Free", "400 Free", "800 Free", "1500 Free",
	"50 Back", "100 Back", "200 Back",
	"50 Breast", "100 Breast", "200 Breast",
	"50 Fly", "100 Fly", "200 Fly",
	"100 IM", "200 IM", "400 IM" ]

backup = 'input.txt'

def input_standard(backup_file = backup, events = all_events, delineator='', quiet=False):
	""" Create a swim time table.

	The format of the table is:
	  table = {
	    'age'    : { 'young' : int, 'old' : int },
	    'SC'     : { 'event' : { 'times' : [int], 'agediff': [int] } }
	    'LC'     : { 'event' : { 'times' : [int], 'agediff': [int] } }
	  }
	"""
	no_time = str2time('0')
	def initialize_event_times(event_list, width = None):
		new_parent = {}
		for event in event_list:
			if isinstance(width,int):
				new_parent[event] = [no_time] * width
			else:
				new_parent[event] = []
		return new_parent

	def get_age_times(event_list, backup_file=backup):
		from blessings import Terminal
		term = Terminal()
		times = {}
		for event in event_list:
			if quiet:
				input_time = input("")
			else:
				input_time = input("{: <11}: ".format(event))
			times[event] = str2time(input_time)
			if not quiet:
				if times[event] != no_time:
					print(term.move_up()  + "{: <11}: {:<12} {}".format(event, input_time, times[event].strftime("%M:%S.%f")[:-4]))

		with open(backup_file,'a+') as save:
			for event in event_list: # Insure order
				if times[event] == no_time:
					save.write("\n")
				else:
					save.write("{}\n".format(times[event].strftime("%M:%S.%f")[:-4]))
		return times

	def merge_age_times(parent, new):
		new_parent = {}
		for k in parent.keys():
			new_parent[k] = parent[k] + [ new[k] ]
		return new_parent

	def normalize_table(table):
		new_table = {}
		for event,times in table.items():
			last_time = no_time
			agediffs = [None] * len(times)
			age = 0
			for index, time in enumerate(times):
				if time == no_time:
					time = last_time
					age += 1
				else:
					age = 0
				times[index] = time
				agediffs[index] = age
				last_time = time
			new_table[event] = {'times':table[event][::-1], 'agediff':agediffs[::-1]}
		return new_table

	def show_table(table, event_key_list, delineator):
		start_age  = table['age']['young']
		finish_age = table['age']['old']

		print("Young Age{} {}".format(delineator, start_age))
		print("Old Age  {} {}".format(delineator, finish_age))
		print("")
		print("{:11}{}".format("Event", delineator), end=' ')
		for course in ['SC', 'LC']:
			for age in range(start_age, finish_age + 1):
				print("{:8}{}".format(age, delineator), end=' ')
		for course in ['SC', 'LC']:
			for age in range(start_age, finish_age + 1):
				print("{:2}{}".format(age, delineator), end=' ')
		print("")
		for event in event_key_list:
			print("{:>11}{}".format(event, delineator), end=' ')
			for course in ['SC', 'LC']:
				last_time = no_time
				for time in table[course][event]['times']:
					if time == no_time:
						time = last_time
					if time == no_time:
						print("{:8}{}".format(' ', delineator), end=' ')
					else:
						print("{}{}".format(time.strftime("%M:%S.%f")[:-4], delineator), end=' ')
					last_time = time
				last_time = no_time

			for course in ['SC', 'LC']:
				last_time = no_time
				for index, age in enumerate(table[course][event]['agediff']):
					time = table[course][event]['times'][index]
					if time == no_time:
						time = last_time
					if time == no_time:
						print("{:2}{}".format(' ', delineator), end=' ')
					else:
						print("{:2}{}".format(age, delineator), end=' ')
					last_time = time
			print("")

	table = { 'age': {}}

	if quiet:
		table['age']['old']   = int(input(""))
		table['age']['young'] = int(input(""))
	else:
		table['age']['old']   = int(input("Old Age  :"))
		table['age']['young'] = int(input("Young Age:"))

	with open(backup_file, 'w') as f:
		f.write("{}\n".format(table['age']['old']))
		f.write("{}\n".format(table['age']['young']))

	for course in ['SC', 'LC']:
		if quiet:
			answer = input( "".format(course))
		else:
			answer = input( "Enter '{}' times? (Y/n)".format(course))
		if 'n' in answer:
			with open(backup_file, 'a+') as f:
				f.write('n\n')
			table[course] = initialize_event_times(events, table['age']['old'] - table['age']['young'] + 1)
		else:
			with open(backup_file, 'a+') as f:
				f.write('y\n')
			table[course] = initialize_event_times(events)

			for age in range(table['age']['old'], table['age']['young'] - 1, -1):
				if not quiet:
					print("Aged: {}".format(age))
				table[course] = merge_age_times(table[course], get_age_times(events, backup_file))

		table[course] = normalize_table(table[course])

	show_table(table, events, delineator)


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = "Manual Swim Standard Formatter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-d', '--delineator', type=str,            default=',',         help="Character (str) to seperate columns with.")
	parser.add_argument('-b', '--backup',     type=str,            default='input.txt', help="File to store the input text into.")
	parser.add_argument('-q', '--quiet',      action='store_true',                      help="Don't put any user feed back on the terminal.")

	opt = parser.parse_args()

	input_standard(delineator=opt.delineator, backup_file=opt.backup, quiet=opt.quiet)
