# models是模块的数据库，模块都要调用models里的数据
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class People(models.Model):
    name=models.CharField(null=True,blank=True,max_length=200)
    job=models.CharField(null=True,blank=True,max_length=200)
    # 下面这个函数是用来在后台页面中直接显示标题的
    def __str__ (self): #一边两个下划线才行
        return self.name

# 用户信息
class UserProfile(models.Model):
    # to=User, related_name='profile',意思是这个belong_to是属于User模块的，并且他在User模块下的名字叫proflie，就像域名解析一样，当User模块调用
    # 他的名字时，就自动跳到了Belong_to函数
    belong_to = models.OneToOneField(to=User, related_name='profile',on_delete=models.CASCADE)
    profile_image = models.FileField(blank=True,upload_to='profile_image')
    def __str__(self):
        return str(self.belong_to)


class Article(models.Model):
    headline = models.CharField(null=True, blank=True,max_length=500)
    content = models.TextField(null=True, blank=True)
    # 下面一行是文章的图片上传功能，upload_to='cover_image'意思是图片会上传到'cover_image'这个文件夹。
    cover = models.FileField(upload_to='cover_image', null=True,blank=True)
    # 文章分类功能的实现
    TAG_CHOICES = (
        ('tech','Tech'),
        ('life','Life'),
        # 左边是他的值，后面是他应该叫的名字，或者说左边的是控制显示在客户端的，后面的是控制显示在后台的
    )
    tag=models.CharField(null=True, blank=True,max_length=5,choices=TAG_CHOICES)
    # 下一行热点文章的实现
    popular_choice = models.BooleanField(default=False)
    editors_choice = models.BooleanField(default=False)
    # default=1意思是默认归属超级管理员
    owner = models.ForeignKey(to=UserProfile, related_name='articles', default=1,on_delete=models.CASCADE)
    def __str__(self):
        return self.headline



# 评论功能
class Comment(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    comment = models.TextField()
    # 下一行是文章与评论关系的实现，实现多个评论对应一个文章，使得访问文章详情时只显示对于这篇文章的评论而不是所有文章的评论。
    # to=Article, related_name='under_comments'的意思是这个对象是属于上面的Article类的'under_comments'模块的。注：即使Article并没有
    # 定义'under_comments'模块，但这么写就好比Article类定义了一样，'under_comments'意思就是这篇文章底下的评论。
    belong_to = models.ForeignKey(to=Article, related_name='under_comments', null=True, blank=True,on_delete=models.CASCADE)
    best_comment = models.BooleanField(default=False)
    def __str__(self):
        return self.comment

# 分页
# class Video(models.Model):
#     title = models.CharField(null=True, blank=True, max_length=300)
#     content = models.TextField(null=True, blank=True)
#     url_image = models.URLField(null=True, blank=True)
#     cover = models.FileField(upload_to='cover_image', null=True)
#     editors_choice = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.title



# 点赞投票功能
class Ticket(models.Model):
    voter = models.ForeignKey(to=UserProfile, related_name='voted_tickets',on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article, related_name='tickets',on_delete=models.CASCADE)
    VOTE_CHOICES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('normal', 'normal'),
        )
    choice = models.CharField(choices=VOTE_CHOICES, max_length=10)

    def __str__(self):
        return str(self.voter)
