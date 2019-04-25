from django.contrib import admin

from Business_rating.models import Business, Review


class BusinessAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('name', 'id', 'category')


admin.site.register(Business, BusinessAdmin)
admin.site.register(Review)
