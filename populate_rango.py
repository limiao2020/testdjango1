import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'testdjango.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
# 首先创建一些字典，列出想添加到各分类的网页
# 然后创建一个嵌套字典，设置各分类
# 这么做看起来不易理解，但是便于迭代，方便为模型添加数据

    python_pages = [
    {"title": "Official Python Tutorial",
    "url":"http://docs.python.org/2/tutorial/",
    "views":2},
    {"title":"How to Think like a Computer Scientist",
    "url":"http://www.greenteapress.com/thinkpython/",
    "views":4},
    {"title":"Learn Python in 10 Minutes",
    "url":"http://www.korokithakis.net/tutorials/python/",
    "views":16} ]

    django_pages = [
    {"title":"Official Django Tutorial",
    "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
    "views":3},
    {"title":"Django Rocks",
    "url":"http://www.djangorocks.com/",
    "views":6},
    {"title":"How to Tango with Django",
    "url":"http://www.tangowithdjango.com/",
    "views":9} ]

    other_pages = [
    {"title":"Bottle",
    "url":"http://bottlepy.org/docs/dev/",
    "views":4},
    {"title":"Flask",
    "url":"http://flask.pocoo.org",
    "views":15} ]

    cats = [["Python",python_pages,128,64],
            ["Django",django_pages,64,32],
            ["Other Frameworks",other_pages,32,16]]
# 如果想添加更多分类或网页，添加到前面的字典中即可

# 下述代码迭代 cats 字典，添加各分类，并把相关的网页添加到分类中
# 如果使用的是 Python 2.x，要使用 cats.iteritems() 迭代
# 迭代字典的正确方式参见
# http://docs.quantifiedcode.com/python-anti-patterns/readability/

    def add_page(cat, title, url, views=0):
        p = Page.objects.get_or_create(category=cat, title=title)[0]
        p.url=url
        p.views=views
        p.save()
        return p

    def add_cat(name,views,likes):
        c = Category.objects.get_or_create(name=name)[0]
        c.views = views
        c.likes = likes
        c.save()
        return c

    for cat in cats:
        c = add_cat(cat[0],cat[2],cat[3])
        for p in cat[1]:
            add_page(c, p["title"], p["url"],p["views"])

# 打印添加的分类
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

# 从这开始执行
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()