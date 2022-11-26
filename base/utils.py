from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event, In_out
from django.contrib.auth.models import User
from datetime import datetime as dt
import datetime as dtt


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, in_outs, user_id):
		in_outs_per_day = in_outs.filter(start_time__day=day, employee = user_id)
		d = ''
		total = []
		i = 0
		for in_out in in_outs_per_day:
			in_out_times = str(in_out.get_html_url)
			in_out_times_arr = in_out_times.split(' ')
			FMT = '%H:%M:%S'
			tdelta = dt.strptime(in_out_times_arr[6], FMT) - dt.strptime(in_out_times_arr[2], FMT)
			total.append(str(tdelta))
			d += f'<li> {in_out.get_html_url}</li>'
		
		if day != 0:
			mysum = dtt.timedelta()
			for i in total:
				(h, m, s) = i.split(':')
				dd = dtt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
				mysum += dd
			if (str(mysum) == '0:00:00'):
				mysum = ''
			else:
				mysum = "Total: " + str(mysum)
			return f"<td><span class='date'>{day}</span><ul> {d} {str(mysum)}</ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, in_outs, user_id):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, in_outs, user_id)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, user_id, withyear=True):
		in_outs = In_out.objects.filter(start_time__year=self.year, start_time__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, in_outs, user_id)}\n'
		return cal
