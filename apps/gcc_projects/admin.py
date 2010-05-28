from django.contrib import admin
from gcc_projects.models import *

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category, CategoryAdmin)


# vim: et sw=4 sts=4
