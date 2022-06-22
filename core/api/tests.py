from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from faker import Faker

from api.models import MyUser


class MyUserTests(APITestCase):
    def setUp(self):
        fake = Faker()

        MyUser.objects.create_user(
            email='aaa@net.com',
            is_admin=True,
            password='0112358',
            birthday='2022-04-29')
        MyUser.objects.create_user(
            email='bbb@daa.com',
            is_admin=False,
            password='0112358',
            birthday='2020-01-20')

        for _ in range(9):
            MyUser.objects.create_user(
                email=fake.email(),
                password=fake.password(),
                is_admin=False,
                first_name=fake.first_name()
            )

    def test_get_general_users_information(self):
        PAGE = 4
        SIZE = 2

        self.client.login(username='aaa@net.com', password='0112358')

        url = reverse('general_users_information')
        response = self.client.get(url, format='json')
        pagination_data = response.json().get('meta').get('pagination')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MyUser.objects.count(), 11)
        self.assertEqual(pagination_data.get('page'), 1)
        self.assertEqual(pagination_data.get('size'), 3)

        url += f'?page={PAGE}&size={SIZE}'
        response = self.client.get(url, format='json')
        pagination_data = response.json().get('meta').get('pagination')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(pagination_data.get('page'), PAGE)
        self.assertEqual(pagination_data.get('size'), SIZE)

        data_fields = [
            field for field in response.json().get('data')[0].keys()
        ]
        self.assertEqual(
            data_fields, ['id', 'first_name', 'last_name', 'email']
        )

    def test_get_general_users_information_unauth(self):

        self.client.logout()

        url = reverse('general_users_information')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_current_user_information(self):

        self.client.login(username='aaa@net.com', password='0112358')

        url = reverse('current_user_information')
        response = self.client.get(url, format='json')
        current_user_information = {
            'first_name': '',
            'last_name': '',
            'other_name': '',
            'email': 'aaa@net.com',
            'phone': '',
            'birthday': '2022-04-29',
            'is_admin': True
        }
        self.assertEqual(response.json(), current_user_information)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user_information_unauth(self):

        self.client.logout()

        url = reverse('current_user_information')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_current_user_information(self):

        self.client.login(username='aaa@net.com', password='0112358')

        user = MyUser.objects.get(email='aaa@net.com')
        url = f'/api/user/users/{user.id}/'
        user = MyUser.objects.get(email='aaa@net.com')
        data = {
            'phone': '+7777777778',
            'birthday': '2022-03-28'
        }

        response = self.client.patch(url, data, format='json')
        eq_data = {
            'first_name': '',
            'last_name': '',
            'other_name': '',
            'email': 'aaa@net.com',
            'phone': '+7777777778',
            'birthday': '2022-03-28'
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, eq_data)

        data = {
            'phone': '+7777777778',
            'is_admin': 'True'
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_list_private_user(self):

        self.client.login(username='aaa@net.com', password='0112358')

        url = '/api/admin/private/users/'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list_private_user(self):

        self.client.login(username='aaa@net.com', password='0112358')

        url = '/api/admin/private/users/'
        data = {
            'first_name': "Владимир",
            'last_name': "Краснов",
            'email': "krasnov@mail.ru",
            'is_admin': "True",
            "password": "0112358"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MyUser.objects.count(), 12)

    def test_get_id_list_private_user(self):

        self.client.login(username='aaa@net.com', password='0112358')

        user = MyUser.objects.get(email='aaa@net.com')
        url = f'/api/admin/private/users/{user.id}/'
        response = self.client.get(url, format='json')
        data_fields = [
            field for field in response.json().keys()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data_fields, ['id', 'first_name', 'last_name', 'other_name',
                          'email', 'phone', 'birthday', 'city',
                          'additional_info', 'is_admin']
        )

    def test_delete_list_private_user(self):

        self.client.login(username='aaa@net.com', password='0112358')

        url = '/api/admin/private/users/10/'
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MyUser.objects.count(), 10)

    def test_patch_list_private_user(self):

        self.client.login(username='aaa@net.com', password='0112358')

        user = MyUser.objects.get(email='aaa@net.com')
        url = f'/api/admin/private/users/{user.id}/'
        user = MyUser.objects.get(email='aaa@net.com')
        data = {
            'phone': '+7777777778',
            'birthday': '2022-03-28',
            'additional_info': 'Coolboy with BFG 2000',
            "city": "Колыма"
        }

        response = self.client.patch(url, data, format='json')
        eq_data = {
            'id': 1,
            'first_name': '',
            'last_name': '',
            'other_name': '',
            'email': 'aaa@net.com',
            'phone': '+7777777778',
            'birthday': '2022-03-28',
            'city': 'Колыма',
            'additional_info': 'Coolboy with BFG 2000',
            'is_admin': True
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, eq_data)
