from rest_framework.routers import SimpleRouter

from shark_task_fields.views import FieldsView, FieldTypesView, ScreensView

router = SimpleRouter()

router.register("field_types", FieldTypesView, "field_types_views")
router.register("fields", FieldsView, "fields_views")
router.register("screens", ScreensView, "screens_views")


urlpatterns = [] + router.urls
