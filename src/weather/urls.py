from django.urls import path

from weather.views import WeatherView


urlpatterns = [
    path(
        "get-weather/",
        WeatherView.as_view(),
        name="get-weather",
    ),
]
