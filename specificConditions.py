from debug_log import *
from tkinter_schedule_vis import tkinter_schedule_vis


def update_min_day_len(conditions, schedule, days, log_file_name):
    for class_schedule_id in schedule.school_schedule:
        class_schedule = schedule.school_schedule[class_schedule_id]
        tk_capture_count = 0
        for current_day in days:
            schedule_at_day = class_schedule[current_day]

            days_with_conflict = set()
            set_days = set(days)

            while schedule.get_num_of_lessons(schedule_at_day, log_file_name) < \
                    conditions.general['min_lessons_per_day']:
                class_schedule_list = list(class_schedule.values())
                max_len_day_i = class_schedule_list.index(max(class_schedule.values(), key=len))

                schedule_at_day = class_schedule[current_day]

                tk_capture_count += 1
                tkinter_schedule_vis(
                    schedule,
                    days,
                    capture_name=f'update_min_day_len_{class_schedule_id}_{tk_capture_count}_pre_change',
                    dir_name=log_file_name
                )

                if days_with_conflict == set_days:
                    debug_log(log_file_name, 'Error: days_with_conflict == set_days')
                    return

                first_lesson_index = schedule.find_first_lesson(schedule_at_day, log_file_name)
                if first_lesson_index is None:
                    debug_log(log_file_name, 'DEBUG: day at max move to first_lesson_index')

                max_day_schedule = schedule.school_schedule[class_schedule_id][days[max_len_day_i]]

                if not schedule.are_teachers_taken(
                        teachers=max_day_schedule[-1][0].teachers_id,
                        day=current_day,
                        lesson_index=len(schedule.school_schedule[class_schedule_id][current_day]),
                        class_id=class_schedule_id
                ):
                    if not schedule.move_subject_to_day(
                            class_id=class_schedule_id,
                            day_to=current_day,
                            day_from=days[max_len_day_i],
                            subject_position=-1,
                            log_file_name=log_file_name
                    ):
                        debug_log(
                            log_file_name,
                            f'While 1: class_schedule_id: '
                            f'{class_schedule_id} '
                            f'lesson_index={-1} '
                            f'day_to: {current_day} day_from: '
                            f'{days[max_len_day_i]}'
                        )
                        return
                    tkinter_schedule_vis(
                        schedule,
                        days,
                        capture_name=f'update_min_day_len_{class_schedule_id}_{tk_capture_count}_post_change',
                        dir_name=log_file_name
                    )
                elif not schedule.are_teachers_taken(
                        teachers=max_day_schedule[first_lesson_index][0].teachers_id,
                        day=current_day,
                        lesson_index=len(schedule.school_schedule[class_schedule_id][current_day]),
                        class_id=class_schedule_id
                ):
                    if not schedule.move_subject_to_day(
                            class_id=class_schedule_id,
                            day_to=current_day,
                            day_from=days[max_len_day_i],
                            subject_position=first_lesson_index,
                            log_file_name=log_file_name
                    ):
                        debug_log(
                            log_file_name,
                            f'While 1: class_schedule_id: '
                            f'{class_schedule_id} '
                            f'lesson_index={first_lesson_index} '
                            f'day_to: {current_day} day_from: '
                            f'{days[max_len_day_i]}',
                        )
                        return
                    tkinter_schedule_vis(
                        schedule,
                        days,
                        capture_name=f'update_min_day_len_{class_schedule_id}_{tk_capture_count}_post_move',
                        dir_name=log_file_name
                    )
                else:
                    days_with_conflict.add(days[max_len_day_i])

                    debug_log(log_file_name, 'while 2', days_with_conflict != set_days, days_with_conflict, set_days)

                    for day in set_days.difference(days_with_conflict):

                        schedule_at_other_day = schedule.school_schedule[class_schedule_id][day]
                        first_lesson_index = schedule.find_first_lesson(schedule_at_other_day, log_file_name)

                        if first_lesson_index is None:
                            debug_log(log_file_name, 'not max move to first_lesson_index')
                            continue

                        if schedule.get_num_of_lessons(schedule_at_other_day, log_file_name) <= \
                                conditions.general['min_lessons_per_day']:
                            continue

                        if not schedule.are_teachers_taken(
                                teachers=schedule_at_other_day[-1][0].teachers_id,
                                day=current_day,
                                lesson_index=len(schedule.school_schedule[class_schedule_id][current_day]),
                                class_id=class_schedule_id
                        ):
                            if not schedule.move_subject_to_day(
                                    class_id=class_schedule_id,
                                    day_to=current_day,
                                    day_from=day,
                                    subject_position=-1,
                                    log_file_name=log_file_name
                            ):
                                debug_log(
                                    log_file_name,
                                    f'While 2: class_schedule_id: '
                                    f'{class_schedule_id} '
                                    f'lesson_index={-1} '
                                    f'day_to: {current_day} day_from: '
                                    f'{day}',
                                )
                                return
                            tkinter_schedule_vis(
                                schedule,
                                days,
                                capture_name=f'update_min_day_len_{class_schedule_id}_{tk_capture_count}_post_move',
                                dir_name=log_file_name
                            )
                        elif not schedule.are_teachers_taken(
                                teachers=schedule_at_other_day[first_lesson_index][0].teachers_id,
                                day=current_day,
                                lesson_index=len(schedule.school_schedule[class_schedule_id][current_day]),
                                class_id=class_schedule_id
                        ):
                            if not schedule.move_subject_to_day(
                                    class_id=class_schedule_id,
                                    day_to=current_day,
                                    day_from=day,
                                    subject_position=first_lesson_index,
                                    log_file_name=log_file_name
                            ):
                                debug_log(
                                    log_file_name,
                                    f'While 1: class_schedule_id: '
                                    f'{class_schedule_id} '
                                    f'lesson_index={first_lesson_index} '
                                    f'day_to: {current_day} day_from: '
                                    f'{day}',
                                )
                                return
                            tkinter_schedule_vis(
                                schedule,
                                days,
                                capture_name=f'update_min_day_len_{class_schedule_id}_{tk_capture_count}_post_move',
                                dir_name=log_file_name
                            )
                        else:
                            days_with_conflict.add(day)
                            continue

                        tk_capture_count += 1
                    break
