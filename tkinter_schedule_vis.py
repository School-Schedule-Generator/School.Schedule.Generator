import tkinter as tk
import tkcap
import os
from settings import settings


def tkinter_schedule_vis(schedule, days, capture_name='tkCapture', dir_name='log_0', capture=True):
    if not settings.TKCAPTURE:
        return False

    def rgb(red, green, blue):
        return f'#{red:02x}{green:02x}{blue:02x}'

    def get_digits(number):
        return [int(d) for d in str(number)]

    root = tk.Tk()
    data = schedule.data

    for i, day in enumerate(days):  # i -> day id
        week_day = tk.Label(root, text=day, font=("Arial", 14))
        week_day.grid(row=0, column=i * len(data), columnspan=len(data))

        # loop through classes and subjects
        for j, class_schedule_id in enumerate(data):  # j -> class id
            class_schedule = data[class_schedule_id]
            for k in range(len(class_schedule[day])):  # k -> subject id
                subjects = class_schedule[day][k]

                # check if there is teacher conflict (one teacher has some lessons in the same time)
                same_time_subjects = []
                for x, other_class_schedule_id in enumerate(data):
                    other_class_schedule = data[other_class_schedule_id]
                    if other_class_schedule != class_schedule:
                        try:
                            same_time_subjects.append(other_class_schedule[day][k])
                        except IndexError:
                            pass

                # create labels and set colors on red if there is a conflict
                if subjects[0].is_empty:
                    label = tk.Label(
                        root,
                        text="empty",
                        font=("Arial", 8),
                        bg=rgb(173, 217, 230)
                    )
                else:
                    color = [27, 58, 19]
                    last_digit = 1
                    for subject in subjects:
                        if subject.teachers_id in schedule.get_same_time_teacher(
                            day_to=day,
                            lesson_index=subject.lesson_hours_id,
                        ):
                            color = [255, 0, 0]
                            break
                        for teacher_id in subject.teachers_id:
                            for digit in get_digits(teacher_id):
                                color[1] *= digit + 1
                            color[1] = color[1] % 255

                            for digit in reversed(get_digits(teacher_id)):
                                color[2] *= digit + 1
                                last_digit = digit
                            color[2] = color[2] % 255

                        color[0] *= last_digit + 1
                        color[0] = color[0] % 255
                        color[0] = min(color[0], 200)

                    teachers = ''
                    classrooms = ''
                    teachers_list = []
                    for subject in subjects:
                        if subject.teachers_id[0] in teachers_list:
                            color = [255, 0, 0]

                        teachers_list.append(subject.teachers_id[0])
                        teachers += str(subject.teachers_id[0]) + ' '
                        classrooms += str(subject.classroom_id)

                    color = rgb(*color)

                    subjects_ids = [x.subject_id for x in subjects]

                    label = tk.Label(
                        root,
                        text=f"subjects id {subjects_ids}\n"
                        f"teacher: {teachers}\n"
                        f"lesson_hours_id: {subjects[0].lesson_hours_id}\n"
                        f"classrooms_id: {classrooms}",
                        font=("Arial", 8),
                        bg=color
                    )

                label.grid(row=k + 1, column=i * len(data) + j)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    if not os.path.exists(f'logs/{dir_name}'):
        os.mkdir(f'logs/{dir_name}')

    if not os.path.exists(f'logs/{dir_name}/{schedule.version}'):
        os.mkdir(f'logs/{dir_name}/{schedule.version}')

    if capture:
        cap = tkcap.CAP(root)
        cap.capture(f'logs/{dir_name}/{schedule.version}/{capture_name}.jpg')

        root.after(0, lambda: root.destroy())
        root.mainloop()

    return True

