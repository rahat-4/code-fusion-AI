import logging
import requests
import time

from django.core.management import BaseCommand
from django.db import transaction

from apps.countries.models import (
    Country,
    Demonym,
    NativeName,
    Currency,
    Language,
    CountryLanguage,
    CountryTranslation,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

API_URL = "https://restcountries.com/v3.1/all"


class Command(BaseCommand):
    help = "Import countries data from REST countries API"

    def handle(self, *args, **kwargs):
        start_time = time.time()
        self.stdout.write(self.style.SUCCESS("Starting countries import..."))

        success = self.load_countries_data()

        if success:
            elapsed_time = time.time() - start_time
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully imported countries data in {elapsed_time:.2f} seconds."
                )
            )
        else:
            self.stdout.write(self.style.ERROR("Failed to import countries data."))

    def fetch_countries_data(self):
        """Fetch countries data from the REST countries API."""

        try:
            self.stdout.write(
                self.style.NOTICE(f"Fetching countries data from {API_URL}")
            )
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data from API: {e}"))
            return None

    def process_native_names(self, country_obj, native_names_data):
        """Process and save native name data for a country."""

        if not native_names_data:
            return

        for lang_code, names in native_names_data.items():
            NativeName.objects.create(
                country=country_obj,
                language_code=lang_code,
                official_name=names.get("official", ""),
                common_name=names.get("common", ""),
            )

    def process_currencies(self, country_obj, currencies_data):
        """Process and save currency data for a country."""

        if not currencies_data:
            return

        for currency_code, currency_info in currencies_data.items():
            Currency.objects.create(
                country=country_obj,
                code=currency_code,
                name=currency_info.get("name", ""),
                symbol=currency_info.get("symbol", ""),
            )

    def process_languages(self, country_obj, languages_data):
        """Process and save language data for a country."""

        if not languages_data:
            return

        for code, name in languages_data.items():
            # Create or get the language object
            language, _ = Language.objects.get_or_create(
                code=code, defaults={"name": name}
            )

            # Create the country-language relationship
            CountryLanguage.objects.create(country=country_obj, language=language)

    def process_demonyms(self, country_obj, demonyms_data):
        """Process and save demonym data for a country."""

        if not demonyms_data:
            return

        for lang_code, gender_data in demonyms_data.items():
            for gender, name in gender_data.items():
                Demonym.objects.create(
                    country=country_obj,
                    language_code=lang_code,
                    gender=gender,
                    name=name,
                )

    def process_translations(self, country_obj, translations_data):
        """Process and save translations data for a country."""

        if not translations_data:
            return

        for lang_code, translation in translations_data.items():
            CountryTranslation.objects.create(
                country=country_obj,
                language_code=lang_code,
                official_name=translation.get("official", ""),
                common_name=translation.get("common", ""),
            )

    @transaction.atomic
    def load_countries_data(self):
        """Main function to load countries data into the database."""

        # Fetch data from API
        countries_data = self.fetch_countries_data()
        if not countries_data:
            self.stdout.write(self.style.ERROR("No data fetched from API."))
            return False

        self.stdout.write(
            f"Successfully fetched {len(countries_data)} countries data from API."
        )

        # Clear existing data
        self.stdout.write(self.style.NOTICE("Clearing existing data..."))

        Currency.objects.all().delete()
        CountryLanguage.objects.all().delete()
        CountryTranslation.objects.all().delete()
        NativeName.objects.all().delete()
        Demonym.objects.all().delete()
        Country.objects.all().delete()
        Language.objects.all().delete()

        # Process countries data
        for country_data in countries_data:
            try:
                name = country_data.get("name", {})
                idd = country_data.get("idd", {})
                capitals = country_data.get("capital", [])
                capital = capitals[0] if capitals else None
                latlng = country_data.get("latlng", [])
                capital_info = country_data.get("capitalInfo", {})
                capital_latlng = (
                    country_data.get("latlng", []) if capital_info else None
                )
                postal_code = country_data.get("postalCode", {})

                country = Country.objects.create(
                    name_common=name.get("common", ""),
                    name_official=name.get("official", ""),
                    tld=country_data.get("tld", []),
                    cca2=country_data.get("cca2", ""),
                    ccn3=country_data.get("ccn3", ""),
                    cioc=country_data.get("cioc", ""),
                    independent=country_data.get("independent", False),
                    status=country_data.get("status", ""),
                    un_member=country_data.get("unMember", False),
                    idd_root=idd.get("root", ""),
                    idd_suffixes=idd.get("suffixes", []),
                    capital=capital,
                    alt_spellings=country_data.get("altSpellings", []),
                    region=country_data.get("region", ""),
                    subregion=country_data.get("subregion", ""),
                    latitude=latlng[0] if latlng else None,
                    longitude=latlng[1] if latlng else None,
                    landlocked=country_data.get("landlocked", False),
                    borders=country_data.get("borders", []),
                    area=country_data.get("area", 0),
                    cca3=country_data.get("cca3", ""),
                    flag=country_data.get("flag", ""),
                    google_maps=country_data.get("maps", {}).get("googleMaps", ""),
                    openstreetmaps=country_data.get("maps", {}).get(
                        "openStreetMaps", ""
                    ),
                    population=country_data.get("population", 0),
                    gini=country_data.get("gini", {}),
                    fifa=country_data.get("fifa", ""),
                    car_signs=country_data.get("car", {}).get("signs", []),
                    car_side=country_data.get("car", {}).get("side", ""),
                    timezones=country_data.get("timezones", []),
                    continents=country_data.get("continents", []),
                    flag_png=country_data.get("flags", {}).get("png", ""),
                    flag_svg=country_data.get("flags", {}).get("svg", ""),
                    flag_alt=country_data.get("flags", {}).get("alt", ""),
                    coat_of_arms_png=country_data.get("coatOfArms", {}).get("png", ""),
                    coat_of_arms_svg=country_data.get("coatOfArms", {}).get("svg", ""),
                    start_of_week=country_data.get("startOfWeek", ""),
                    capital_latlng=capital_latlng,
                    postal_code_format=postal_code.get("format", ""),
                    postal_code_regex=postal_code.get("regex", ""),
                )

                # Process native names
                native_names = name.get("nativeName", {})
                self.process_native_names(country, native_names)

                # Process currencies
                self.process_currencies(country, country_data.get("currencies", {}))

                # Process languages
                self.process_languages(country, country_data.get("languages", {}))

                # Process translations
                self.process_translations(country, country_data.get("translations", {}))

                # Process demonyms
                self.process_demonyms(country, country_data.get("demonyms", {}))

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error processing country {country_data.get('name', {})}: {e}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Data import completed. Imported {Country.objects.count()} countries."
            )
        )

        return True
