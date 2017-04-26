#!/usr/bin/python
from __future__ import print_function
import sys

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

def format_header(minage, maxage, fh = sys.stdout):
	print ('Young Age,%d' % minage, file = fh)
	print ('Old Age,%d' % maxage, file = fh)
	print ('', file = fh)
	print ('%s,' % 'Event', end='', file = fh)
	print (*range(minage, maxage + 1)*4, sep = ',', file = fh)

def format_table(standards, age_adjust, minage, maxage, index = 0, fh = sys.stdout):
	for event in standards:
		print ('%s,' % event + ','*(maxage-minage + 1), end = '', file = fh)
		for age in range(minage, maxage + 1):
			if standards[event][age][index]:
				print (standards[event][age][index].strftime('%M:%S.%f')[:-4] + ',', end = '', file = fh)
			else:
				print (',', end = '', file = fh) 
		print (',' * (maxage-minage + 1), end = '', file = fh)
		for age in range(minage, maxage):
			print ('%d,' % age_adjust[event][age][index], end = '', file = fh)
		print ('%d' % age_adjust[event][maxage][index], file = fh)

if __name__ == "__main__":
	import argparse

	event_names = [
		'100 IM', 
		'200 IM', 
		'400 IM', 
		'50 Free',
		'100 Free',
		'200 Free',
		'400 Free',
		'800 Free',
		'1500 Free',
		'50 Fly',
		'100 Fly',
		'200 Fly',
		'50 Back',
		'100 Back',
		'200 Back',
		'50 Breast',
		'100 Breast',
		'200 Breast']

	parser = argparse.ArgumentParser(description="Format Swim Canada 'On Track' times for spreadsheet.")

	parser.add_argument('--min', action="store", type=int, dest = 'minage', help='Minimum age in the tables.')
	parser.add_argument('--max', action="store", type=int, dest = 'maxage', help='Maximum age in the tables.')
	parser.add_argument('-t', '--title', action="store_true", dest = 'title', help='Create the header for the tables.')
	parser.add_argument('--track', choices = range(1,4), type=int, dest='track', help='Create table for specific track.')
	parser.add_argument('--events', nargs='+', choices = event_names, help='Event headers.')
	parser.add_argument('--out', action="store", help="File name root to save data in. If provided, overrides '--track' option.")

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
	for event in [ event for event in event_names if event in standards]:
		standard = standards[event]
		for age in range(options.maxage, options.minage, -1):
			for index in range(0,3):
				if not standard[age - 1][index]:
					standard[age - 1][index] = standard[age][index]
					if standard[age][index]:
						age_adjust[event][age - 1][index] = age_adjust[event][age][index] + 1

	# print out
	if options.out:
		for track in range (1,4):
			filename = options.out + '-%d.csv' % track
			if options.title:
				with open(filename, 'w') as f:
					format_header(options.minage, options.maxage, fh = f)
			with open(filename, 'a+') as f:
				format_table(standards, age_adjust, options.minage, options.maxage, index=track - 1, fh = f)
	else:
		if options.title:
			format_header(options.minage, options.maxage)
		format_table(standards, age_adjust, options.minage, options.maxage, index=options.track - 1)

