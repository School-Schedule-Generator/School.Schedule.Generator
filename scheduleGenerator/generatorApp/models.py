from django.db import models
from django.utils import timezone


class Users(models.Model):
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.username


class ScheduleList(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now())
    content = models.TextField()

    def __str__(self):
        return self.name


class ClassroomTypes(models.Model):
    schedule_id = models.ForeignKey(ScheduleList, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.description


class Classrooms(models.Model):
    type_id = models.ForeignKey(ClassroomTypes, default=0, on_delete=models.SET_DEFAULT)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Teachers(models.Model):
    main_classroom_id = models.ForeignKey(Classrooms, default='Null', on_delete=models.SET_DEFAULT)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    possible_subjects = models.CharField(max_length=300)
    start_hour_index = models.CharField(max_length=30)
    end_hour_index = models.CharField(max_length=30)
    days = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name) + " " + str(self.surname)


class LessonHours(models.Model):
    start_hour = models.CharField(max_length=30)
    duration = models.IntegerField()

    def __str__(self):
        return self.start_hour


class Classes(models.Model):
    supervising_teacher_id = models.ForeignKey(Teachers, default='Null', on_delete=models.SET_DEFAULT)
    starting_lesson_hour_id = models.ForeignKey(LessonHours, default=0, on_delete=models.SET_DEFAULT)
    grade = models.IntegerField()
    class_signature = models.CharField(max_length=10)

    def __str__(self):
        return str(self.grade) + str(self.class_signature)


class SubjectNames(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    subject_name_id = models.ForeignKey(SubjectNames, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    lesson_hour_id = models.ForeignKey(LessonHours, default='Null', on_delete=models.SET_DEFAULT)
    classroom_id = models.ForeignKey(Classrooms, default='Null', on_delete=models.SET_DEFAULT)
    subject_count_in_week = models.IntegerField()
    number_of_groups = models.IntegerField()
    max_stack = models.IntegerField()
    classroom_types = models.CharField(max_length=30)
