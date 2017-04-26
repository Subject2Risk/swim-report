#!/usr/bin/python
from __future__ import print_function

def line_split(headers, line):
	import re
	regex = ur"(\d{2}) (?=\d{2}( |$))"
	subst = ur"\g<1>,"
	events = re.sub(regex, subst, line.strip()).split(',')

	if len(headers) != len(events):
		import sys
		print ('Mismatched data!')
		sys.exit(-1)

	data = {}
	for i in range(0,len(events)):
		event = events[i]
		header = headers[i]

		values = event.strip().split(' ')
		age, times = int(values[0]), convert_times([None]*(4 - len(values)) + values[1:])

		yield header, age, times

def convert_times(times):
	new_times = []
	for strtime in times:
		if strtime:
			import re, datetime
			arrtime = map(int, re.findall(r'[\d]+', strtime))
			arrtime[-1] *= 10000
			arrtime = [0] + arrtime
			if len(arrtime) < 4:
				arrtime = [0] + arrtime
			new_times.append(datetime.time(*arrtime))
		else:
			new_times.append(None)
	return new_times

def print_header(minage, maxage):
	print ('Young Age,%d' % minage)
	print ('Old Age,%d' % maxage)
	print ('')
	print ('%s,' % 'Event', end='')
	print (*range(minage, maxage + 1)*4, sep = ',')

def print_table(standards, age_adjust, minage, maxage, index = 0):
	for event in standards:
		print ('%s,' % event + ','*(maxage-minage + 1), end = '')
		for age in range(minage, maxage + 1):
			if standards[event][age][index]:
				print (standards[event][age][index].strftime('%M:%S.%f')[:-4] + ',', end = '')
			else:
				print (',', end = '') 
		print (',' * (maxage-minage + 1), end = '')
		for age in range(minage, maxage):
			print ('%d,' % age_adjust[event][age][index], end = '')
		print ('%d' % age_adjust[event][maxage][index])

if __name__ == "__main__":
	import sys
	import argparse

	parser = argparse.ArgumentParser(description="Format Swim Canada 'On Track' times for spreadsheet.")

	parser.add_argument('--min', action="store", type=int, dest = 'minage', help='Minimum age in the tables.')
	parser.add_argument('--max', action="store", type=int, dest = 'maxage', help='Maximum age in the tables.')
	parser.add_argument('-t', '--title', action="store_true", dest = 'title', help='Create the header for the tables.')
	parser.add_argument('--track', choices = range(1,4), type=int, dest='track', help='Create table for specific track.')
	parser.add_argument('--events', nargs='+', help='Event headers.')

	options = parser.parse_args()

	standards = {}
	age_adjust = {}

	for line in sys.stdin:
		for event, age, times in line_split(options.events, line):
			if event in standards:
				standards[event][age] = times
				age_adjust[event][age] = [0] * len(times)
			else:
				standards[event] = { age : times }
				age_adjust[event] = { age: [0] * len(times) }

	# pad the times for younger ages.
	for event in standards:
		standard = standards[event]
		for age in range(options.maxage, options.minage, -1):
			for index in range(0,3):
				if not standard[age - 1][index]:
					standard[age - 1][index] = standard[age][index]
					if standard[age][index]:
						age_adjust[event][age - 1][index] = age_adjust[event][age][index] + 1

	# print out
	if options.title:
		print_header(options.minage, options.maxage)
	print_table(standards, age_adjust, options.minage, options.maxage, index=options.track - 1)

