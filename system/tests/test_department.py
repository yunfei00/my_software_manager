# system/tests/test_department.py
from django.test import TestCase
from django.urls import reverse
from system.models import Department

class TestDepartmentModel(TestCase):
    def test_create_department(self):
        # 创建部门实例，不使用 code
        dept = Department.objects.create(name="研发部")
        self.assertEqual(dept.name, "研发部")
        self.assertTrue(dept.status)  # 默认启用状态
        self.assertIsNone(dept.parent)  # 默认没有父部门

class TestDepartmentViews(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="测试部")

    def test_department_list_view(self):
        # 假设你有 department_list URL name
        response = self.client.get(reverse("system:department_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "测试部")

    def test_department_export_csv(self):
        # 假设你有 department_export_csv URL name
        response = self.client.get(reverse("department_export_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])
        self.assertIn("测试部", response.content.decode("utf-8"))
