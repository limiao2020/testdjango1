from django.test import TestCase
from rango.models import Category
# Create your tests here.
class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive 函数在分类的查看次数
        为零或正数时应该返回 True
        """
        cat = Category(name='test',views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)