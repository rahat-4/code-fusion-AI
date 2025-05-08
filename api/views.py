from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from apps.countries.models import Country

from .serializers import CountrySerializer


class CountryListCreateView(ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetailView(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_object(self):
        return self.get_queryset().get(uid=self.kwargs["country_uid"])
