from rest_framework import serializers
from .models import Content,Topic
from django.contrib.auth.models import User

# class RangeFieldSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = rangefield
#         fields = '__all__'


class ContentSeralizer(serializers.ModelSerializer):

    class Meta:
        model = Content
        # fields = ['id', 'text', 'code', 'output']
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    content = ContentSeralizer(read_only=True, many=True)
    
    class Meta:
        model = Topic
        # fields = ['id','name']
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user