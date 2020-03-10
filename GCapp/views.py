from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Game_news
from .models import GameCollection
from .models import Games
from .models import Users
from .models import Comments
from .models import Community
from .models import Posts
from django.template import loader
from django.http import Http404
from . import models
from . import forms
from .forms import CommentForm
import hashlib
import json
import markdown


#加密算法
def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


# Create your views here.
'''
Main page
'''
def index(request):
    #显示最新的4个新闻和评分最高的游戏
    latest_news_list = Game_news.objects.order_by('-news_date')[:4]
    recommend_game_list = Games.objects.order_by('-game_score')[:4]
    community_list = Community.objects.all()
    template = loader.get_template('GCapp/index.html') #载入模板
    context = {
        'latest_news_list': latest_news_list,
        'recommend_game_list': recommend_game_list,
        'community_list':community_list,
    }#传入上下文
    return HttpResponse(template.render(context, request))

'''
If the corresponding news of id is not existing, then throw out 404 excepton 
'''
def detail(request, news_id):
    try:
        news = Game_news.objects.get(pk=news_id)
    except Game_news.DoesNotExist:
        raise Http404("News does not exist")
    return render(request, 'GCapp/detail.html', {'news': news})

'''
login
'''
def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/GCapp/main')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = 'Please check the input content'

        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.Users.objects.get(user_name=username)
            except:
                message = 'User is not exist!'
                return render(request, 'GCapp/login.html', locals())

            if user.user_password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.user_id
                request.session['user_name'] = user.user_name
                return redirect('/GCapp/main')
            else:
                message = 'The input password is wrong, please input again!'
                return render(request, 'GCapp/login.html',locals())

        else:
            return render(request, 'GCapp/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'GCapp/login.html',locals())

'''
register
'''
def register(request):
    if request.session.get('is_login', None):
        return redirect('GCapp/main/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "Please check the input content！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            gender = register_form.cleaned_data.get('gender')
            tag = register_form.cleaned_data.get('tag')
            community = register_form.cleaned_data.get('community')

            if password1 != password2:
                message = 'The passwords entered are not same!'
                return render(request, 'GCapp/register.html', locals())
            else:
                same_name_user = models.Users.objects.filter(user_name=username)
                if same_name_user:
                    message = 'User exists'
                    return render(request, 'GCapp/register.html', locals())
                same_email_user = models.Users.objects.filter(user_email=email)
                if same_email_user:
                    message = 'Email has been registered'
                    return render(request, 'GCapp/register.html', locals())

                new_user = models.Users()
                new_user.user_name = username
                new_user.user_password = hash_code(password1)
                new_user.user_email = email
                new_user.user_gender = gender
                new_user.user_tags = tag
                new_user.user_community = community
                new_user.save()

                return redirect('/GCapp/login/')
        else:
            return render(request, 'GCapp/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'GCapp/register.html', locals())

'''
logout
'''
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/GCapp/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/GCapp/')

'''
main page
'''
def main(request):
    userid = request.session.get('user_id', None)
    game_collection_list = GameCollection.objects.filter(collection_owner = userid)
    tag = Users.objects.get(user_id= userid)#获取用户标签
    recommend_game_list = Games.objects.filter(game_type=tag.user_tags)
    #print(recommend_game_list)
    context = {'game_collection_list': game_collection_list,
               'recommend_game_list': recommend_game_list}#传入上下文
    return render(request, 'GCapp/main.html', context)

def game(request, collection_gameid):
    try:
        game = Games.objects.get(game_id=collection_gameid)

        if request.method == 'POST':
            # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
            # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
            form = CommentForm(request.POST)

            # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
            if form.is_valid():
                # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
                # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
                comment = form.save(commit=False)

                # 将评论和被评论的游戏关联起来。
                comment.comment_game = game

                # 最终将评论数据保存进数据库，调用模型实例的 save 方法
                comment.save()

                # 重定向到 game 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
                # 然后重定向到 get_absolute_url 方法返回的 URL。

                #return redirect(game)

            else:
                # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
                # 因此我们传了三个模板变量给 game.html，
                # 一个是游戏（game），一个是评论列表，一个是表单 form
                # 注意这里我们用到了 game.comment_set.all() 方法，
                # 这个用法有点类似于 game.objects.all()
                # 其作用是获取这个 game 下的的全部评论，
                # 因为 Games 和 Comment 是 ForeignKey 关联的，
                # 因此使用 game.comment_set.all() 反向查询全部评论。
                # 具体请看下面的讲解。
                comment_list = Comments.objects.filter(comment_game=game)
                context = {'game': game,
                           'form': form,
                           'comment_list': comment_list
                           }
                return render(request, 'GCapp/game.html', context=context)

        # 记得在顶部导入 CommentForm
        form = CommentForm()
        # 获取这篇 game 下的全部评论
        comment_list = Comments.objects.filter(comment_game = game)

        # 将游戏、表单、以及游戏下的评论列表作为模板变量传给 game.html 模板，以便渲染相应数据。
        context = {'game': game,
                   'form': form,
                   'comment_list': comment_list
                   }
        return render(request, 'GCapp/game.html', context=context)
    except Games.DoesNotExist:
        raise Http404("Game does not exist")
    return render(request, 'GCapp/game.html', {'game': game})

def search(request):
    q = request.POST['gamename']
    print(q)
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'GCapp/errors.html', {'error_msg': error_msg})

    game_list = Games.objects.filter(game_name__icontains = q)
    return render(request, 'GCapp/results.html', {'error_msg': error_msg, 'game_list': game_list})

def error(request):
    pass
    return render(request, 'GCapp/errors.html')

def results(request):
    pass
    return render(request, 'GCapp/results.html')

def delete(request):
    gid = request.POST['game_id']
    print(gid)
    GameCollection.objects.get(collection_gameid=gid).delete()
    return HttpResponse(json.dumps({'state': 'SUCCESS'}))

def add(request):
    gameid = request.POST['game_id']#获取gameid
    gameobj = Games.objects.get(game_id=gameid)#利用gameid获取外键对象
    userid = request.session.get('user_id', None)#获取userid
    owner = Users.objects.get(user_id=userid)#利用userid查找用户名字
    game_name = Games.objects.get(game_id= gameid)#利用gameid获取游戏名字
    #查找用户拥有的collection,避免add相同的游戏
    if(GameCollection.objects.filter(collection_owner=owner).filter(collection_gameid=gameid).exists()):
        pass
    else:
        collection = GameCollection(collection_owner = owner, collection_gameid= gameobj, collection_game = game_name)#外键以对象方式插入
        collection.save()  # flush到数据库中
    return HttpResponse(json.dumps({'state': 'SUCCESS'}))

def community(request, communityid):
    try:
        community = Community.objects.get(community_id=communityid)
        #利用community找到所有属于这个社区的帖子
        post_list = Posts.objects.filter(post_community = community.community_id)
        return render(request, 'GCapp/community.html' ,{'community': community,'post_list':post_list})
    except Community.DoesNotExist:
        raise Http404("Community does not exist")
    #return render(request, 'GCapp/community.html.html', {'game': game})

def post(request,postid):
    try:
        post = Posts.objects.get(post_id=postid)
        return render(request, 'GCapp/post.html', {'post':post})
    except Posts.DoesNotExist:
        raise Http404("Post does not exist!")
    return render(request, 'GCapp/post.html')
