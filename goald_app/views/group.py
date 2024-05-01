"""
File for defining handlers for group in Django notation
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from ..models import User, Group
from ..serializers import GroupSerializer


class GroupView(APIView):
    """
       Description of GroupView
    """

    def get(self, request, **kwargs):
        """
        Handler for reading the group info
        """

        user_id = self.request.session["id"]
        group_id = self.kwargs.get("id", None)

        if not group_id:
            user_groups = User.objects.get(id=user_id).groups
            leader_group = Group.objects.filter(leader_id=user_id)
            queryset = user_groups.union(leader_group)
            return Response(
                data=GroupSerializer(queryset, many=True).data,
            status=status.HTTP_200_OK
            )

        if not Group.objects.filter(id=group_id).exists():
            return Response(
                data={"detail": "Group does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not User.objects.get(id=user_id).groups.filter(id=group_id).exists() \
            and not Group.objects.filter(id=group_id, leader_id=user_id).exists():
            return Response(
                data={"detail": "You have no permission to have this info"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        group = Group.objects.get(id=kwargs["id"])
        return Response(
            data=GroupSerializer(instance=group).data,
            status=status.HTTP_200_OK
        )


    def post(self, request):
        """
        Handler for creating a group
        """

        serializer = GroupSerializer(data=request.data, context={'request': request})

        if Group.objects.filter(tag=request.data["tag"]).exists():
            raise serializers.ValidationError("Group with this tag already exists")

        if not serializer.is_valid(raise_exception=True):
            return Response(
                data={"detail": "Group data is not valid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            data={"detail", f"Group id: {serializer.data}"},
            status=status.HTTP_201_CREATED
        )


    def patch(self, request, **kwargs):
        """
        Handler for updating the group info
        """

        group_id = kwargs.get("id", None)
        if not group_id:
            return Response(
                data={"detail": "No id given"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not Group.objects.filter(id=group_id).exists():
            return Response(
                data={"detail": "group with given id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not Group.objects.filter(id=group_id, leader_id=request.session["id"]).exists():
            return Response(
                data={"detail": "You have no permission to change group info"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        instance = Group.objects.get(id = group_id)

        serializer = GroupSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={"detail": "Group info updated"},
            status=status.HTTP_200_OK
        )


    def delete(self, request, **kwargs):
        """
        Handler for deleting the group
        """

        user_id = request.session["id"]
        group_id = kwargs.get("id", None)

        if not group_id:
            return Response(
                data={"detail": "No id given"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not Group.objects.filter(id=group_id).exists():
            return Response(
                data={"detail": "No group with given id found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not Group.objects.filter(id=group_id, leader_id=user_id).exists():
            return Response(
                data={"detail": "You have no permission to delete group"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        Group.objects.get(id=group_id).delete()

        return Response(
            data={"detail": "Group deleted"},
            status=status.HTTP_200_OK
        )
