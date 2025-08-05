from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Reaction(models.Model):
    class ReactionType(models.TextChoices):
        NO = 'no', 'No Reaction'
        LIKE = 'like', 'Like'
        DISLIKE = 'dislike', 'Dislike'

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=ReactionType.choices, default=ReactionType.NO)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')  # Mỗi user chỉ được react 1 lần cho 1 article