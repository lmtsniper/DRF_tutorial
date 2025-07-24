from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, RegisterView, CustomLoginView, LogoutView, verify_email

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
urlpatterns += [
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify-email'),
]