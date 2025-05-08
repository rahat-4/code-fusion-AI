from rest_framework.generics import ListCreateAPIView

from apps.countries.models import Country

from .serializers import CountrySerializer


class CountryListCreateView(ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
