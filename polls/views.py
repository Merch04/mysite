from ast import Try
from django.http import HttpResponseRedirect
from django.shortcuts import render
import sqlite3
from datetime import datetime
from .forms import TimeInterval_Form
from .models import Video


def read_sqlite_table(start_rows, end_rows):
    try:
        sqlite_connection = sqlite3.connect('db-controller.sqlite')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = f"SELECT * from telemetry where time BETWEEN {start_rows} AND {end_rows}"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Всего строк:  ", len(records))
        print("Вывод каждой строки")
        miss_time = []
        for i in range(1, len(records)):
            last_row = records[i-1]
            real_row = records[i]
            if real_row[1] - last_row[1] >= 2:
                last_time = datetime.fromtimestamp(last_row[1])
                real_time = datetime.fromtimestamp(real_row[1])
                #miss_time.append(f'{last_row[1]}  ->  {real_row[1]}')
                miss_time.append(f"{last_time.strftime('%H:%M:%S')}  ->  {real_time.strftime('%H:%M:%S')}")

        cursor.close()
        return miss_time

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        return None
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")



def index(request):
    if request.method == 'POST':     
        form = TimeInterval_Form(request.POST)
        if form.is_valid():
            print(form.cleaned_data['start_time'])
            request.session['times'] = [str(form.cleaned_data['start_time']), str(form.cleaned_data['end_time'])]
            return HttpResponseRedirect('statics')
    else:
        form = TimeInterval_Form()
    #need_times = read_sqlite_table(1649774679, 1649774762)
    content = {'form' : form}
    return render(request, 'polls/index.html', content)
  
def statics(request):
    times = request.session.get('times', None)
    miss_time = read_sqlite_table(1649774679, 1649774762)
    print(miss_time)
    video=Video.objects.all()
    content = {
        'miss_time' : miss_time,
        'times': times,
        "video": video,
    }
    return render(request, 'polls/statics.html', content)
