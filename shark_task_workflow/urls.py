from rest_framework.routers import SimpleRouter

from .views import StatusesViewSet, TransitionsViewSet, WorkflowsViewSet

router = SimpleRouter()

router.register("statuses", StatusesViewSet, "statuses")
router.register("workflows", WorkflowsViewSet, "workflows")
router.register("transitions", TransitionsViewSet, "transitions")

urlpatterns = [] + router.urls
