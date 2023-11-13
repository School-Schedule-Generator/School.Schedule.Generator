import tkinter as tk
import tkcap
import os
from settings import settings


# TODO: change to handle lists of subjects and multiple teachers in same time
def tkinter_schedule_vis(schedule_obj, days, capture_name='tkCapture', dir_name='log_0', capture=True):
    if not settings.TKCAPTURE:
        return

    def rgb(red, green, blue):
        return f'#{red:02x}{green:02x}{blue:02x}'

    def get_digits(number):
        return [int(d) for d in str(number)]

    root = tk.Tk()
    schedule = schedule_obj.school_schedule

    for i, day in enumerate(days):  # i -> day id
        week_day = tk.Label(root, text=day, font=("Arial", 14))
        week_day.grid(row=0, column=i * len(schedule), columnspan=len(schedule))
        for j, class_schedule_id in enumerate(schedule):  # j -> class id
            class_schedule = schedule[class_schedule_id]
            for k in range(len(class_schedule[day])):  # k -> subject id
                subjects = class_schedule[day][k]

                same_time_subjects = []
                for x, other_class_schedule_id in enumerate(schedule):
                    other_class_schedule = schedule[other_class_schedule_id]
                    if other_class_schedule != class_schedule:
                        try:
                            same_time_subjects.append(other_class_schedule[day][k])
                        except IndexError:
                            pass

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
                        if schedule_obj.are_teachers_taken(
                                subject.teachers_id,
                                day,
                                subject.lesson_hours_id,
                                class_schedule_id
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

                    color = rgb(*color)

                    teachers = ''
                    for subject in subjects:
                        for teacher in subject.teachers_id:
                            teachers += str(teacher) + ' '

                    label = tk.Label(
                        root,
                        text=f"teacher: {teachers}\n"
                        f"lesson_hours_id: {subjects[0].lesson_hours_id}",
                        font=("Arial", 8),
                        bg=color
                    )

                label.grid(row=k + 1, column=i * len(schedule) + j)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    if not os.path.exists(f'logs/{dir_name}'):
        os.mkdir(f'logs/{dir_name}')

    if capture:
        cap = tkcap.CAP(root)
        cap.capture(f'logs/{dir_name}/{capture_name}.jpg')

        root.after(0, lambda: root.destroy())
        root.mainloop()
