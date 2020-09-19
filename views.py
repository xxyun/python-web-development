from django.shortcuts import render,redirect
from firstapp.models import People,Article,Comment,Ticket
from django.template import Context, Template
from django.shortcuts import render, HttpResponse
from firstapp.form import CommentForm,LoginForm
from django.shortcuts import render, Http404, redirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist






# Create your views here.
def first_try(request):
    person=People(name='yun',job='manager')
    html_string = '''
        <html>
            <head>
                <meta charset="utf-8">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.6/semantic.css" media="screen" title="no title">
                <title>firstapp</title>
            </head>
            <body>
                <h1 class="ui center aligned icon header">
                    <i class="hand spock icon"></i>
                    Hello, {{ person.name }}
                </h1>
</body>
</html>
'''
    t = Template(html_string)
    c = Context({'person':person})
    web_page = t.render(c)
    return HttpResponse(web_page)

# def index(request):
#     queryset=request.GET.get('tag')
#     if queryset:
#         article_list = Article.objects.filter(tag=queryset)
#     else:
#         article_list = Article.objects.all()
# # 上面这段是在首页数据下拉栏中选择不同的标签，则首页只显示不同的标签对应文章
#
#     context = {}
#
#     context['article_list'] = article_list
#     index_page = render(request, 'first_web_2.html', context)
#     return index_page

def fweb(request):
    index_page1 = render(request, 'fweb.html')
    return index_page1



def Json(request):
    index_page1 = render(request, 'Json AJAX.html')
    return index_page1


# 表单视图
def detail(request,page_num, error_form=None):
    context = {}


# 投票显示
# 下一行是用来获取文章id对应的详细页面的
    vid_info = Article.objects.get(id=page_num)
    # 下面这一行代码是实现投票用的，需要调用用户的profile，若你是游客登录则看不了详情且会报错
    voter_id = request.user.profile.id
    like_counts = Ticket.objects.filter(choice='like', article_id=page_num).count()
    try:
        # 下一行是把投票哲的id和文章的id取出来
        user_ticket_for_this_video = Ticket.objects.get(voter_id=voter_id, article_id=page_num)
        context['user_ticket'] = user_ticket_for_this_video
    except:
        pass

    context['vid_info'] = vid_info
    context['like_counts'] = like_counts

# 评论表单
    form = CommentForm
    # 下一行是用来获取文章id对应的详细页面的
    a = Article.objects.get(id=page_num)
    best_comment = Comment.objects.filter(best_comment=True, belong_to=a)
    if best_comment:
        context['best_comment'] = best_comment[0]
    article = Article.objects.get(id=page_num)
    context['article'] = article
    # context['comment_list'] = comment_list
    # 表单验证
    if error_form is not None:
        context['form'] = error_form
    else:
        context['form'] = form
    return render(request, 'article_detail.html', context)

# 用户投票功能
def detail_vote(request, page_num):

    voter_id = request.user.profile.id

    try:
        user_ticket_for_this_video = Ticket.objects.get(voter_id=voter_id, article_id=page_num)
        user_ticket_for_this_video.choice = request.POST['vote']
        user_ticket_for_this_video.save()
    except ObjectDoesNotExist:
        new_ticket = Ticket(voter_id=voter_id, article_id=page_num, choice=request.POST['vote'])
        new_ticket.save()

    return redirect(to='detail', page_num=page_num)

# 一图多表，分离了文章详情页面的评论提交表单成一个新视图
def detail_comment(request, page_num):
    form = CommentForm(request.POST)

    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        a = Article.objects.get(id=page_num)
        c = Comment(name=name, comment=comment, belong_to=a)
        c.save()
    else:
        # 表单验证
        return detail(request, page_num, error_form=form)
        # 重定向
    return redirect(to='detail', page_num=page_num)



# 实现分页的index
def listing(request,cate=None):

    # vid_info = Article.objects.get(id=page_num)
    # context['vid_info'] = vid_info

    queryset = request.GET.get('tag')
    if queryset:
        article_list = Article.objects.filter(tag=queryset)
    else:
        article_list = Article.objects.all()

    # if cate is None:
    #     article_list = Article.objects.all()
    # if cate == 'popular':
    #     article_list = Article.objects.filter(popular_choice=True)
    # else:
    #     article_list = Article.objects.all()

    context = {}


    # 每页有9个信息
    page_robot = Paginator(article_list, 9)
    # 获取页数
    page_num = request.GET.get('page')


    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
        # raise Http404('EmptyPage!')     这个是返回404页面
    except PageNotAnInteger:
        article_list = page_robot.page(1)





    context['article_list'] = article_list
    return render(request,'first_web_2.html',context)





# 注册和登录
def index_login(request):
    context = {}
    if request.method == 'GET':

        form=AuthenticationForm
        # 这里用的是自己写的form.py里定义的LoginForm
        # form = LoginForm
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        # 这是用自己写的表单
        # form = LoginForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            # login(request, form.get_user())
            # return redirect(to='list')
            if user:
                login(request,user)
                return redirect(to='list')
            else:
                return HttpResponse('你输错了账户了不好意思')
    context['form'] = form
    return render(request, 'register_login.html', context)

def index_register(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # 表单的验证
        if form.is_valid():

            form.save()
            return redirect(to='login')
    context['form'] = form
    return render(request, 'register_login.html', context)
