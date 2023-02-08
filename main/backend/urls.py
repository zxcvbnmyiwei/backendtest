from email import contentmanager
from tabnanny import check
from django.urls import path, include

from . import views
from .views import ContentViewSet,Topic, TopicViewSet,checkResult,MyTokenObtainPairView,profile_list,appendCompleted,UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = DefaultRouter()
router.register('contents', ContentViewSet, basename='contents')
router.register('topics', TopicViewSet, basename='topics')
router.register('users', UserViewSet)

urlpatterns = [
    path('submit/', views.index),
    path('submitMulti/', views.multiFile),
    path('',include(router.urls)),
    path('status/<uuid:task_id>', views.checkResult),
    path('single/', views.singleFile),
    path('multiple/', views.multipleFile),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<str:username>', views.profile_list),
    path('completed/', views.appendCompleted),
]
