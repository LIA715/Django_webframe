from django.db import models
import os
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)  # allow unicode= 한글도 가능하게
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

class Meta:
    verbose_name_plural = 'Categories'

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True) #현재시간 자동반영
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    #on_delete = models.CASCADE

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    # one to many

    tags = models.ManyToManyField(Tag, blank=True)
    #many to many

    def __str__(self):
        return f'[{self.pk}] {self.title}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name) #업로드된파일의 이름 가져와. 전체 경로 가져옴,

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
        #전체 경로에서 이름 가져오고 .을 기준으로 나눠(파일명.확장자). 배열이 됨. -1은 맨 마지막 인덱스를 의미. 앞에 갯수 상관X
        #맨 마지막에 있는 확장자명을 가져와서 리턴해줌.

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment{self.pk}'


