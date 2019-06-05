#!/usr/bin/python

def age_adjustment(fill_width, column_count):
	if fill_width > 0:
		age_adjust = []
		for age in range(fill_width, 0, -1):
			age_adjust.append(age)
		for age in range(0, column_count):
			age_adjust.append(0)
		return age_adjust
	else:
		return [0] * column_count

def age_header(start_age, columns, delimiter, short_and_long = True):
	print 'Young Age{0}{1}'.format(delimiter,start_age)
	print 'Old Age{0}{1}'.format(delimiter,start_age + columns - 1)
	age_line = '\nEvent'
	if short_and_long: 
		end_range = 4
	else:
		end_range = 2
	for course in range(0,end_range):
		for age in range(start_age, start_age + columns):
			age_line += '{0}{1}'.format(delimiter,age)
	print age_line

def event_name(abbrv):
	return {
		'BK'       : 'Back',
		'BACK'     : 'Back',
		'DOS'      : 'Back',
		'FL'       : 'Fly',
		'FLY'      : 'Fly',
		'PAPILLON' : 'Fly',
		'BRASSE'   : 'Breast',
		'BREAST'   : 'Breast',
		'BR'       : 'Breast',
		'LIBRE'    : 'Free',
		'FR'       : 'Free',
		'FREE'     : 'Free',
		'QNI'      : 'IM',
		'IM'       : 'IM'
	}[abbrv.upper()]

def fnq(filename, columns = 8, delimiter = ','):
	with open(filename, 'r') as standard:
		for line in standard:
			data = line.split()
			header = ['{0:>6}'.format(data[0]) + ' ' + event_name(data[1])]
			times = data[2:]
			length = len(times)
			if columns == 11:
				if length == 1:
					times = ['        '] * 10 + times
				elif length == 2:
					times.insert(1,'        ')
					times.insert(1,'        ')
					times.insert(1,'        ')
					times.insert(1,'        ')
					times.insert(1,'        ')
					times.insert(1,'        ')
					times = ['        '] * 3 + times
				elif length == 3:
					times = times + ['        '] * 8
				elif length == 6:
					times.insert(3,'        ')
					times.insert(3,'        ')
					times.insert(3,'        ')
					times.insert(3,'        ')
					times.insert(3,'        ')
				elif length == 8:
					times = ['        '] * 3 + times
				elif length == 9:
					times = ['        '] * 2 + times
			else:
				if length == 2:
					times.insert(1,'        ')
					times.insert(1,'        ')
					times.insert(1,'        ')
					times.insert(1,'        ')
					times.insert(1,'        ')
					times.insert(1,'        ')
				elif length == 3:
					times = ['        '] * 5 + times
				elif length == 7:
					times = ['        '] + times
				times = ['        '] * 3 + times
			print delimiter.join(map(str, header + times))


provincial_standards = {
	"festival"      : { 'columns' : 4, 'start_age' : 10 },
	"championships" : { 'columns' : 4, 'start_age' : 14 },
	"youth-junior"  : { 'columns' : 5, 'start_age' : 13 },
	"nova-scotia"   : { 'columns' : 6, 'start_age' : 12 }
}

def festival(filename, columns = 4, start_age=10, delimiter = ','):
	age_header(start_age, columns, delimiter)

	with open(filename, 'r') as standard:
		for line in standard:
			times = line.split()
			length = len(times)
			if length != 3:
				half = length / 2
				header = [times[half - 1] + ' ' + event_name(times[half])]
				lc_times = times[:half-1]
				sc_times = times[half + 1:]
				sc_times.reverse()
				fill_width = columns - len(lc_times)
				lc_filler = [lc_times[0]] * fill_width
				sc_filler = [sc_times[0]] * fill_width
				age_adjust = age_adjustment(fill_width, len(lc_times))
				new_times = header + sc_filler + sc_times + lc_filler + lc_times + age_adjust + age_adjust
			else:
				lc_times = [''] * columns
				filler = [''] * (columns - 1)
				sc_times = [times[2]]
				age_adjust = [0] + [''] * (columns * 2 - 1)
				new_times = [ times[0] + ' ' + times[1]] + sc_times + filler + lc_times + age_adjust
			print delimiter.join(map(str, new_times))

