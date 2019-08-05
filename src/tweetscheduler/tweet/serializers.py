from rest_framework import serializers
from .models import DmUserList


class DmUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = DmUserList
        fields = ('id', 'user_id', 'user_name')
