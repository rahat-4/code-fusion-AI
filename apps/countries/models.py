import uuid

from django.db import models


class BaseModelWithUID(models.Model):
    uid = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Country(BaseModelWithUID):
    name_common = models.CharField(max_length=100)
    name_official = models.CharField(max_length=255)
    tld = models.JSONField(default=list, blank=True, null=True)
    cca2 = models.CharField(max_length=2, blank=True, null=True)
    ccn3 = models.CharField(max_length=3, blank=True, null=True)
    cioc = models.CharField(max_length=3, blank=True, null=True)
    independent = models.BooleanField(default=False)
    status = models.CharField(max_length=100)
    un_member = models.BooleanField(default=False)
    idd_root = models.CharField(max_length=5, blank=True, null=True)
    idd_suffixes = models.JSONField(default=list, blank=True, null=True)
    capital = models.JSONField(default=list, blank=True, null=True)
    alt_spellings = models.JSONField(default=list, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    subregion = models.CharField(max_length=100, blank=True, null=True)
    # Approximate center of the country
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    landlocked = models.BooleanField(default=False)
    borders = models.JSONField(default=list, blank=True, null=True)
    area = models.BigIntegerField(default=0)
    cca3 = models.CharField(max_length=3, blank=True, null=True)
    flag = models.CharField(max_length=100, blank=True, null=True)
    # Maps
    google_maps = models.URLField(blank=True, null=True)
    openstreetmaps = models.URLField(blank=True, null=True)
    population = models.BigIntegerField(default=0)
    gini = models.JSONField(default=dict, blank=True, null=True)
    fifa = models.CharField(max_length=3, blank=True, null=True)
    car_signs = models.JSONField(default=list, blank=True, null=True)
    car_side = models.CharField(max_length=5, blank=True, null=True)
    timezones = models.JSONField(default=list, blank=True, null=True)
    continents = models.JSONField(default=list, blank=True, null=True)
    # Flags and symbols
    flag_png = models.URLField(blank=True, null=True)
    flag_svg = models.URLField(blank=True, null=True)
    flag_alt = models.TextField(blank=True, null=True)
    coat_of_arms_png = models.URLField(blank=True, null=True)
    coat_of_arms_svg = models.URLField(blank=True, null=True)
    start_of_week = models.CharField(max_length=10, blank=True, null=True)
    capital_latlng = models.JSONField(default=list, blank=True, null=True)
    postal_code_format = models.CharField(max_length=100, blank=True, null=True)
    postal_code_regex = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name_common


class Demonym(BaseModelWithUID):
    GENDER_CHOICES = (
        ("m", "Male"),
        ("f", "Female"),
    )

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="demonyms"
    )
    language_code = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country.name_common}, {self.get_gender_display()})"

    class Meta:
        unique_together = ("country", "language_code", "gender")


class NativeName(BaseModelWithUID):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="native_names"
    )
    language_code = models.CharField(max_length=10)
    official_name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.country.name_common} - ({self.language_code})"

    class Meta:
        unique_together = ("country", "language_code")
        ordering = ["-created_at"]


class Currency(BaseModelWithUID):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="currencies"
    )
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.code} ({self.country.name_common})"


class Language(BaseModelWithUID):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class CountryLanguage(BaseModelWithUID):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="languages"
    )
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="countries"
    )

    def __str__(self):
        return f"{self.country.name_common} - {self.language.name}"

    class Meta:
        unique_together = ("country", "language")
        ordering = ["-created_at"]


class CountryTranslation(BaseModelWithUID):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="translations"
    )
    language_code = models.CharField(max_length=10)
    official_name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.country.name_common} - ({self.language_code})"

    class Meta:
        unique_together = ("country", "language_code")
        ordering = ["-created_at"]

        verbose_name = "Country Translation"
        verbose_name_plural = "Country Translations"
