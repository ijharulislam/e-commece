from django.contrib import admin
from geo.models import Country, State, Address



class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code2', 'iso_code3', 'iso_numeric', 'allow_billing',
                    'allow_shipping', 'subject_to_vat', 'display_order', 'is_active',)
    list_filter = ('is_active', 'allow_billing', 'allow_shipping', 'subject_to_vat', 'display_order', 'created_on',)
    search_fields = ('name', 'iso_code2', 'iso_code3', 'iso_numeric',)
    date_hierarchy = 'created_on'


class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country', 'display_order', 'is_active',)
    list_filter = ('is_active', 'display_order', 'created_on',)
    search_fields = ('name', 'code', 'country__name',)
    date_hierarchy = 'created_on'


class AddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'address1', 'address2', 'city', 'state', 'country',)
    list_filter = ('city', 'state', 'country', 'created_on',)
    search_fields = ('first_name', 'last_name', 'email', 'address1', 'address2',)
    date_hierarchy = 'created_on'


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Address, AddressAdmin)
