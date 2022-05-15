from datetime import datetime
import sqlite3
from django.shortcuts import render
from django.http import HttpResponseRedirect
from email.header import Header
from .forms import DateForm  # new
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import logout
import time
from .models import Shift, Telemetry, Video, Restaurants
from .forms import ChoiseVideoForm


def read_sqlite_table(times, shift):
    dt = datetime.strptime(times[0], "%Y-%m-%d %H:%M:%S")
    start_rows = datetime.timestamp(dt) + 25200
    dt = datetime.strptime(times[1], "%Y-%m-%d %H:%M:%S")
    end_rows = datetime.timestamp(dt) + 25200

    profit_coef = {
        '9': 0.4,
        '12': 1,
        '18': 0.5
    }
    try:
        object_arr = Telemetry.objects.filter(
            time__gt=start_rows, time__lt=end_rows, shiftId=shift[0])
        miss_time = []
        miss_timecode = []
        temp_samp = 0
        start_video = int(Shift.objects.filter(
            id=shift[0])[0].videos[0]['start'])

        for i in range(2, len(object_arr)):
            last_row = object_arr[i-1]
            real_row = object_arr[i]
            if real_row.time - last_row.time >= 60:
                last_time = datetime.fromtimestamp(last_row.time)
                real_time = datetime.fromtimestamp(real_row.time)

                last_timecode = last_row.time - start_video
                real_timecode = real_row.time - start_video
                last_timecode = time.strftime(
                    "%H:%M:%S", time.gmtime(last_timecode))
                real_timecode = time.strftime(
                    "%H:%M:%S", time.gmtime(real_timecode))

                miss_time.append(
                    f"{last_time.strftime('%H:%M:%S')}  ->  {real_time.strftime('%H:%M:%S')}")
                miss_timecode.append(f"{last_timecode}  ->  {real_timecode}")

                temp_samp += real_row.time - last_row.time

        temp_samp = time.strftime("%H:%M:%S", time.gmtime(temp_samp))

        print(miss_time)
        return miss_time, miss_timecode, temp_samp,

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

                # print('ДАТА С ВИДЖЕТА')
                start_date = str(form_date.cleaned_data['start_date'])[0:-6]
                end_date = str(form_date.cleaned_data['end_date'])[0:-6]
                shift = str(form_date.cleaned_data['shift'])
                request.session['times'] = [start_date, end_date]
                request.session['shiftId'] = [shift]
                return HttpResponseRedirect('statics')
        else:
            form_date = ChoiseVideoForm()

        content = {'form_date': form_date}

        return render(request, 'polls/index.html', content)


def denis_geniy(time, shift):

    clients = []
    First = True
    ErrorTime = 0
    Loop = False
    TimeCustomer = {
        'StartTime': 0,
        'EndTime': 0,
        'SumTime': 0
    }
    print(time)
    for x in Telemetry.objects.filter(time__gt=time[0], time__lt=time[1], shiftId=shift[0]):

        y1 = x.detectionCoordinates['y1']
        y2 = x.detectionCoordinates['y2']

        center = (y1+y2)/2

        if (center <= 130):
            if (First):
                TimeCustomer = {
                    'StartTime': x.time,
                    'EndTime': 0,
                    'SumTime': 1
                }
                Loop = True
                First = False
                continue
            else:
                TimeCustomer['SumTime'] = abs(
                    TimeCustomer['StartTime'] - x.time)
        else:
            if (ErrorTime <= 10 and Loop):
                ErrorTime += 1
                continue
            if (ErrorTime >= 10 and TimeCustomer['SumTime'] > 60 and Loop):
                TimeCustomer['EndTime'] = TimeCustomer['StartTime'] + \
                    TimeCustomer['SumTime']
                clients.append(TimeCustomer)
                ErrorTime = 0
                First = True
                Loop = False
            if (ErrorTime >= 10 and TimeCustomer['SumTime'] < 60 and Loop):
                ErrorTime = 0
                First = True
                Loop = False
            else:
                ErrorTime = 0
                First = True
    return clients


def statics(request):
    if (request.user.username == ''):
        return HttpResponseRedirect('/')
    else:
        times = request.session.get('times', None)
        time_confines = []
        print(times)

        shiftId = request.session.get('shiftId', None)

        # Возможно дальнейшая функция не нужна

        miss_time, miss_timecode, temp_samp = read_sqlite_table(
            times, shiftId)
        video = Video.objects.all()
        content = {
            'miss_time': miss_time,
            'miss_timecode': miss_timecode,
            'temp_samp': temp_samp,
            "video": video,
        }
        return render(request, 'polls/statics.html', content)


def load_restaurants(request):
    shift_id = request.GET.get('shift_id')
    restaurants = Restaurants.objects.filter(shift_id=shift_id).all()
    return render(request, 'polls/restaurants_dropdown_list_options.html', {'restaurants': restaurants})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)
