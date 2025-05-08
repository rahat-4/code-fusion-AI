from rest_framework import serializers

from apps.countries.models import (
    Country,
    Demonym,
    NativeName,
    Currency,
    Language,
    CountryLanguage,
    CountryTranslation,
)


class NativeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NativeName
        fields = ["language_code", "official_name", "common_name"]


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["code", "symbol", "name"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["code", "name"]


class CountryLanguageSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = CountryLanguage
        fields = ["language"]


class DemonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demonym
        fields = ["language_code", "gender", "name"]


class CountryTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryTranslation
        fields = ["language_code", "official_name", "common_name"]


class CountrySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    currencies = serializers.SerializerMethodField()
    idd = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    demonyms = serializers.SerializerMethodField()
    maps = serializers.SerializerMethodField()
    flags = serializers.SerializerMethodField()
    coatOfArms = serializers.SerializerMethodField()
    capitalInfo = serializers.SerializerMethodField()
    postalCode = serializers.SerializerMethodField()
    translations = serializers.SerializerMethodField()
    latlng = serializers.SerializerMethodField()
    car = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = [
            "uid",
            "name",
            "tld",
            "cca2",
            "ccn3",
            "cioc",
            "independent",
            "status",
            "un_member",
            "currencies",
            "idd",
            "capital",
            "alt_spellings",
            "region",
            "subregion",
            "languages",
            "latlng",
            "landlocked",
            "borders",
            "area",
            "demonyms",
            "cca3",
            "translations",
            "flag",
            "maps",
            "population",
            "gini",
            "fifa",
            "car",
            "timezones",
            "continents",
            "flags",
            "coatOfArms",
            "start_of_week",
            "capitalInfo",
            "postalCode",
        ]

    def get_translations(self, obj):
        translations = obj.translations.all()
        return {
            t.language_code: {"official": t.official_name, "common": t.common_name}
            for t in translations
        }

    def get_name(self, obj):
        native_names = NativeName.objects.filter(country=obj)
        native_dict = {
            nn.language_code: {
                "official": nn.official_name,
                "common": nn.common_name,
            }
            for nn in native_names
        }
        return {
            "common": obj.name_common,
            "official": obj.name_official,
            "nativeName": native_dict,
        }

    def get_currencies(self, obj):
        return {
            c.code: {"symbol": c.symbol, "name": c.name} for c in obj.currencies.all()
        }

    def get_idd(self, obj):
        return {
            "root": obj.idd_root,
            "suffixes": obj.idd_suffixes or [],
        }

    def get_languages(self, obj):
        return {
            cl.language.code: cl.language.name
            for cl in obj.languages.select_related("language").all()
        }

    def get_demonyms(self, obj):
        result = {}
        for gender in ["m", "f"]:
            for d in obj.demonyms.filter(gender=gender):
                result.setdefault(d.language_code, {})[gender] = d.name
        return result

    def get_maps(self, obj):
        return {
            "googleMaps": obj.google_maps,
            "openStreetMaps": obj.openstreetmaps,
        }

    def get_flags(self, obj):
        return {
            "png": obj.flag_png,
            "svg": obj.flag_svg,
            "alt": obj.flag_alt,
        }

    def get_coatOfArms(self, obj):
        return {
            "png": obj.coat_of_arms_png,
            "svg": obj.coat_of_arms_svg,
        }

    def get_capitalInfo(self, obj):
        return {"latlng": obj.capital_latlng}

    def get_postalCode(self, obj):
        return {"format": obj.postal_code_format, "regex": obj.postal_code_regex}

    def get_latlng(self, obj):
        latlng = []
        latlng.append(obj.latitude)
        latlng.append(obj.longitude)
        return latlng

    def get_car(self, obj):
        car = {}
        car["signs"] = obj.car_signs
        car["side"] = obj.car_side
        return car
