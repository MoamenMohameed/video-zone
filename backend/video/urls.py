from .views import AuthViewSet , Videos
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()

router.register('auth', AuthViewSet, basename='auth')     
router.register('vid', Videos, basename="test")

urlpatterns = [
    path('', include(router.urls)),
    # path('login/', CustomLoginView.as_view(), name="login")
]