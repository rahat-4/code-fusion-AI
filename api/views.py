from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from apps.countries.models import Country

from .serializers import CountryReadSerializer, CountryWriteSerializer


class CountryListCreateView(ListCreateAPIView):
    queryset = Country.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CountryWriteSerializer
        return CountryReadSerializer


class CountryDetailView(RetrieveAPIView):
    queryset = Country.objects.all()

    def get_serializer_class(self):
        return CountryReadSerializer

    def get_object(self):
        return self.get_queryset().get(uid=self.kwargs["country_uid"])
