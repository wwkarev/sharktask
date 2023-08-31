from django.urls import path

from shark_task_core.views import LinkTypeView, LinkView, TaskView, filter_tasks, get_task_events

urlpatterns = [
    path("task/", TaskView.as_view(), name="task_views"),
    path("task/<int:task_id>/", TaskView.as_view(), name="task_views"),
    path("filter_tasks/", filter_tasks, name="filter_task_view"),
    path("task_events/<int:task_id>/", get_task_events, name="task_events_view"),
    path("link_type/", LinkTypeView.as_view(), name="link_type_view"),
    path("link/", LinkView.as_view(), name="link_view"),
    path("link/<int:link_id>/", LinkView.as_view(), name="link_view"),
]
