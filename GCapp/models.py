import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
'''
用户表：
用户名（唯一标识） 用户密码 用户性别 用户游戏喜好（暂时还没有想好是什么类型的变量） 用户游戏库 用户发表过的评论 用户发表过的帖子

每个用户应当有自己的游戏库

游戏表：
游戏id(唯一标识) 游戏名 游戏介绍 游戏购买链接 游戏评论（一个游戏可以有多条评论） 游戏社区？（链接？）

讨论区表？评论表？帖子表？

'''
class Users(models.Model):
    gender_choice = (
        ('male', "Male"),
        ('female', "Female"),
    )

    tags_choice = (
        ('N/A',"N/A"),
        ('adventure',"Adventure"),
        ('ancient',"Ancient"),
        ('educational',"Educational"),
        ('fighting',"Fighting"),
        ('racing',"Racing"),
        ('sports',"Sports"),
        ('wargame',"Wargame"),
        ('zombies',"Zombies"),
    )

    community_choice =(
        ('N/A',"N/A"),
        ('gamechat',"GameChat"),
        ('gamequestions',"GameQuestions"),
        ('bugs',"Bugs"),
        ('find users',"FindUsers"),
        ('avatars',"Avatars"),
        ('stats',"Stats")
    )

    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=200, unique=True)#用户名唯一
    user_password = models.CharField(max_length=200)
    user_gender = models.CharField(max_length=32, choices=gender_choice, default='male')
    user_email = models.EmailField(unique=True)#邮箱唯一
    register_time = models.DateTimeField(auto_now_add=True)
    user_tags = models.CharField(max_length=200,choices=tags_choice, default='N/A')
    user_community = models.CharField(max_length=200, choices=community_choice, default='N/A')

    def __str__(self):
        return self.user_name


    class Meta:
        ordering = ["-register_time"] #注册最近的最先显示
        verbose_name = "User"
        verbose_name_plural = "User"

class Games(models.Model):

    type_choice = (
        ('N/A',"N/A"),
        ('adventure',"Adventure"),
        ('ancient',"Ancient"),
        ('educational',"Educational"),
        ('fighting',"Fighting"),
        ('racing',"Racing"),
        ('sports',"Sports"),
        ('wargame',"Wargame"),
        ('zombies',"Zombies"),
    )

    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=200)
    game_type = models.CharField(max_length=200, choices=type_choice, default='N/A')
    game_introduction = models.TextField()
    game_rules = models.TextField()
    game_purchase = models.CharField(max_length=200)
    game_score = models.CharField(max_length=200)
    errata_doc = models.FileField( null= True)
    def __str__(self):
        return self.game_name

class GameCollection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    collection_owner = models.ForeignKey(Users,on_delete=models.CASCADE)
    collection_gameid = models.ForeignKey(Games, on_delete=models.CASCADE)
    collection_game = models.CharField(max_length=200)
    def __str__(self):
        return str(self.collection_owner)

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_publisher = models.CharField(max_length=200)#如果要找用户发表的评论 直接用此字段搜索
    comment_text = models.TextField()
    comment_likecount = models.IntegerField(default=0)
    comment_game = models.ForeignKey(Games,on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_text

class Community(models.Model):

    community_choice =(
        ('N/A',"N/A"),
        ('gamechat',"GameChat"),
        ('gamequestions',"GameQuestions"),
        ('bugs',"Bugs"),
        ('find users',"FindUsers"),
        ('avatars',"Avatars"),
        ('stats',"Stats")
    )

    community_id = models.AutoField(primary_key=True)
    community_name = models.CharField(max_length=200, choices=community_choice, default='N/A')
    def __str__(self):
        return self.community_name

class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_publisher = models.ForeignKey(Users,on_delete=models.CASCADE)
    post_title = models.CharField(max_length=300)
    post_text = models.TextField()
    post_likecount = models.IntegerField(default=0)
    post_community = models.ForeignKey(Community,on_delete=models.CASCADE)#如果找某个社区内的帖子 直接用此字段搜索
    post_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.post_text

class FAQ(models.Model):
    FAQ_id = models.AutoField(primary_key=True)
    FAQ_game =models.ForeignKey(Games,on_delete=models.CASCADE)
    FAQ_text = models.TextField()
    def __str__(self):
        return self.FAQ_game

class Game_news(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_title = models.TextField()
    news_text = models.TextField()
    news_date = models.DateTimeField('date published')

    def __str__(self):
        return self.news_title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
