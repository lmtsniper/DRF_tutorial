from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, RegisterView, CommentViewSet, ReactionViewSet, verify_email
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'reactions', ReactionViewSet, basename='reaction')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # JWT login
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # JWT refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
urlpatterns += [
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify-email'),
]