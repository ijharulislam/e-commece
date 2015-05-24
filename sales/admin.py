from django.contrib import admin

from sales.models import PaymentMethod, Cart, CartItem, Order, OrderItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'updated_on', 'updated_by',)
    list_filter = ('created_on',)
    search_fields = ('id',)
    date_hierarchy = 'created_on'


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('book', 'cart', 'quantity',)
    list_filter = ('book', 'created_on',)
    search_fields = ('book__name', 'cart__id',)
    date_hierarchy = 'created_on'


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)
    date_hierarchy = 'created_on'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'sub_total', 'taxes', 'total', 'currency', 'charge_amount',
                    'refunded_amount', 'payment_status', 'order_status', 'shipping_status', )
    list_filter = ('payment_status', 'order_status', 'shipping_status', 'currency', 'created_on',)
    search_fields = ('id', 'customer__username', 'customer__first_name', 'customer__last_name',
                     'customer__email', 'currency__name',)
    date_hierarchy = 'created_on'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'price', 'quantity', 'sub_total', 'taxes', 'total', 'tax_rate', 'tax_method', )
    list_filter = ('tax_rate', 'tax_method', 'created_on',)
    search_fields = ('order__id', 'book__name', 'tax_method',)
    date_hierarchy = 'created_on'


admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
