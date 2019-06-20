import pwd
import grp

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


all_users = []
for usr in pwd.getpwall():
    all_users.append()


class ListUsersView(APIView):
    """
    List all system users
    """
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)

    def get(self, request, format=None):
        """
        Returns a list of all users
        """
        result = []
        all_users = pwd.getpwall()
        for usr in all_users:
            result.append({'name': usr.pw_name,
                           'uid': usr.pw_uid,
                           'gid': usr.pw_gid,
                           'comment': usr.pw_gecos,
                           'home': usr.pw_dir,
                           'shell': usr.pw_shell,
                           })
        return Response(result)


class ListGroupsView(APIView):
    """
    List all groups
    """

    def get(self, request, format=None):
        """
        Returns a list of all groups
        """
        result = []
        all_groups = grp.getgrall()
        for group in all_groups:
            result.append({'name': group.gr_name,
                           'gid': group.gr_gid,
                           'members': group.gr_mem,
                           })
        return Response(result)


class UserDetailView(APIView):
    def get(self, request, uid, format=None):
        all_users = pwd.getpwall()
