from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.timezone import now, timedelta

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    recommended = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # Tasdiqlash maydoni

    def __str__(self, *args, **kwargs):
        return self.title

    @staticmethod
    def get_most_viewed():
        return Post.objects.filter().order_by('-views')[:5]

    @staticmethod
    def get_weekly_popular():
        week_ago = now() - timedelta(days=7)
        return Post.objects.filter(created_at__gte=week_ago).order_by('-views')[:5]

    @staticmethod
    def get_monthly_popular():
        month_ago = now() - timedelta(days=30)
        return Post.objects.filter(created_at__gte=month_ago).order_by('-views')[:5]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
