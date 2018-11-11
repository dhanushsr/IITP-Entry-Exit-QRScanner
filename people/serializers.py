from django.contrib.auth.models import User, Group
from rest_framework import serializers
from people.models import People

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class PeopleSerializer(serializers.Serializer):
    id = serializers.CharField(required = True)
    name = serializers.CharField(required = False)
    phone = serializers.CharField(required = False)
    photo = serializers.ImageField(required = False)
    email = serializers.EmailField(required = False)
    
    def create(self, validated_data):
        return People.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


