from unittest import mock
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.views import get_groups
from users.serializers import GroupSerializer


class GroupViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @mock.patch('users.views.process_grp_file')
    def test_group_list(self, process_mock):
        all_groups = [{"name": "certusers",
                       "gid": "29",
                       "members": [
                           "root",
                           "_jabber",
                           "_postfix",
                           "_cyrus",
                           "_calendar",
                           "_dovecot"
                       ],
                       },
                      {"name": "_postdrop",
                       "gid": "28",
                       "members": []
                       }]

        process_mock.return_value = all_groups
        url = reverse('groups-list')
        response = self.client.get(url)
        serializer = GroupSerializer(instance=get_groups(settings.GRP_FILEPATH).values(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @mock.patch('users.views.process_grp_file')
    def test_group_retrieve(self, process_mock):
        all_groups = [{"name": "certusers",
                       "gid": "29",
                       "members": [
                           "root",
                           "_jabber",
                           "_postfix",
                           "_cyrus",
                           "_calendar",
                           "_dovecot"
                       ],
                       },
                      {"name": "_postdrop",
                       "gid": "28",
                       "members": []
                       }]
        process_mock.return_value = all_groups
        pk = '28'
        url = reverse('groups-detail', kwargs={'pk': pk})

        response = self.client.get(url)
        group = get_groups(settings.GRP_FILEPATH)[pk]
        serializer = GroupSerializer(instance=group)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @mock.patch('users.views.process_grp_file')
    def test_group_query(self, process_mock):
        all_groups = [{"name": "certusers",
                       "gid": "29",
                       "members": [
                           "root",
                           "_jabber",
                           "_postfix",
                           "_cyrus",
                           "_calendar",
                           "_dovecot"
                       ],
                       },
                      {"name": "_postdrop",
                       "gid": "28",
                       "members": []
                       }]
        process_mock.return_value = all_groups
        url = '{}?name=certusers&gid=29'.format(reverse('groups-query'))
        response = self.client.get(url)
        group = get_groups(settings.GRP_FILEPATH)['29']
        serializer = GroupSerializer(instance=[group], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

        url = '{}?name=blah'.format(reverse('groups-query'))
        response = self.client.get(url)
        # user with name blah doesn't exist, so 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
