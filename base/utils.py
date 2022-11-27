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
			return f"<td><span class='date'>{day}</span><ul> {d} <br> {str(mysum)}</li> </ul></td>"
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
