from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.websearch import run_query

def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    category_dict = {"categories": category_list,"pages":page_list}
    visitor_cookie_handler(request)
    category_dict['visits'] = request.session['visits']

    response = render(request,'rango/index.html',category_dict)
    return response

@login_required(login_url='www.baidu.com')
def about(request):
    return render(request, 'rango/about.html', {})
    '''
    context_dict = {'message': "ok!", 'head':"les's go!",'name':"limiao"}
    return render(request,'rango/about.html',context = context_dict)
'''
def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    context_dict['query'] = category.name
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['query'] = query
    context_dict['result_list'] = result_list
    return render(request,'rango/category.html',context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            cat = form.save(commit=True)
            print(cat)
            return index(request)
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form':form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category =  category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

'''
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()


            profile = profile_form.save(False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',{'user_form': user_form,
                                                  'profile_form': profile_form,
                                                  'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user1 = authenticate(username=username, password=password)

        if user1:
            if user1.is_active:
                login(request,user1)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("your rango account is disabled.")
        else:
            print("invalid login details: {0},{1}".format(username,password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request,'rango/user_login.html',{})

@login_required
def user_logout(request):
# 可以确定用户已登录，因此直接退出
    logout(request)
# 把用户带回首页
    return HttpResponseRedirect(reverse('index'))
'''

@login_required
def restricted(request):
    return render(request,'rango/restricted.html',{})

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds > 10:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, dafault_val = None):
    val = request.session.get(cookie)
    if not val:
        val = dafault_val
    return val

def search(request):
    result_list = []
    query = ''
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
    return render(request, 'rango/search.html',{'result_list': result_list, 'query': query})

def track_url(request):
    page_id = None
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

            page = Page.objects.get(id=page_id)
            page.views = page.views + 1
            page.save()
            return HttpResponseRedirect(page.url)
        else:
            return HttpResponseRedirect(reverse('index'))

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'rango/profile_registration.html', context_dict)

@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
    if cat:
        likes = cat.likes + 1
    cat.likes = likes
    cat.save()
    return HttpResponse(likes)

def get_category_list(max_results=0,starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith = starts_with)
    else:
        cat_list = Category.objects.all()
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list

def suggest_category(request):
    cat_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    cat_list = get_category_list(8,starts_with)

    return render(request,'rango/cats.html',{'cats': cat_list})

@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
    p = Page.objects.get_or_create(category=category,
                                   title=title, url=url)
    pages = Page.objects.filter(category=category).order_by('-views')
    # 把网页列表传给模板上下文
    context_dict['pages'] = pages
    return render(request, 'rango/page_list.html', context_dict)