from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='متن پست', unique=True)
    slug = models.SlugField(allow_unicode=True)
    created = models.DateField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f'{self.user} - {self.slug}'

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))

    def likes_count(self):
        return self.pvote.count()

    def user_can_like(self, user):
        user_like = user.uvote.filter(post=self)
        if user_like.exists():
            return True
        return False


class Relations(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followrs')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    create = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} followig {self.to_user}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomment', null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -> {self.body[0:30]}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvote')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvote')

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'
