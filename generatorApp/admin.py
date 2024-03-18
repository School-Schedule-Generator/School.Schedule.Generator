from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Classes)
admin.site.register(ClassroomTypes)
admin.site.register(Classrooms)
admin.site.register(Teachers)
admin.site.register(Subject)
admin.site.register(SubjectNames)
admin.site.register(LessonHours)
admin.site.register(ScheduleList)
admin.site.register(ScheduleSettings)
