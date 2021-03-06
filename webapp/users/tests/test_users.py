from unittest import mock
from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.views import get_users, get_groups
from users.serializers import UserSerializer, GroupSerializer


class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @mock.patch('users.views.process_pwd_file')
    def test_user_list(self, process_mock):
        all_users = [{'name': '_appowner',
                      'uid': '87',
                      'gid': '87',
                      'comment': 'Application Owner',
                      'home': '/var/empty',
                      'shell': '/usr/bin/false'},
                     {'name': '_ard',
                      'uid': '67',
                      'gid': '67',
                      'comment': 'Apple Remote Desktop',
                      'home': '/var/empty',
                      'shell': '/usr/bin/false'}]

        process_mock.return_value = all_users

        url = reverse('users-list')
        response = self.client.get(url)
        serializer = UserSerializer(instance=get_users(settings.PASSWD_FILEPATH).values(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @mock.patch('users.views.process_pwd_file')
    def test_user_retrieve(self, process_mock):
        all_users = [{'name': '_appowner',
                      'uid': '87',
                      'gid': '87',
                      'comment': 'Application Owner',
                      'home': '/var/empty',
                      'shell': '/usr/bin/false'},
                     {'name': '_ard',
                      'uid': '67',
                      'gid': '67',
                      'comment': 'Apple Remote Desktop',
                      'home': '/var/empty',
                      'shell': '/usr/bin/false'}]

        process_mock.return_value = all_users
        pk = '67'
        url = reverse('users-detail', kwargs={'pk': pk})

        response = self.client.get(url)
        user = get_users(settings.PASSWD_FILEPATH)[pk]
        serializer = UserSerializer(instance=user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @mock.patch('users.views.process_pwd_file')
    def test_user_retrieve_404(self, process_mock):
        all_users = [{'name': '_appowner',
                      'uid': '87',
                      'gid': '87',
                      'comment': 'Application Owner',
                      'home': '/var/empty',
                      'shell': '/usr/bin/false'},
                     {'name': '_ard',
                      'uid': '67',
                      'gid': '67',
                      'comment': 'Apple Remote Desktop',
                      'home': '/var/empty',
                      'shell': '/usr/bin/false'}]

        process_mock.return_value = all_users
        pk = '97'
        url = reverse('users-detail', kwargs={'pk': pk})

        response = self.client.get(url)
        # pk does not exist, should raise 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "User not found")

    @mock.patch('users.views.process_grp_file')
    @mock.patch('users.views.process_pwd_file')
    def test_user_groups(self, process_pwd_mock, process_grp_mock):
        all_users = [{'name': '_appowner',
                      'uid': '87',
                      'gid': '87',
                      'comment': 'Application Owner',
                      'home': '/var/empty',
                      'shell': '/usr/bin/false'},
                     {'name': '_ard',
                      'uid': '67',
                      'gid': '67',
                      'comment': 'Apple Remote Desktop',
                      'home': '/var/empty',
                      'shell': '/usr/bin/false'}]
        all_groups = [{"name": "certusers",
                       "gid": "29",
                       "members": [
                           "root",
                           "_jabber",
                           "_postfix",
                           "_cyrus",
                           "_calendar",
                           "_appowner"
                       ],
                       },
                      ]
        process_pwd_mock.return_value = all_users
        process_grp_mock.return_value = all_groups
        pk = '87'
        url = reverse('users-groups', kwargs={'pk': pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        groups = get_groups(settings.GRP_FILEPATH).values()
        serializer = GroupSerializer(instance=groups, many=True)
        self.assertEqual(response.data, serializer.data)

    @mock.patch('users.views.process_pwd_file')
    def test_user_query(self, process_mock):
        all_users = [{'name': '_appowner',
                      'uid': '87',
                      'gid': '87',
                      'comment': 'Application Owner',
                      'home': '/var/empty',
                      'shell': '/usr/bin/false'},
                     {'name': '_ard',
                      'uid': '67',
                      'gid': '67',
                      'comment': 'Apple Remote Desktop',
                      'home': '/var/empty',
                      'shell': '/usr/bin/false'}]
        process_mock.return_value = all_users
        url = '{}?name=_ard&uid=67'.format(reverse('users-query'))
        response = self.client.get(url)
        user = get_users(settings.PASSWD_FILEPATH)['67']
        serializer = UserSerializer(instance=[user], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

        # invalid user query
        url = '{}?name=nouser&uid=67'.format(reverse('users-query'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "User not found")

    @override_settings(PASSWD_FILEPATH='/etc/blah')
    def test_invalid_passwd_file(self):
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Invalid File: /etc/blah")
