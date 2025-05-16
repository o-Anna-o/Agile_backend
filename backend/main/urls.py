from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

from .views import SprintViewSet, TaskViewSet


# DRF Router для API
router = DefaultRouter()
router.register(r'sprints', SprintViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    # API маршруты для моделей
    path('api/', include(router.urls)),

    # Аутентификация и регистрация через dj-rest-auth
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

]

