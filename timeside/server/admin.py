
from django.contrib import admin
from timeside.server.models import *


class SelectionAdmin(admin.ModelAdmin):
    model = Selection
    list_display = ['__unicode__', 'date_added', 'date_modified']
    list_filter = ['date_modified']
    filter_horizontal = ['items', 'selections']

class ExperienceAdmin(admin.ModelAdmin):
    model = Experience
    list_display = ['__unicode__', 'date_added', 'date_modified']
    list_filter = ['date_modified']
    filter_horizontal = ['presets', 'experiences']

class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ['__unicode__', 'date_added', 'date_modified', 'status']
    list_filter = ['date_modified', 'status']

class ResultAdmin(admin.ModelAdmin):
    modele = Result
    list_display = ['__unicode__', 'date_added', 'date_modified', 'status']
    list_filter = ['date_modified', 'status']


admin.site.register(Selection, SelectionAdmin)
admin.site.register(Item)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Processor)
admin.site.register(SubProcessor)

admin.site.register(Preset)
admin.site.register(Result, ResultAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Analysis)
