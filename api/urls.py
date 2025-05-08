from django.urls import path

from .views import CountryListCreateView, CountryDetailView

urlpatterns = [
    path("/countries", CountryListCreateView.as_view(), name="country-list-create"),
    path(
        "/countries/<uuid:country_uid>",
        CountryDetailView.as_view(),
        name="country-detail",
    ),
]
