from django.urls import path

from weather.views import WeatherView


urlpatterns = [
    path(
        "get-weather/",
        WeatherView.as_view(),
        name="get_weather_by_postal_code",
    ),
]
