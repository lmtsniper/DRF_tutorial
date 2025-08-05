from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse

from .models import Article, Comment, Reaction
from .serializers import ArticleSerializer, RegisterSerializer, CommentSerializer, ReactionSerializer

# Đăng ký
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Tài khoản đã được xác thực thành công!")
    else:
        return HttpResponse("Liên kết xác thực không hợp lệ hoặc đã hết hạn.")

# Đăng nhập
# class CustomLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         token = Token.objects.get(key=response.data['token'])
#         if not token.user.is_active:
#             return Response({'error': 'Tài khoản chưa được xác thực qua email.'}, status=403)
#         return Response({'token': token.key, 'username': token.user.username})

# Đăng xuất
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response({"message": "Logged out successfully"})

# CRUD bài viết
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Nếu đã tồn tại thì cập nhật
        obj, created = Reaction.objects.update_or_create(
            article=serializer.validated_data['article'],
            user=self.request.user,
            defaults={'type': serializer.validated_data['type']}
        )
        return obj