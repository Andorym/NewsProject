from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.db.models import Sum


class Author(models.Model):
    author_id = models.OneToOneField(User, on_delete=CASCADE)
    rating_Author = models.SmallIntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.author_id = None
        self.post_set = None

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(postRating=Sum('Рейтинг'))
        p_r = 0
        p_r += post_rating.get('postRating')

        comment_rating = self.author_id.comment_sel.all().aggregate(commentRating=Sum('Рейтинг'))
        c_r = 0
        c_r += comment_rating.get('commentRating')

        self.rating_Author = p_r * 3 + c_r
        self.save()

    def __str__(self):
        return f"{self.author_id}"


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.name = None

    def __str__(self):
        return f"{self.name_category}"


class Post(models.Model):
    some_data = models.DateTimeField(auto_now_add=True)
    name_post = models.CharField(max_length=255)
    materials = models.FileField()
    post_text = models.TextField()
    url_materials = models.URLField()
    Author = models.OneToOneField(Author, on_delete=CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.title = None
        self.author = None
        self.dataCreations = None
        self.text = None
        self.rating = None

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:128] + '...'

    def __str__(self, dataf=None):
        'Post from {}'.format(self.dataCreations.strftime('%Д.%М.%Г. %H:%M'))
        return f"{dataf},{self.author},{self.title}"


class Comment(models.Model):
    comment_text = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    comment_post = models.ForeignKey(Post, on_delete=CASCADE)
    user_post = models.ForeignKey(User, on_delete=CASCADE)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.date_comment}, {self.user_post}"


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=CASCADE)

    def __str__(self):
        return f"{self.postThrough},from the category: {self.categoryThrough}"
