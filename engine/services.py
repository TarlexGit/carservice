import datetime
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import timedelta
from .models import FixDate, Master


def chek_and_return(request):
    jwt_object      = JWTAuthentication() 
    header          = jwt_object.get_header(request)
    raw_token       = jwt_object.get_raw_token(header)
    validated_token = jwt_object.get_validated_token(raw_token)
    user            = jwt_object.get_user(validated_token)

    user = User.objects.get(username=user).profile.id
    data = request.data

    # now = datetime.datetime.now().date
    time_date = datetime.datetime.strptime(data['start_time'], '%H:%M:%S').time()  
    print('time_date ***** ', time_date)
    
    end_time = datetime.time(time_date.hour + 1,time_date.minute,time_date.second)
    chek_busy = busy_time(date=data['start_date'], time=time_date, master=data['master'], end_t =end_time)
    if chek_busy['busy_status'] == True:
        return False
    else:
    
        end_time = datetime.time(time_date.hour + 1,time_date.minute,time_date.second)
        print(end_time)
        """ remember old state, set to mutable, сhange the values, set mutable flag back """
        _mutable = data._mutable
        data._mutable = True
        data['profile'] = str(user) 
        data['end_time'] = end_time
        data._mutable = _mutable
        print(data)
        return data

""" Проверки по гафику работы """
def chek_work_time(date, time): 
    print('date ---- ',date, 'time --- ', time) 
    now = datetime.datetime.now() 
    from_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    # print('111111', from_date)
    time_date = datetime.datetime.strptime(time, '%H:%M:%S').time()
    # print('22222',time_date)
    start = datetime.datetime.combine(from_date, time_date)
    message = None
    correct = False 
    
    if start.hour > 20 or start.hour < 10 or start.hour == 20:
        message = 'К сожалению, в это время мы не работаем, наш график: пн-пт с 10 до 20.'
    elif start < now: 
        message = '1 К сожалению, мы не работаем в прошлом. Введите корректную дату.' 
    elif time_date.hour == 19 and time_date.minute > 00:
        message = 'Нам может не хватить времени, наш график: пн-пт с 10 до 20.' 
    else:
        correct = True
        message = 'Вы записаны! Ждем Вас {} в {}'.format(date, time)
          
    return {'correct': correct, 'message': message}


def busy_time(date, time, master, end_t):
    obj =FixDate.objects
    
    print('start chek filter') 
    h = time.hour
    eh = end_t.hour
    m = [m for m in range(time.minute, 60)] # minets from start and before 60 (to 59)
    em = [m for m in range(end_t.minute, 60)]
    print('Проверяем часы: {} и минуты: {}'.format(h, m))
    busy_status = False
    for x in m:
        chek = obj.filter(start_time__hour = h).filter(start_time__minute = x)
        chek_add_hour = obj.filter(start_time__hour = h+1).filter(start_time__minute = 60 - x)
        chek_ent_t = obj.filter(end_time__hour = h).filter(start_time__minute = x)

        # chek_minus_hour = obj.filter(start_time__hour = h+1).filter(start_time__minute = 60 - x)
        if chek or chek_add_hour:
            busy_status = True
            return {'busy_status': busy_status}
            break
        elif chek_ent_t:
            busy_status = True
            print('end_time')
            return {'busy_status': busy_status}
            break
        else: print('-')
    return {'busy_status': busy_status}