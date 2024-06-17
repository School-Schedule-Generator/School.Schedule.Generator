import json
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import ast


class ScheduleList(models.Model):
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=800, default='')
    created_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return self.name


class ClassroomTypes(models.Model):
    in_id = models.TextField(default=None, null=True)
    schedule_id = models.ForeignKey(ScheduleList, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)

    class Meta:
        unique_together = ('schedule_id', 'in_id')

    def __str__(self):
        return self.description


class Classrooms(models.Model):
    in_id = models.TextField(default=None, null=True)
    schedule_id = models.ForeignKey(ScheduleList, on_delete=models.CASCADE)
    type_id = models.ForeignKey(ClassroomTypes, default=0, on_delete=models.SET_DEFAULT)
    name = models.CharField(max_length=30)

    class Meta:
        unique_together = ('schedule_id', 'in_id')

    def __str__(self):
        return self.name


class Teachers(models.Model):
    in_id = models.TextField(default=None, null=True)
    schedule_id = models.ForeignKey(ScheduleList, on_delete=models.CASCADE)
    main_classroom_id = models.ForeignKey(Classrooms, null=True, default=None, on_delete=models.SET_DEFAULT)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    possible_subjects = models.CharField(max_length=300)
    start_hour_index = models.CharField(max_length=30)
    end_hour_index = models.CharField(max_length=30)
    days = models.CharField(max_length=30)

    class Meta:
        unique_together = ('schedule_id', 'in_id')

    def __str__(self):
        return str(self.name) + " " + str(self.surname)


class LessonHours(models.Model):
    in_id = models.TextField(default=None, null=True)
    schedule_id = models.ForeignKey(ScheduleList, on_delete=models.CASCADE)
    start_hour = models.CharField(max_length=30)
    duration = models.IntegerField()

    class Meta:
        unique_together = ('schedule_id', 'in_id')

    def __str__(self):
        return self.start_hour


class Classes(models.Model):
    in_id = models.TextField(default=None, null=True)
    schedule_id = models.ForeignKey(ScheduleList, on_delete=models.CASCADE)
    supervising_teacher_id = models.ForeignKey(Teachers, default=None, on_delete=models.SET_DEFAULT)
    starting_lesson_hour_id = models.ForeignKey(LessonHours, default=0, on_delete=models.SET_DEFAULT)
    grade = models.IntegerField()
    class_signature = models.CharField(max_length=10)

    class Meta:
        unique_together = ('schedule_id', 'in_id')

    def __str__(self):
        return str(self.grade) + str(self.class_signature)


class SubjectNames(models.Model):
    in_id = models.TextField(default=None, null=True)
    schedule_id = models.ForeignKey(ScheduleList, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('schedule_id', 'in_id')

    def __str__(self):
        return self.name


class ScheduleSettings(models.Model):
    schedule_id = models.ForeignKey(ScheduleList, on_delete=models.CASCADE)
    content = models.TextField(
        default=json.dumps({
            "min_lessons_per_day": 5,
            "max_lessons_per_day": 9,
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
        })
    )

    def __str__(self):
        return self.content


# TODO: FIXXX
class Subject(models.Model):
    in_id = models.TextField(default=None, null=True)
    schedule_id = models.ForeignKey(ScheduleList, on_delete=models.CASCADE)

    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    subject_name_id = models.ForeignKey(SubjectNames, on_delete=models.CASCADE)
    lesson_hour_id = models.ForeignKey(LessonHours, null=True, default=None, on_delete=models.SET_DEFAULT)
    teachers_id = models.TextField(default=None, null=True)
    classroom_id = models.ForeignKey(Classrooms, null=True, default=None, on_delete=models.SET_DEFAULT)
    subject_count_in_week = models.IntegerField()
    number_of_groups = models.IntegerField()
    max_stack = models.IntegerField()
    classroom_types = models.CharField(max_length=30)

    class Meta:
        unique_together = ('schedule_id', 'in_id')

    @staticmethod
    def check_teachers(teachers_id, schedule_id):
        for teacher_id in ast.literal_eval(teachers_id):
            try:
                Teachers.objects.get(schedule_id=schedule_id, _id=teacher_id)
            except Teachers.DoesNotExist:
                return False
        return True
