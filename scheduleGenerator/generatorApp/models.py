from django.db import models
from django.utils import timezone


# po zrobieniu modeli zrobic migracje i stworzy super usera
class Teachers(models.Model):
    def __str__(self):
        return


class Classes(models.Model):
    def __str__(self):
        return


class Classrooms(models.Model):
    def __str__(self):
        return


class LessonHours(models.Model):
    def __str__(self):
        return


class SubjectNames(models.Model):
    def __str__(self):
        return


class Subject(models.Model):
    def __str__(self):
        return


class Users:
    username = models.CharField(max_length=40, unique=True) # unikalna nazwa dla usera
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class ScheduleList(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now())
    context = models.TextField()

    def __str__(self):
        return self.user_id, self.name
