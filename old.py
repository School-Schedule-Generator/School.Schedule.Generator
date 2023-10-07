# classes_subjects = {}
# for class_id in classes_id:
#     classes_subjects[class_id] = {}
#
# print(classes_subjects)
#
# for subject in subjects:
#     classes_subjects[subject.class_id][subject.subject_id] = subject
#
# for i, class_subjects in enumerate(classes_subjects.items()):
#     print('class ', i)
#     for subject in range(len(class_subjects)):
#         print('\t', subject)


# subjects = [Subject(
#     subject_id=subjects_df.loc[i, 'subject_ID'],
#     subject_name_id=subjects_df.loc[i, 'subject_name_ID'],
#     class_id=subjects_df.loc[i, 'class_ID'],
#     subject_count_in_week=subjects_df.loc[i, 'subject_count_in_week'],
#     number_of_groups=subjects_df.loc[i, 'number_of_groups'],
#     teacher_id=subjects_df.loc[i, 'teacher_ID'],
#     classroom_id=subjects_df.loc[i, 'classroom_ID'],
#     subject_length=subjects_df.loc[i, 'subject_length'],
#     lesson_hours_id=subjects_df.loc[i, 'lesson_hours_ID']
# ) for i in range(len(subjects_df))]
