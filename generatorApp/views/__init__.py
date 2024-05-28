class views:
    from .general import (
        home,
        DocsView
    )
    from .schedule import (
        SchedulesListView,
        ScheduleView,
        LessonHoursView,
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