def regional(filename, columns = 6, start_age = 10, delimiter = ','):
	def regional_formatter(distance, event, times):
		field_count = len(times)
		if field_count == 1:
			csv_times = ',{}'.format(times[0]) + ',' * (columns * 2 - field_count)
			age_adjustments = '0' + ',' * (columns * 2 - field_count)
		else:
			event_count = field_count // 2
			csv_times  = ',{}'.format(times[event_count]) * (columns - event_count)
			csv_times += ',' + ','.join(times[event_count:])
			csv_times += ',{}'.format(times[0]) * (columns - event_count)
			csv_times += ',' + ','.join(times[:event_count])
			age_adjustments = ','.join(map(str,age_adjustment(columns - event_count, event_count) * 2))
		print '{} {}{},{}'.format(distance, event, csv_times, age_adjustments)

	age_header(start_age, columns, delimiter)

	header = None
	with open(filename, "r") as standard:
		for line in standard:
			fields = line.split()
			regional_formatter(fields[0], fields[1], fields[2:])

national_standards = { 
	"trials":	{ 'max_age': 17, 'min_age' : 15, 'columns' : [0,1,2]},
	"csc":  	{ 'max_age': 19, 'min_age' : 19, 'columns' : [3]},
	"cjc":  	{ 'max_age': 17, 'min_age' : 14, 'columns' : [4,5,6,7]},
	"easterns":	{ 'max_age': 17, 'min_age' : 14, 'columns' : [8,10,11,12]},
	"westerns":	{ 'max_age': 17, 'min_age' : 14, 'columns' : [9,10,11,12]}
}

def national(filename, delimiter = ',', standard='easterns', male=True):
	with open(filename, 'r') as standards:
		ns = national_standards[standard]
		column_count = len(ns['columns'])
		if male:
			age_start = ns['min_age']
		else:
			age_start = ns['min_age'] - 1

		age_header(age_start, column_count, delimiter)
		for line in standards:
			data = line.split()
			event = [data[0] + ' ' + event_name(data[1])]
			times = data[2:]
			times_len = len(times)

			# Align
			if times_len < 13:
				times.insert(1,'')
				times.insert(1,'')
				if times_len == 4:
					times.insert(4,'')
					times.insert(4,'')
					times.insert(4,'')
					times.insert(4,'')
				while len(times) < 13:
					times.append('')

			#Extract
			new_times = [times[i] for i in ns['columns']]

			#Age compensations
			ages = []
			filler = []
			prior_nt = '' 
			for i, nt in enumerate(new_times):
				filler.append('')
				if not nt:
					new_times[i] = prior_nt
					ages.append(i)
				else:
					prior_nt = nt
					ages.append(0)

			new_times.reverse()
			ages.reverse()
			print delimiter.join(map(str, event + filler + new_times + ages + ages))


if __name__ == "__main__":
	import sys
	if len(sys.argv) >= 3:
		import os
		fn = sys.argv[1]
		if (len(sys.argv) == 5):
			delimiter = sys.argv[4]
			if 't' == delimiter:
				delimiter = '\t'
		else:
			delimiter = ','

		if os.path.isfile(fn):
			standard = sys.argv[2].lower()
			if "regional" in standard:
				regional(fn, delimiter = delimiter)
			elif any( s in standard for s in provincial_standards.keys()):
				ps = provincial_standards[standard]
				festival(fn , start_age = ps["start_age"], columns = ps["columns"])
#			elif "festival" in standard:
#				festival(fn, delimiter = delimiter)
			elif "fnq" in standard:
				fnq(fn, delimiter = delimiter)
#			elif "provincial" in standard:
#				festival(fn, start_age = 14, delimiter = delimiter)
			elif "nova-scotia" in standard:
				festival(fn, columns = 6, start_age = 12, delimiter = delimiter)
			elif any(s in standard for s in national_standards.keys()):
				male = True
				if len(sys.argv) == 4:
					if sys.argv[3] == 'f':
						male = False
				national(fn, delimiter = delimiter, standard=standard, male = male)
	else:
		print 'Usage:'
		print ' {0} {{filename}} {{formater}} [m (default) | f] [delimiter ("," = default)]'.format(sys.argv[0])
		print 'Where "formatter" is one of:'
		print '   "Regional", "Festival", "Provincial", "Trials", "CSC", "CJC", "Nova-Scotia", "Easterns", or "Westerns".'
		print 'Specifying the delimiter requires the gender ("m" or "f") be specified too.'
