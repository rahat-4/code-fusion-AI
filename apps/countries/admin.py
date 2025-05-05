from django.contrib import admin
from .models import (
    Country,
    Currency,
    Language,
    CountryLanguage,
    CountryTranslation,
    NativeName,
    Demonym,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name_common", "capital", "region", "population")
    search_fields = ("name_common", "name_official")
    list_filter = ("region", "subregion", "independent", "un_member")


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "symbol", "country")
    search_fields = ("code", "name", "country__name_common")
    list_filter = ("country__region",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(CountryLanguage)
class CountryLanguageAdmin(admin.ModelAdmin):
    list_display = ("country", "language")
    search_fields = ("country__name_common", "language__name")
    list_filter = ("country__region", "language")


@admin.register(CountryTranslation)
class CountryTranslationAdmin(admin.ModelAdmin):
    list_display = ("country", "language_code", "common_name", "official_name")
    search_fields = (
        "country__name_common",
        "language_code",
        "common_name",
        "official_name",
    )
    list_filter = ("language_code", "country__region")


@admin.register(NativeName)
class NativeNameAdmin(admin.ModelAdmin):
    list_display = ("country", "language_code", "common_name", "official_name")
    search_fields = (
        "country__name_common",
        "language_code",
        "common_name",
        "official_name",
    )
    list_filter = ("language_code", "country__region")


@admin.register(Demonym)
class DemonymAdmin(admin.ModelAdmin):
    list_display = ("country", "language_code", "gender", "name")
    search_fields = ("country__name_common", "language_code", "name")
    list_filter = ("language_code", "gender", "country__region")
