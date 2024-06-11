from ..models import *


def upload_file(file_name, file, schedule_id):
    schedule = ScheduleList.objects.get(id=schedule_id)
    try:
        if file_name == 'classes':
            for index, row in file.iterrows():
                _id, grade, class_signature, supervising_teacher, starting_lesson_hour_id = row.values

                if not Classes.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        supervising_teacher_id=Teachers.objects.get(_id=supervising_teacher, schedule_id=schedule),
                        starting_lesson_hour_id=LessonHours.objects.get(_id=starting_lesson_hour_id,
                                                                        schedule_id=schedule),
                        grade=grade,
                        class_signature=class_signature
                ).exists():
                    data = Classes.objects.create(
                        _id=_id,
                        schedule_id=schedule,
                        supervising_teacher_id=Teachers.objects.get(_id=supervising_teacher, schedule_id=schedule),
                        starting_lesson_hour_id=LessonHours.objects.get(_id=starting_lesson_hour_id,
                                                                        schedule_id=schedule),
                        grade=grade,
                        class_signature=class_signature
                    )
                    data.save()

        elif file_name == 'classroom_types':
            for index, row in file.iterrows():
                _id, description = row.values
                if not ClassroomTypes.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        description=description
                ).exists():
                    data = ClassroomTypes.objects.create(_id=_id, schedule_id=schedule, description=description)
                    data.save()
        elif file_name == 'classrooms':
            for index, row in file.iterrows():
                _id, name, type_id = row.values
                if not Classrooms.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        name=name,
                        type_id=ClassroomTypes.objects.get(id=type_id, schedule_id=schedule)
                ).exists():
                    data = Classrooms.objects.create(_id=_id, schedule_id=schedule, name=name,
                                                     type_id=ClassroomTypes.objects.get(id=type_id))
                    data.save()
        elif file_name == 'lesson_hours':
            for index, row in file.iterrows():
                _id, start_hour, duration = row.values
                if not LessonHours.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        start_hour=start_hour,
                        duration=duration
                ).exists():
                    data = LessonHours.objects.create(
                        _id=_id,
                        schedule_id=schedule,
                        start_hour=start_hour,
                        duration=duration
                    )
                    data.save()
        elif file_name == 'subject_names':
            for index, row in file.iterrows():
                _id, name = row.values
                if not SubjectNames.objects.filter(_id=_id, schedule_id=schedule, name=name).exists():
                    data = SubjectNames.objects.create(_id=_id, schedule_id=schedule, name=name)
                    data.save()
        elif file_name == 'teachers':
            for index, row in file.iterrows():
                _id, name, surname, possible_subjects, start_hour_index, end_hour_index, days, main_classroom_id = row.values
                if not Teachers.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        main_classroom_id=Classrooms.objects.get(_id=main_classroom_id,
                                                                 schedule_id=schedule) if main_classroom_id != 'Null' else None,
                        end_hour_index=end_hour_index,
                        days=days
                ).exists():
                    data = Teachers.objects.create(
                        _id=_id,
                        schedule_id=schedule,
                        main_classroom_id=Classrooms.objects.get(_id=main_classroom_id,
                                                                 schedule_id=schedule) if main_classroom_id != 'Null' else None,
                        name=name,
                        surname=surname,
                        possible_subjects=possible_subjects,
                        start_hour_index=start_hour_index,
                        end_hour_index=end_hour_index,
                        days=days
                    )
                    data.save()
        elif file_name == 'subjects':
            for index, row in file.iterrows():
                (
                    _id,
                    subject_name_id,
                    classes_id,
                    subject_count_in_week,
                    number_of_groups,
                    lesson_hour_id,
                    teachers_id,
                    classroom_id,
                    max_stack,
                    classroom_types
                ) = row.values

                if not Subject.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        classes_id=Classes.objects.get(_id=classes_id, schedule_id=schedule),
                        subject_name_id=SubjectNames.objects.get(_id=subject_name_id, schedule_id=schedule),
                        lesson_hour_id=LessonHours.objects.get(_id=lesson_hour_id, schedule_id=schedule) if str(
                            lesson_hour_id) != 'nan' else None,
                        teachers_id=teachers_id,
                        classroom_id=Classrooms.objects.get(_id=classroom_id, schedule_id=schedule) if str(
                            classroom_id) != 'nan' else None,
                        subject_count_in_week=subject_count_in_week,
                        number_of_groups=number_of_groups,
                        max_stack=max_stack,
                        classroom_types=classroom_types
                ).exists():
                    data = Subject.objects.create(
                        _id=_id,
                        schedule_id=schedule,
                        classes_id=Classes.objects.get(_id=classes_id, schedule_id=schedule),
                        subject_name_id=SubjectNames.objects.get(_id=subject_name_id, schedule_id=schedule),
                        lesson_hour_id=LessonHours.objects.get(_id=lesson_hour_id, schedule_id=schedule) if str(
                            lesson_hour_id) != 'nan' else None,
                        teachers_id=teachers_id,
                        classroom_id=Classrooms.objects.get(_id=classroom_id, schedule_id=schedule) if str(
                            classroom_id) != 'nan' else None,
                        subject_count_in_week=subject_count_in_week,
                        number_of_groups=number_of_groups,
                        max_stack=max_stack,
                        classroom_types=classroom_types
                    )
                    if data.check_teachers(teachers_id, schedule):
                        data.save()
        else:
            return False
    except ValueError:
        return False
    return True
