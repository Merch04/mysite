from datetime import datetime
import sqlite3
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from email.header import Header
from asyncio.windows_events import NULL
from .forms import DateForm  # new
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import logout
import time
from .models import Shift, Telemetry, Video, Restaurants
from .forms import ChoiseVideoForm
from ast import Try


def read_sqlite_table(times, shift):
    dt = datetime.strptime(times[0], "%Y-%m-%d %H:%M:%S")
    start_time = datetime.timestamp(dt) + 25200
    dt = datetime.strptime(times[1], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.timestamp(dt) + 25200

    try:
        object_arr = Telemetry.objects.filter(
            time__gt=start_time, time__lt=end_time, shiftId=shift[0])
        miss_time = []
        miss_timecode = []
        temp_samp = 0
        start_video = int(Shift.objects.filter(
            id=shift[0])[0].videos[0]['start'])

        for i in range(2, len(object_arr)):
            y = object_arr[i-1].detectionCoordinates["y1"]
            last_row = object_arr[i-1]
            real_row = object_arr[i]
            if real_row.time - last_row.time >= 60 and y <= 720:
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

        return miss_time, miss_timecode, temp_samp,

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        return None


# ---------------------------------------------GOVNO----NO rabotaet------------------------------------------


def Customer_counts(times, shift):
    clients = []
    First = True
    ErrorTime = 0
    Loop = False
    ErrorCounter = 20
    TimeToClient = 5
    TimeCustomer = {
        'StartTime': 0,
        'EndTime': 0,
        'SumTime': 0
    }
    dt = datetime.strptime(times[0], "%Y-%m-%d %H:%M:%S")
    start_time = datetime.timestamp(dt) + 25200
    dt = datetime.strptime(times[1], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.timestamp(dt) + 25200

    for x in Telemetry.objects.filter(time__gt=start_time, time__lt=end_time, shiftId=shift[0]):

        y1 = x.detectionCoordinates['y1']
        y2 = x.detectionCoordinates['y2']

        center = (y1+y2)/2

        if (center <= 130):
            # Точка входа в последовательность клиентных координат
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
                # Если следующая строка не первое вхождение, и является клиентом, добавляем время, учитывая разрывы
                TimeCustomer['SumTime'] = abs(
                    TimeCustomer['StartTime'] - x.time)
        else:
            # пока количество допустимых ошибок меньше 10 продолжаем работу
            if (ErrorTime <= ErrorCounter and Loop):
                ErrorTime += 1
                continue

            # Если Ошибок уже много для допущения и время свыше 60 секунд, отправляем клиента в БД
            if (ErrorTime >= ErrorCounter and TimeCustomer['SumTime'] > TimeToClient and Loop):
                TimeCustomer['EndTime'] = TimeCustomer['StartTime'] + \
                    TimeCustomer['SumTime']
                clients.append(TimeCustomer)
                ErrorTime = 0
                First = True
                Loop = False

            # Если ошибок достаточно много и не набралось нужного количества координат от клиента, то нахуй его такого клиента, заебали блять ходят нахуй трясутся суки ебаые прячутся от камеры за ебаным продавцом меня заебало эту хуйню уже писать я сам не понимаю что я пишу когда уже кто нибудь придет и решит все мои проблемы пырнув меня ножом в подворотне что бы не идти на ебучую сессию по истории а.......
            if (ErrorTime >= ErrorCounter and TimeCustomer['SumTime'] < TimeToClient and Loop):
                ErrorTime = 0
                First = True
                Loop = False
            # А если совем все плохо и у нас мусорные данные, просто игнорим их
            else:
                ErrorTime = 0
                First = True
    clients = Unite(clients, 145)
    return clients


# ----------------------------------------------------------
def Unite(array, acc):
    output = []
    Buf = {
        'StartTime': -1,
        'EndTime': -1,
        'SumTime': -1
    }

    First = True
    i = 0
    while i < len(array):
        if First:
            Buf = {'StartTime': array[i]['StartTime'], 'EndTime': array[i]
                   ['EndTime'], 'SumTime': array[i]['SumTime']}
            First = False
        # Если пересекаются, то объединяем
        elif ((Buf['EndTime'] + acc >= array[i]['StartTime'] or Buf['StartTime'] >= array[i]['EndTime'])):
            Buf = {'StartTime': Buf['StartTime'], 'EndTime': array[i]
                   ['EndTime'], 'SumTime': array[i]['EndTime']-Buf['StartTime']}
        else:
            output.append(Buf)
            First = True
            i -= 1
        i += 1

    # Костыль ибо хз как отлавливать последний элемент да и мне лень че та
    if ((output[-1]['EndTime'] + acc >= array[-1]['StartTime'] or output[-1]['StartTime'] >= array[-1]['EndTime'])):
        Buf = {'StartTime': output[-1]['StartTime'], 'EndTime': array[-1]
               ['EndTime'], 'SumTime': array[-1]['EndTime']-output[-1]['StartTime']}
        output.append(Buf)
    else:
        output.append(array[-1])

    return output
# ----------------------------------------------------------


def average_time_customers(customers):
    average_time = 0
    average_time = sum([i['SumTime'] for i in customers])
    average_time /= len(customers)
    return time.strftime("%H:%M:%S", time.gmtime(average_time))


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
                shift = str(form_date.cleaned_data['shift'])
                request.session['times'] = [start_date, end_date]
                request.session['shiftId'] = [shift]

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
        shift_id = request.session.get('shiftId', None)
        customers = Customer_counts(times, shift_id)
        miss_time, miss_timecode, temp_samp = read_sqlite_table(
            times, shift_id)
        average_time = average_time_customers(customers)
        video = Video.objects.filter(shiftId=shift_id[0])
        print(len(customers), average_time)
        content = {
            'miss_time': miss_time,
            'miss_timecode': miss_timecode,
            'temp_samp': temp_samp,
            'customers': len(customers),
            'average_time_customers': average_time,
            "video": video,
        }
        return render(request, 'polls/statics.html', content)


def load_shifts(request):
    restaurants_id = request.GET.get('restaurant_id')
    shifts = Shift.objects.filter(restaurants_id=restaurants_id).all()
    return render(request, 'polls/shift_dropdown_list_options.html', {'shifts': shifts})
