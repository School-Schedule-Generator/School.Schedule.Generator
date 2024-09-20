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
        DeleteScheduleView,
        DeleteDataView,
        UploadDataView,
        ScheduleSettingsView,
        ExportScheduleView,
        GenerateScheduleView,
    )
    from .user import (
        RegisterUserView,
        LoginUserView,
        LogoutUserView
    )
