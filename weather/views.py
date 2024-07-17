from django.shortcuts import render
from .forms import WeatherForm
import requests


def get_weather_data(city):
    url = f"http://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from wttr.in: {e}")
        return None


def weather_view(request):
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather_data(city)
            if weather_data and 'current_condition' in weather_data:
                context = {
                    'form': form,
                    'city': city,
                    'temperature': weather_data['current_condition']
                    [0]['temp_C'],
                    'description': weather_data['current_condition']
                    [0]['weatherDesc'][0]['value'],
                }
            else:
                context = {
                    'form': form,
                    'city': city,
                    'error': 'Город не найден.'
                }
        else:
            context = {'form': form}
    else:
        form = WeatherForm()
        context = {'form': form}
    return render(request, 'weather/weather.html', context)
