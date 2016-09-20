#!/usr/bin/python

def festival(filename, columns = 5):
	with open(filename, 'r') as standard:
		for line in standard:
			times = line.split()
			length = len(times)
			if length != 3:
				half = length / 2
				header = [times[half - 1] + ' ' + times[half]]
				lc_times = times[:half-1]
				sc_times = times[half + 1:]
				sc_times.reverse()
				filler = [''] * (columns - len(lc_times))
				new_times = header + filler + sc_times + filler + lc_times
			else:
				lc_times = [''] * columns
				filler = [''] * (columns - 1)
				sc_times = [times[2]]
				new_times = [ times[0] + ' ' + times[1]] + sc_times + filler + lc_times
			print ','.join(map(str, new_times))

def regional(filename, columns = 6):
	def regional_formatter(header, times):
		if len(times) == 1:
			print header + "," + times[0]
		else:
			column_count = len(times) // 2
			sc_times, lc_times = [times[x:x+column_count] for x in xrange(0, len(times), column_count)]
			filler = ['']  * (columns - column_count)
			new_times = [header] + filler + sc_times + filler + lc_times
			print ','.join(map(str, new_times))
	
	header = None
	with open(filename, "r") as standard:
		for line in standard:
			import re
			if re.search('[a-zA-Z]', line):
				if header:
					regional_formatter(header, times)
				header = line.strip()
				times = []
			else:
				times.append(line.strip())

if __name__ == "__main__":
	import sys
	if len(sys.argv) == 3:
		import os
		fn = sys.argv[1]
		if os.path.isfile(fn):
			if "regional" in sys.argv[2]:
				regional(fn)
			elif any(st in sys.argv[2] for st in ["festival", "provincial"]):
				festival(fn)
	else:
		print 'Usage:'
		print ' {0} {{filename}} {{formater}}'
		print 'Where "formatter" is one of "regional", "festival", "provincial".'
