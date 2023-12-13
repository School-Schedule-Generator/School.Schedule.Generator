from debug_log import *
from tkinter_schedule_vis import tkinter_schedule_vis


def add_classrooms(self, classrooms, days, log_file_name):
    for class_id in self.data:
        class_schedule = self.data[class_id]
        for day in days:
            class_schedule_at_day = class_schedule[day]

            for subjects_list in class_schedule_at_day:
                first_lesson_index = self.find_first_lesson_index(class_schedule_at_day, log_file_name)

                # na poczatku sprawdzac czy lekcja ma juz przypisana klase (czy jest rowna 0)
                # moze byc lepiej napisac funkcje ktora zwraca ilosc zestakowanych lekcji dla podanego subjecta w danym dniu
                # i wtedy dla wszystkich pokolei ustawiac ta sama klase a jesli w ktoryms miejscu nie bedzie pasowac to
                # wylosowac kolejna


                    # for subject in subjects_list:
                    #     for classroom in classrooms:
                    #         # TODO trzeba dodac spawdzanie czy dana klasa nie jest juz zajeta
                    #         if classrooms[classroom].type_id in subject.classroom_types:
                    #             subject.classroom_id = classroom
                    #             break

