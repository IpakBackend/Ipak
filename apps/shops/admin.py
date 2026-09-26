from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Color

# Register your models here.


class ColorAdmin(ModelAdmin):
    list_display = "id", "__str__", "hex_value"
    readonly_fields = "id",
    list_per_page = 16


admin.site.register(Color, ColorAdmin)
