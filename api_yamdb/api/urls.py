from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, APISignUp, APIToken,
                    CommentsViewSet, ReviewsViewSet,
                    CategoryViewSet, GenreViewSet, TitleViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/auth/signup/', APISignUp.as_view(), name='signup'),
    path('v1/auth/token/', APIToken.as_view(), name='token'),
    path('v1/', include(router_v1.urls)),
]
