from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Comment, Reaction

# User Register
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # Tài khoản chưa kích hoạt
        )
        self.send_verification_email(user)
        return user
    
    def send_verification_email(self, user):
        from django.core.mail import send_mail
        from django.contrib.sites.shortcuts import get_current_site
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        domain = get_current_site(self.context['request']).domain  # "127.0.0.1:8000"

        link = f"http://{domain}/api/verify-email/{uid}/{token}/"

        send_mail(
            subject='Xác thực tài khoản',
            message=f'Click để xác thực: {link}',
            from_email='noreply@example.com',
            recipient_list=[user.email],
            fail_silently=False
        )

# Article CRUD
class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'content', 'created_at']

# Comment
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']

# Reaction
class ReactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reaction
        fields = ['id', 'article', 'user', 'type', 'created_at']
        read_only_fields = ['user', 'created_at']