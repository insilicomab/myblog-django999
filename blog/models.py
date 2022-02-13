from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class CategoryManager(models.Manager):

    def fetch_category(self, name_en):
        return self.get(name_en=name_en)


class Category(models.Model):
    name = models.CharField(verbose_name='カテゴリー名', max_length=50)
    name_en = models.CharField(verbose_name='カテゴリー名映画', max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CategoryManager()

    def post_count(self):
        post_count = Post.objects.filter(category = self).count()
        return post_count

    def __str__(self):
        return self.name

class PostManager(models.Manager):

    def fetch_all_posts(self):
        return self.order_by('-created_at').all()
    
    def fetch_by_post_id(self, post_id):
        return self.get(pk=post_id)

    def fetch_by_category(self, category_id):
        return self.filter(category_id = category_id).order_by('-created_at')
    
    def fetch_by_category_name(self, category):
        return self.filter(category=category).order_by('-created_at')
    
    def fetch_by_search_freeword(self, freeword):
        return self.filter(Q(title__icontains = freeword) | Q(content__icontains = freeword))


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    title = models.CharField(verbose_name='タイトル', max_length=50)
    content = models.TextField(verbose_name='内容', max_length=1000)
    category = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT)
    thumbnail = models.ImageField(verbose_name='サムネイル画像', upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostManager()

    def like_count(self):
        like_count = Like.objects.filter(post = self).count()
        return like_count

    def __str__(self):
        return self.title


class LikeManager(models.Manager):

    def fetch_is_liked(self, user, post_id):
        return self.filter(user=user, post=post_id).count()


class Like(models.Model):
    post = models.ForeignKey(Post, verbose_name='投稿', on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name='Likeしたユーザー', on_delete=models.PROTECT)

    objects = LikeManager()