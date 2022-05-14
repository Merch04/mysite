from .forms import DateForm  # new
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import logout
import time
from .models import Video
from .models import Shift, Telemetry, Video

from ast import Try
from django.http import HttpResponseRedirect
from django.shortcuts import render
import sqlite3
from datetime import datetime


def read_sqlite_table(start_rows, end_rows):
    profit_coef = {
        '9': 0.4,
        '12': 1,
        '18': 0.5
    }
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
        miss_timecode = []
        temp_samp = 0
        lose_profit = 0
        time_kirill = ''
        for i in range(1, len(records)):
            last_row = records[i-1]
            real_row = records[i]
            if real_row[1] - last_row[1] >= 60:
                last_time = datetime.fromtimestamp(last_row[1])
                real_time = datetime.fromtimestamp(real_row[1])

                time_kirill = str(last_time).split(" ")[1].split(":")[0]

                last_timecode = last_row[1] - start_rows
                real_timecode = real_row[1] - start_rows
                last_timecode = time.strftime(
                    "%H:%M:%S", time.gmtime(last_timecode))
                real_timecode = time.strftime(
                    "%H:%M:%S", time.gmtime(real_timecode))

                if int(time_kirill) >= 18:
                    lose_profit += profit_coef['18'] * \
                        (real_row[1] - last_row[1])
                elif int(time_kirill) >= 12:
                    lose_profit += profit_coef['12'] * \
                        (real_row[1] - last_row[1])
                elif int(time_kirill) >= 9:
                    lose_profit += profit_coef['9'] * \
                        (real_row[1] - last_row[1])

                miss_time.append(
                    f"{last_time.strftime('%H:%M:%S')}  ->  {real_time.strftime('%H:%M:%S')}")
                miss_timecode.append(f"{last_timecode}  ->  {real_timecode}")
                temp_samp += real_row[1] - last_row[1]
        temp_samp = time.strftime("%H:%M:%S", time.gmtime(temp_samp))
        lose_profit = lose_profit * 5
        cursor.close()
        return miss_time, miss_timecode, temp_samp, lose_profit

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        return None
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def index(request):
    if (request.user.username == ''):
        print("Kal")
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':

            form_date = DateForm(request.POST)  # new
            if form_date.is_valid():  # new

                print('ДАТА С ВИДЖЕТА')
                print(form_date.cleaned_data['s_date'])  # new
                print(form_date.cleaned_data['e_date'])  # new
                #request.session['times'] = [str(form.cleaned_data['start_time']), str(form.cleaned_data['end_time'])]

                return HttpResponseRedirect('statics')
        else:
            form_date = DateForm()  # new
        #need_times = read_sqlite_table(1649774679, 1649774762)
        content = {'form_date': form_date}
        return render(request, 'polls/index.html', content)


def statics(request):
    if (request.user.username == ''):
        print("Kal")
        return HttpResponseRedirect('/')
    else:
        times = request.session.get('times', None)
        print(times)
        miss_time, miss_timecode, temp_samp, lose_profit = read_sqlite_table(
            1649774679, 1649778786)
        print(miss_time)
        print(miss_timecode)
        video = Video.objects.all()
        content = {
            'miss_time': miss_time,
            'miss_timecode': miss_timecode,
            'temp_samp': temp_samp,
            'lose_profit': lose_profit,
            'times': times,
            "video": video,
        }
        return render(request, 'polls/statics.html', content)
