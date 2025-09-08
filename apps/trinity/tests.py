from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from apps.merovingian.models import Course

from .models import CourseLearningOutcome, EducationArea, ModuleLearningOutcome


class ResponseTest(TestCase):
    fixtures = ['merovingian/base', 'trinity/base', 'trainman/base',
                'trinity/response/department', 'trinity/response/course', 'trinity/response/clo']

    def setUp(self):
        self.client = Client()

        self.super_user = User.objects.get(pk=1)
        self.superuser_client = Client()
        self.superuser_client.force_login(self.super_user)

    def test_ea_response(self):
        # ---------------------------------------
        # --- ASSIGN
        # ---------------------------------------

        url = reverse('trinity:ea:assign', kwargs={'course_id': 1})
        expected_url = reverse('trainman:login') + '/?next=' + url
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)

        url = reverse('trinity:ea:assign', kwargs={'course_id': 1})
        response = self.superuser_client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('trinity:ea:assign', kwargs={'course_id': 1})
        expected_url = url
        data = {'education_areas': [1, 2]}
        response = self.superuser_client.post(url, data)
        self.assertRedirects(response, expected_url)

        course = Course.objects.get(id=1)
        self.assertSequenceEqual(course.education_areas.values_list('id', flat=True), [1, 2])

        # ---------------------------------------
        # --- ASSIGN PHD
        # ---------------------------------------

        url = reverse('trinity:ea:assign_phd', kwargs={'course_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        url = reverse('trinity:ea:assign_phd', kwargs={'course_id': 1})
        expected_url = reverse('merovingian:course:details', kwargs={'course_id': 1})
        response = self.superuser_client.get(url, follow=True)
        self.assertRedirects(response, expected_url)

        url = reverse('trinity:ea:assign_phd', kwargs={'course_id': 2})
        response = self.superuser_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_clo_response(self):
        # ---------------------------------------
        # --- SHOW
        # ---------------------------------------

        url = reverse('trinity:clo:show', kwargs={'course_id': 1, 'education_category_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # ---------------------------------------
        # --- ADD
        # ---------------------------------------

        url = reverse('trinity:clo:add', kwargs={'course_id': 1, 'education_category_id': 1})
        response = self.superuser_client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('trinity:clo:add', kwargs={'course_id': 1, 'education_category_id': 1})
        expected_url = url
        data = {'symbol': 'X', 'description': 'X', 'education_category': 1, 'course': 1}
        response = self.superuser_client.post(url, data)
        self.assertRedirects(response, expected_url)

        # ---------------------------------------
        # --- UPDATE
        # ---------------------------------------

        url = reverse('trinity:clo:update', kwargs={'course_id': 1, 'education_category_id': 1, 'clo_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        url = reverse('trinity:clo:update', kwargs={'course_id': 1, 'education_category_id': 1, 'clo_id': 1})
        response = self.superuser_client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('trinity:clo:update', kwargs={'course_id': 1, 'education_category_id': 1, 'clo_id': 1})
        data = {'symbol': 'X', 'description': 'X', 'education_category': 1, 'course': 1}
        response = self.superuser_client.post(url, data)
        self.assertEqual(response.status_code, 302)

        # ---------------------------------------
        # --- DELETE
        # ---------------------------------------

        url = reverse('trinity:clo:delete', kwargs={'course_id': 1, 'education_category_id': 1})
        data = {'selected_id': [1]}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CourseLearningOutcome.objects.filter(id=1).exists())

        url = reverse('trinity:clo:delete', kwargs={'course_id': 1, 'education_category_id': 1})
        data = {'selected_id': [1]}
        response = self.superuser_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CourseLearningOutcome.objects.filter(id=1).exists())

    def test_mlo_response(self):
        # ---------------------------------------
        # --- SELECT SGROUP
        # ---------------------------------------

        url = reverse('trinity:mlo:select_sgroup', kwargs={'course_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('trinity:mlo:select_sgroup', kwargs={'course_id': 1})
        data = {'sgroup': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        # ---------------------------------------
        # --- SELECT MODULE
        # ---------------------------------------

        url = reverse('trinity:mlo:select_module', kwargs={'course_id': 1, 'sgroup_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('trinity:mlo:select_module', kwargs={'course_id': 1, 'sgroup_id': 1})
        data = {'module': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        # ---------------------------------------
        # --- SHOW
        # ---------------------------------------

        url = reverse('trinity:mlo:show', kwargs={'course_id': 1, 'sgroup_id': 1, 'module_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # ---------------------------------------
        # --- ADD
        # ---------------------------------------

        url = reverse('trinity:mlo:add', kwargs={'course_id': 1, 'sgroup_id': 1, 'module_id': 1})
        response = self.superuser_client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('trinity:mlo:add', kwargs={'course_id': 1, 'sgroup_id': 1, 'module_id': 1})
        data = {'symbol': 'X', 'description': 'X', 'course': 1, 'sgroup': 1, 'module': 1}
        response = self.superuser_client.post(url, data)
        self.assertEqual(response.status_code, 302)

        # ---------------------------------------
        # --- UPDATE
        # ---------------------------------------

        url = reverse('trinity:mlo:update', kwargs={'course_id': 1, 'sgroup_id': 1, 'module_id': 1, 'mlo_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        url = reverse('trinity:mlo:update', kwargs={'course_id': 1, 'sgroup_id': 1, 'module_id': 1, 'mlo_id': 1})
        response = self.superuser_client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('trinity:mlo:update', kwargs={'course_id': 1, 'sgroup_id': 1, 'module_id': 1, 'mlo_id': 1})
        data = {'symbol': 'X', 'description': 'X', 'course': 1, 'sgroup': 1, 'module': 1}
        response = self.superuser_client.post(url, data)
        self.assertEqual(response.status_code, 302)

        # ---------------------------------------
        # --- DELETE
        # ---------------------------------------

        url = reverse('trinity:mlo:delete', kwargs={'course_id': 1, 'sgroup_id': 1, 'module_id': 1})
        data = {'selected_id': [1]}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ModuleLearningOutcome.objects.filter(id=1).exists())

        url = reverse('trinity:mlo:delete', kwargs={'course_id': 1, 'sgroup_id': 1, 'module_id': 1})
        data = {'selected_id': [1]}
        response = self.superuser_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ModuleLearningOutcome.objects.filter(id=1).exists())
