# coding:utf-8
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.utils.datetime_safe import datetime
from weibo.models import UserProfiles, Contents, Follows, Comments


# Create your views here.



def findMyall(username):  # 查找自己以及关注人的微博
    follows = list(Follows.objects.filter(username=username))
    showcontent = list(Contents.objects.filter(username=username))
    for follow in follows:
        showcontent += list(Contents.objects.filter(username=follow.follow_username))
    showcontent.sort(key=lambda content: content.content_time, reverse=True)  # 按时间排序
    return showcontent


def findAll():  # 查找所有微博
    allcontent = list(Contents.objects.filter())
    allcontent.sort(key=lambda content: content.content_time, reverse=True)  # 按时间排序
    return allcontent


def mylogin(request):  # 若有登录请求，判断并处理，无请求显示登录页面
    errors = ''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username:
            errors = '请输入用户名'
        elif not password:
            errors = '请输入密码'
        else:
            user = auth.authenticate(username=username, password=password)  # 进行用户认证，成功后进入主页
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    request.session['username'] = username
                    return HttpResponseRedirect('/')
            else:
                errors = '用户名或密码不正确'
    return render(request, 'login.html', locals())  # 返回错误信息


def mysignup(request):  # 有注册请求进行处理，否则直接打开注册页面
    errors = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if not username:
            errors = '请输入用户名'
        elif User.objects.filter(username=username):
            errors = '用户名已存在'
        elif not password:
            errors = '请输入密码'
        elif (len(password) < 8):
            errors = '密码太短，请输入至少八位'
        elif not password2:
            errors = '请再次输入密码'
        elif password != password2:
            errors = '两次输入的密码不一致'
        else:
            user = User.objects.create_user(username, ' ', password)  # 添加用户
            user.is_active = True
            user.save
            userprofile = UserProfiles()
            userprofile.username = username  # 为用户创建个人信息条目
            userprofile.save()
            user = auth.authenticate(username=username, password=password)  # 注册后自动登录
            auth.login(request, user)
            request.session['username'] = username
            request.session['user_id'] = user.id
            return HttpResponseRedirect('/')

    return render(request, 'signup.html', locals())


def mylogout(request):  # 注销，暂时保存用户名
    username = request.session.get('username')
    auth.logout(request)
    return HttpResponseRedirect('/mylogin/')


def index(request):  # 已登录，显示主页，否则返回登录页面
    if request.user.is_authenticated():
        username = request.session.get('username')
        myprofile = UserProfiles.objects.get(username=username)
        showcontent = findMyall(username)
        return render(request, 'index.html', locals())
    else:
        return HttpResponseRedirect('/mylogin')


def send(request):  # 发布微博，并刷新页面
    if request.method == 'POST':
        content = request.POST['content']
        username = request.session.get('username')
        mycontent = Contents()
        mycontent.username = username
        mycontent.content = content
        mycontent.content_time = datetime.now()
        mycontent.save()
        userprofile = UserProfiles.objects.get(username=username)
        userprofile.contents_count += 1
        userprofile.save()
    return HttpResponseRedirect('/')


def discover(request):  # 发现页面，显示出所有人的微博
    allcontent = findAll()
    return render(request, 'discover.html', locals())


def getprofile(request):  # 获取个人信息
    username = request.session.get('username')
    try:  # 若是get请求，显示请求的人信息，否则显示自己信息
        follow_username = request.GET['username']
    except:
        follow_username = username
    userprofile = UserProfiles.objects.get(username=follow_username)
    contents = list(Contents.objects.filter(username=follow_username))
    if username == follow_username:
        pass
    elif Follows.objects.filter(username=username, follow_username=follow_username).exists():  # 已关注显示取消关注，否则显示关注
        showfollow = '取消关注'
    else:
        showfollow = '关注'
    return render(request, 'profile.html', locals())


