from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from users.system_user import SystemUser
from users.serializers import UserSerializer

from users.system_group import SystemGroup
from users.serializers import GroupSerializer
from users.process_pwd import process_pwd_file
from users.process_grp import process_grp_file


def get_users(filepath):
    result = {}
    all_users = process_pwd_file(filepath)
    for usr in all_users:
        result[usr['uid']] = SystemUser(name=usr['name'],
                                        uid=usr['uid'],
                                        gid=usr['gid'],
                                        comment=usr['comment'],
                                        home=usr['home'],
                                        shell=usr['shell'],
                                        )
    return result


def get_groups(filepath):
    result = {}
    all_groups = process_grp_file(filepath)
    for grp in all_groups:
        result[grp['gid']] = SystemGroup(name=grp['name'],
                                         gid=grp['gid'],
                                         members=grp['members'],
                                         )
    return result


class UserViewSet(ViewSet):
    def initial(self, request, *args, **kwargs):
        super(UserViewSet, self).initial(request, *args, **kwargs)
        try:
            self.all_users = get_users(settings.PASSWD_FILEPATH)
        except IOError:
            raise NotFound('Invalid File: {}'.format(settings.PASSWD_FILEPATH))

    def list(self, request):
        """
        List all system users
        """
        serializer = UserSerializer(instance=self.all_users.values(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            user = self.all_users[pk]
        except KeyError:
            raise NotFound(detail="User not found", code=404)

        serializer = UserSerializer(instance=user)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def groups(self, request, pk=None):
        try:
            user = self.all_users[pk]
        except KeyError:
            raise NotFound(detail="User not found in any groups", code=404)

        try:
            groups = get_groups(settings.GRP_FILEPATH).values()
        except IOError:
            raise NotFound('Invalid File: {}'.format(settings.GRP_FILEPATH))

        try:
            groups = get_groups(settings.GRP_FILEPATH).values()
        except IOError:
            raise NotFound('Invalid File: {}'.format(settings.GRP_FILEPATH))

        filtered_groups = []
        for group in groups:
            if user.name in group.members:
                filtered_groups.append(group)

        serializer = GroupSerializer(instance=filtered_groups, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def query(self, request):
        filterset = self.all_users.values()
        username = request.query_params.get('name', None)
        uid = request.query_params.get('uid', None)
        gid = request.query_params.get('gid', None)
        comment = request.query_params.get('comment', None)
        home = request.query_params.get('home', None)
        shell = request.query_params.get('shell', None)

        if username is not None:
            filterset = [obj for obj in filterset if obj.name == username]

        if uid is not None:
            filterset = [obj for obj in filterset if obj.uid == uid]

        if gid is not None:
            filterset = [obj for obj in filterset if obj.gid == gid]

        if comment is not None:
            filterset = [obj for obj in filterset if obj.comment == comment]

        if home is not None:
            filterset = [obj for obj in filterset if obj.home == home]

        if shell is not None:
            filterset = [obj for obj in filterset if obj.shell == shell]

        if not filterset:
            raise NotFound(detail="User not found", code=404)

        serializer = UserSerializer(instance=filterset, many=True)
        return Response(serializer.data)


class GroupViewSet(ViewSet):
    def initial(self, request, *args, **kwargs):
        super(GroupViewSet, self).initial(request, *args, **kwargs)
        try:
            self.all_groups = get_groups(settings.GRP_FILEPATH)
        except IOError:
            raise NotFound('Invalid File: {}'.format(settings.GRP_FILEPATH))

    def list(self, request):
        serializer = GroupSerializer(instance=self.all_groups.values(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            group = self.all_groups[pk]
        except KeyError:
            raise NotFound(detail="Group not found", code=404)

        serializer = GroupSerializer(instance=group)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def query(self, request):
        groupname = request.query_params.get('name', None)
        gid = request.query_params.get('gid', None)
        members = request.query_params.getlist('member', None)

        filterset = self.all_groups.values()

        if groupname is not None:
            filterset = [obj for obj in filterset if obj.name == groupname]

        if gid is not None:
            filterset = [obj for obj in filterset if obj.gid == gid]

        if members is not None:
            filterset = [obj for obj in filterset if all(member_name in obj.members for member_name in members)]

        if not filterset:
            raise NotFound(detail="Group not found", code=404)

        serializer = GroupSerializer(instance=filterset, many=True)
        return Response(serializer.data)
