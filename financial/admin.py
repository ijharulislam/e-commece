from django.contrib import admin
from financial.models import Currency, Tax


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'exchange_rate', 'display_format', 'is_primary', 'is_active',)
    list_filter = ('is_primary', 'is_active', 'created_on',)
    search_fields = ('name', 'code',)
    date_hierarchy = 'created_on'


class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'method', 'rate',)
    list_filter = ('method', 'created_on',)
    search_fields = ('name',)
    date_hierarchy = 'created_on'


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Tax, TaxAdmin)
