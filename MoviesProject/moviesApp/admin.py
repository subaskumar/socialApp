from django.contrib import admin
from moviesApp.models import movieUpcoming
# Register your models here.

class moviesAdmin(admin.ModelAdmin):
    list_display=['rdate','name','actor','actress','rating']

admin.site.register(movieUpcoming,moviesAdmin)