from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('profiles', views.UserProfileViewSet)

router.register('data', views.UserProfileData, basename="data")

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginView.as_view()),
    path('featured/', views.ListFeaturedData.as_view())
]