from django.contrib import admin

# Register your models here.


from catalog.models import Publisher, Category, Book, BookPic


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active', 'created_on',)
    search_fields = ('id', 'name', 'description',)
    date_hierarchy = 'created_on'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'tags', 'display_order', 'is_active',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent', 'created_on',)
    search_fields = ('name', 'description', 'tags',)
    date_hierarchy = 'created_on'


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_publisher', 'price', 'quantity', 'is_active', 'is_bestseller', 'is_featured',)
    list_filter = ('book_publisher', 'is_active', 'is_bestseller', 'is_featured', 'is_free_shipping', 'created_on',)
    search_fields = ('name', 'gist', 'brand__name', 'sku', 'gtin', )
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_on'


class BookPicAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'url', 'display_order',)
    list_filter = ('created_on',)
    search_fields = ('id', 'product__name', 'url',)
    date_hierarchy = 'created_on'


admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookPic, BookPicAdmin)
