from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event, In_out
from django.contrib.auth.models import User
from datetime import datetime as dt
import datetime as dtt
import matplotlib.pyplot as plt
import base64
from io import BytesIO


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
			d += f'<li> {in_out.get_html_url}'
		
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
			# print(f"day: {day}")
			# print(d)
			return f"<td><span class='date'>{day}</span><ul> {d} <br> {str(mysum)}</li> </ul></td>"
		return '<td></td>'


	def formatday_rep(self, day, start_date, end_date ,in_outs, user_id):
		in_outs_per_day = in_outs.filter(start_time__day=day, employee = user_id)
		# print(start_date)
		sdate = datetime.strptime(start_date, '%Y-%m-%d').date()		
		edate = datetime.strptime(end_date, '%Y-%m-%d').date()
		# print(end_date)
		for ins in in_outs_per_day:
			if not (sdate <= ins.start_time.date() and edate >= ins.start_time.date()):
				day = 0
			# else:
			# 	day = 0
		d = ''
		total = []
		i = 0
		for in_out in in_outs_per_day:
			in_out_times = str(in_out.get_html_url)
			in_out_times_arr = in_out_times.split(' ')
			FMT = '%H:%M:%S'
			tdelta = dt.strptime(in_out_times_arr[6], FMT) - dt.strptime(in_out_times_arr[2], FMT)
			total.append(str(tdelta))
			d += f'<li> {in_out.get_html_url}'
		
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
			# print(f"day: {day}")
			# print(d)
			return f"<td><span class='date'>{day}</span><ul> {d} <br> {str(mysum)}</li> </ul></td>"
		return '<td></td>'



	# formats a week as a tr
	def formatweek(self, theweek, in_outs, user_id):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, in_outs, user_id)
		return f'<tr> {week} </tr>'

	def formatweek_rep(self, theweek, start_date, end_date ,in_outs, user_id):
		week = ''
		for d, weekday in theweek:
			week += self.formatday_rep(d, start_date, end_date, in_outs, user_id)
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

	def formatmonth_rep(self, user_id, sdate, edate, withyear=True):
		# print(f"sdate: {sdate}")
		# print(f"edate: {edate}")
		if sdate != '' and edate != '' and user_id != '':
			smonth = int(sdate[5:7])
			syear = int(sdate[0:4])
			emonth = int(edate[5:7])
			eyear = int(edate[0:4])
			cal = ''
			for j in range(syear, eyear+1):
				for i in range(smonth, emonth+1):
					cal += f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
					in_outs = In_out.objects.filter(start_time__year=j, start_time__month=i)
					st_in = in_outs.values_list('start_time')
					# print("in_outs")
					# print(st_in)
					cal += f'{self.formatmonthname(j, i, withyear=withyear)}\n'
					cal += f'{self.formatweekheader()}\n'
					for week in self.monthdays2calendar(j, i):
						cal += f'{self.formatweek_rep(week, sdate, edate, in_outs, user_id)}\n'
			return cal
		return ''

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
    
def get_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize = (9.5, 5))
    plt.title("Working Hours")
    plt.plot(x, y)
    plt.xticks(rotation=45)
    plt.xlabel('date')
    plt.ylabel('hours')
    plt.tight_layout()
    graph = get_graph()
    return graph
