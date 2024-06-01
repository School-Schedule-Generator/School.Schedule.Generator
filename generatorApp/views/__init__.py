class views:
    from .general import (
        home,
        DocsView
    )
    from .schedule import (
        SchedulesListView,
        ScheduleView,
        LessonHoursView,
        ClassesView,
        ClassroomsView,
        ClassroomTypesView,
        TeachersView,
        SubjectNamesView,
        SubjectsView,
        upload_file,
        get_upload_file,
        create_schedule,
        upload,
        schedule_settings
    )
    from .user import (
        RegisterUserView,
        LoginUserView,
        LogoutUserView
    )
