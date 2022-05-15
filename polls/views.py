from datetime import datetime
import sqlite3
from django.shortcuts import render
from django.http import HttpResponseRedirect
from email.header import Header
from asyncio.windows_events import NULL
from .forms import DateForm  # new
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import logout
import time
from .models import Shift, Telemetry, Video, Restaurants
from .forms import ChoiseVideoForm
from ast import Try


def read_sqlite_table(start_rows, end_rows):
    """dt = datetime.strptime(times[0])
    start_rows = datetime.timestamp(dt)
    dt = datetime.strptime(times[1])
    end_rows = datetime.timestamp(dt)"""
    
    profit_coef = {
        '9': 0.4,
        '12': 1,
        '18': 0.5
    }
    try:
        object_arr = Telemetry.objects.filter(
            time__gt=start_rows, time__lt=end_rows)
        miss_time = []
        miss_timecode = []
        temp_samp = 0
        lose_profit = 0
        time_kirill = ''
        for i in range(2, len(object_arr)):
            last_row = object_arr[i-1]
            real_row = object_arr[i]
            if real_row.time - last_row.time >= 60:
                last_time = datetime.fromtimestamp(last_row.time)
                real_time = datetime.fromtimestamp(real_row.time)

                time_kirill = str(last_time).split(" ")[1].split(":")[0]

                last_timecode = last_row.time - start_rows
                real_timecode = real_row.time - start_rows
                last_timecode = time.strftime(
                    "%H:%M:%S", time.gmtime(last_timecode))
                real_timecode = time.strftime(
                    "%H:%M:%S", time.gmtime(real_timecode))

                if int(time_kirill) >= 18:
                    lose_profit += profit_coef['18'] * \
                        (real_row.time - last_row.time)
                elif int(time_kirill) >= 12:
                    lose_profit += profit_coef['12'] * \
                        (real_row.time - last_row.time)
                elif int(time_kirill) >= 9:
                    lose_profit += profit_coef['9'] * \
                        (real_row.time - last_row.time)

                miss_time.append(
                    f"{last_time.strftime('%H:%M:%S')}  ->  {real_time.strftime('%H:%M:%S')}")
                miss_timecode.append(f"{last_timecode}  ->  {real_timecode}")

                temp_samp += real_row.time - last_row.time

        temp_samp += real_row.time - last_row.time
        temp_samp = time.strftime("%H:%M:%S", time.gmtime(temp_samp))

        lose_profit = lose_profit * 5

        return miss_time, miss_timecode, temp_samp, lose_profit

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        return None


def index(request):
    if (request.user.username == ''):
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':

            form_date = ChoiseVideoForm(request.POST)  # new
            if form_date.is_valid():  # new
                
                print('ДАТА С ВИДЖЕТА')
                start_date = str(form_date.cleaned_data['start_date'])[0:-6]
                end_date = str(form_date.cleaned_data['end_date'])[0:-6]
                print(form_date.cleaned_data['shift'])
                request.session['times'] = [start_date, end_date]

                return HttpResponseRedirect('statics')
        else:
            form_date = ChoiseVideoForm()
            
        content = {'form_date': form_date}

        return render(request, 'polls/index.html', content)


def statics(request):
    if (request.user.username == ''):
        return HttpResponseRedirect('/')
    else:
        times = request.session.get('times', None)
        miss_time, miss_timecode, temp_samp, lose_profit = read_sqlite_table(
            1649774679, 1649778786)
        video = Video.objects.all()
        content = {
            'miss_time': miss_time,
            'miss_timecode': miss_timecode,
            'temp_samp': temp_samp,
            'lose_profit': lose_profit,
            "video": video,
        }
        return render(request, 'polls/statics.html', content)

def load_restaurants(request):
    shift_id = request.GET.get('shift_id')
    restaurants = Restaurants.objects.filter(shift_id=shift_id).all()
    return render(request, 'polls/restaurants_dropdown_list_options.html', {'restaurants': restaurants})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

# def hui(request):
#     peremenaya = Telemetry.objects.filter(
#         time__lt=1649774681, time__gt=1649774679)
#     print([i.id for i in peremenaya])
