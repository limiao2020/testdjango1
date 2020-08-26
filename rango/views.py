from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
# Create your views here.
from django.http import HttpResponse

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    category_dict = {"categories": category_list,"pages":page_list}
    return render(request,'rango/index.html',category_dict)

def about(request):
    context_dict = {'message': "ok!", 'head':"les's go!",'name':"limiao"}
    return render(request,'rango/about.html',context = context_dict)

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

    return render(request,'rango/category.html',context=context_dict)

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

def add_page(request):
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            cat = form.save(commit=True)
            print(cat)
            return index(request)
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form':form})