def follow(request):  # 关注某人或取消关注
    username = request.session.get('username')
    if request.method == 'POST':
        follow_username = request.POST['username']
        userprofile = UserProfiles.objects.get(username=follow_username)
        contents = list(Contents.objects.filter(username=follow_username))
        if not Follows.objects.filter(username=username,
                                      follow_username=follow_username).exists():  # 若未关注则添加关注，否则删除关注关系
            newfollow = Follows()
            newfollow.username = username
            newfollow.follow_username = follow_username
            newfollow.save()
            myuserprofile = UserProfiles.objects.get(username=username)
            myuserprofile.follow_count += 1
            myuserprofile.save()
            userprofile.follower_count += 1
            userprofile.save()
            showfollow = '取消关注'
        else:
            Follows.objects.filter(username=username, follow_username=follow_username).delete()
            myuserprofile = UserProfiles.objects.get(username=username)
            myuserprofile.follow_count -= 1
            myuserprofile.save()
            userprofile.follower_count -= 1
            userprofile.save()
            showfollow = '关注'
    return render(request, 'profile.html', locals())


def comment(request):  # 查看此微博所有评论
    if request.GET:
        content_id = request.GET['content_id']
        request.session['content_id'] = content_id
    else:
        content_id = request.session.get('content_id')
    content = Contents.objects.get(id=content_id)
    comments = list(Comments.objects.filter(content_id=content_id))
    return render(request, 'comment.html', locals())


def sendcomment(request):  # 发布评论
    content_id = request.POST['content_id']
    comment = request.POST['comment']
    comment_username = request.session.get('username')
    newcomment = Comments()  # 添加评论
    newcomment.content_id = content_id
    newcomment.comment_username = comment_username
    newcomment.comment = comment
    newcomment.comment_time = datetime.now()
    newcomment.save()
    content = Contents.objects.get(id=content_id)  # 评论数加1
    content.comment_count += 1
    content.save()
    return HttpResponseRedirect('/comment/')


def listfollow(request):  # 列出关注人列表
    theusername = request.GET['username']
    theusers = list(Follows.objects.filter(username=theusername))
    theUserprofile = []
    for theuser in theusers:
        theUserprofile += list(UserProfiles.objects.filter(username=theuser.follow_username))
    return render(request, 'listfollow.html', locals())


def listfollower(request):  # 列出粉丝列表
    theusername = request.GET['username']
    theusers = list(Follows.objects.filter(follow_username=theusername))
    theUserprofile = []
    for theuser in theusers:
        theUserprofile += list(UserProfiles.objects.filter(username=theuser.username))
    return render(request, 'listfollower.html', locals())


def delcontent(request):  # 删除微博
    delcontent_id = request.GET['content_id']
    username = request.session['username']
    Comments.objects.filter(content_id=delcontent_id).delete()  # 删除所有评论
    Contents.objects.filter(id=delcontent_id).delete()  # 删除微博
    myprofile = UserProfiles.objects.get(username=username)  # 微博数减一
    myprofile.contents_count -= 1
    myprofile.save()
    return HttpResponseRedirect('/')


def delcomment(request):  # 删除评论
    delcomment_id = request.GET['comment_id']
    content_id = request.session['content_id']
    Comments.objects.filter(id=delcomment_id).delete()  # 删除评论
    thecontent = Contents.objects.get(id=content_id)  # 评论数减一
    thecontent.comment_count -= 1
    thecontent.save()
    return HttpResponseRedirect('/comment/')


def editprofile(request):  # 进入编辑个人资料
    username = request.session.get('username')
    myprofile = UserProfiles.objects.get(username=username)
    return render(request, 'editprofile.html', locals())


def updateprofile(request):  # 更新个人资料
    username = request.session.get('username')
    gender = request.POST['gender']
    birthday = request.POST['birthday']
    intro = request.POST['intro']
    myprofile = UserProfiles.objects.get(username=username)
    myprofile.gender = gender
    myprofile.birthday = birthday
    myprofile.intro = intro
    myprofile.save()
    return HttpResponseRedirect('/getprofile/')
