
from django.contrib import admin
from timeside.server.models import *


class TaskAdmin(admin.ModelAdmin):
    list_display = ['date_added', 'date_modified', 'status']
    list_filter = ['date_modified', 'status']


class ResultAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'date_added', 'date_modified', 'status']
    list_filter = ['date_modified', 'status']



admin.site.register(Selection)
admin.site.register(Item)
admin.site.register(Experience)
admin.site.register(Processor)
admin.site.register(Preset)
admin.site.register(Result, ResultAdmin)
admin.site.register(Task, TaskAdmin)
