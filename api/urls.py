from django.urls import path

from .views import CountryListCreateView

urlpatterns = [
    path("/countries", CountryListCreateView.as_view(), name="country-list-create"),
]
