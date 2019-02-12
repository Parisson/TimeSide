
from django.contrib import admin
from timeside.server.models import *


class PresetAdmin(admin.ModelAdmin):
    model = Preset
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'processor', 'parameters', 'date_added', 'date_modified']
    list_filter = ['date_modified', 'processor']
    search_fields = ['uuid']


class SelectionAdmin(admin.ModelAdmin):
    model = Selection
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified']
    list_filter = ['date_modified']
    filter_horizontal = ['items', 'selections']
    search_fields = ['title']


class ExperienceAdmin(admin.ModelAdmin):
    model = Experience
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified']
    list_filter = ['date_modified', 'title']
    filter_horizontal = ['presets', 'experiences']
    search_fields = ['uuid', 'title']


class TaskAdmin(admin.ModelAdmin):
    model = Task
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified', 'status']
    list_filter = ['date_modified', 'status']
    search_fields = ['uuid']


class ResultAdmin(admin.ModelAdmin):
    modele = Result
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified', 'status']
    list_filter = ['date_modified', 'status']
    search_fields = ['uuid']


class AnalysisAdmin(admin.ModelAdmin):
    modele = Analysis
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified']
    list_filter = ['date_modified', ]


class AnalysisTrackAdmin(admin.ModelAdmin):
    modele = AnalysisTrack
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified']
    list_filter = ['date_modified']
    search_fields = ['uuid', 'title']

admin.site.register(Selection, SelectionAdmin)
admin.site.register(Item)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Processor)
admin.site.register(SubProcessor)

admin.site.register(Preset, PresetAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Analysis, AnalysisAdmin)
admin.site.register(AnalysisTrack, AnalysisTrackAdmin)
admin.site.register(Annotation)
admin.site.register(AnnotationTrack)
