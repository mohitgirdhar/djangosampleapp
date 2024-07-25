from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostView, PostDetailView, CommentView, PostLikeViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("likes", PostLikeViewSet, basename="post-likes")

urlpatterns = [
    path("", include(router.urls)),
    path("posts/", PostView.as_view()),
    path("posts/<int:pk>/", PostDetailView.as_view()),
    path("comments/<int:post_id>/", CommentView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
