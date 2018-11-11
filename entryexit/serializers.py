from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from rest_framework import serializers
from entryexit.models import EntryExit, Building
from people.models import People

class EntryExitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryExit
        fields = ('id_name',  'entrytimestamp','exittimestamp', 'building_id')
    
    def validate(self, data):
        id_name = data.get('id_name', None)
        building_id = data.get('building_id', None)
        try:
            People.objects.get(pk = id_name)
        except People.DoesNotExist:
            return ValidationError("The Person is not registered")
        try:
            Building.objects.get(pk = building_id)
        except Building.DoesNotExist:
            return ValidationError("The Building is not registered") 
        return data

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('id',  'name')