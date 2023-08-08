from operator import truediv
from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from weather_admin.models import Weather, City, Date, MyUser
from datetime import datetime
from django.contrib.auth import logout
from django.utils.formats import get_format

# Create your views here.

def parse_date(date_str):
    # Parse date from string by DATE_INPUT_FORMATS of current language
    for item in get_format('DATE_INPUT_FORMATS'):
        try:
            return datetime.strptime(date_str, item).date()
        except (ValueError, TypeError):
            continue
    return None


def home_view(request, *args, **kwargs):

    cities = City.objects.all() # query set
    dates = Date.objects.all()
    all_weather = Weather.objects.all()

    place = None
    city_id = None
    new_dates_list = None
    filtered_allweather = None
    min_max_temp_gap = None
    date_not_exist_error = False
    not_chosen_error = False

    if request.method == 'POST': # form>select in home.html # POST method is used to transfer data from client to server in HTTP

        alldata = request.POST
        city_name = alldata.get("city", "0") # string item
        date_name = alldata.get("date", "0")
        print(city_name)

        if city_name != '0' and date_name != '0': # both of select options (city/date) are chosen

            dates_list = list(dates) # convert query set to list

            parsed_date = parse_date(date_name)
            query_date = Date.objects.get(date=parsed_date)

            new_dates_list = []
            n = 0
            for i in dates:
                n += 1
                if i == query_date:
                    new_dates_list = Date.objects.all()[n:(n+7)] # dates_list[dates_list.index(i):(dates_list.index(i)+6)]

            place = City.objects.get(name=city_name)
            city_id = place.id

            filtered_allweather = all_weather.order_by('date').filter(city__name=city_name)
            date_not_exist_error = False
            try:
                chosen_date_id = filtered_allweather.get(date=query_date).id #! gets id from the first query set, not from filtered_allweather (добавлять даты в django-admin по порядку)
                filtered_allweather.query.set_limits(low=chosen_date_id-1, high=chosen_date_id+6)
            except Weather.DoesNotExist:
                date_not_exist_error = True

            if Weather.temperature_gap(city_name) != None:
                min_max_temp_gap = Weather.temperature_gap(city_name) # static method in models.py (the gap between the warmest and coldest day of the month)
    
        else:
            not_chosen_error = True

    context = {
        'cities': cities,
        'dates': dates,
        'place': place,
        'new_dates_list': new_dates_list,
        'not_chosen_error': not_chosen_error,
        'date_not_exist_error': date_not_exist_error,
        'filtered_allweather': filtered_allweather,
        'min_max_temp_gap': min_max_temp_gap
    }
    return render(request, "home.html", context)
    # "home.html" - template name, {} - context ({} - empty dictionary)


def newadmin_view(request, *args, **kwargs):
    return render(request, "newadmin.html", {})


def register_view(request):
    user_created_message = False
    unique_username_error = False
    different_passwords_error = False
    no_input_data_error = False

    if request.method == 'POST':
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        password2 = request.POST.get('Password2')
    
        if username!='' and password!='' and password2!='':
            if password == password2:
                try:
                    MyUser.objects.create_user(username, email, password)
                    messages.success(request, 'Account created successfully')
                    return redirect(reverse('home'))
                except: #! IntegrityError
                    unique_username_error = True
            else:
                different_passwords_error = True
        else:
            no_input_data_error = True # request was empty

    context2 = {
        'no_input_data_error': no_input_data_error,
        'different_passwords_error': different_passwords_error,
        'user_created_message': user_created_message,
        'unique_username_error': unique_username_error,
    }         
    return render(request, 'register.html', context2)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return redirect('login')    
    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    return redirect('home')

