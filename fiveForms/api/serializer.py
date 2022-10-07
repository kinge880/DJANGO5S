
from rest_framework import serializers
from fiveForms.models import fiveForm, fiveFormAsk, fiveFormResponse, fiveFormResponseImage
from rest_framework.validators import UniqueValidator
from accounts.api import serializer as userSerializer

class fiveFormSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = fiveForm
        fields = '__all__'
        read_only_fields = ['userId']

    def create(self, validated_data):
        validated_data['title'] = validated_data['title'].strip()
        validated_data['userId'] = self.context['request'].user
        return fiveForm.objects.create(**validated_data)

class fiveFormRelatorySerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = fiveForm
        fields = '__all__'
        read_only_fields = ['userId']
    
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["is_active"] = instance.is_active
        representation["userId"] = instance.userId.first_name
        representation["sectorGroup"] = instance.sectorId.sectorGroup.name
        representation["sectorGroupId"] = int(instance.sectorId.sectorGroup.id)
        representation["sector"] = instance.sectorId.name
        representation["sectorId"] = int(instance.sectorId.id)
        representation["title"] = instance.title
        representation["description"] = instance.description
        representation["start_at"] = instance.start_at
        representation["end_at"] = instance.end_at
        representation["created_at"] = instance.created_at
        representation["updated_at"] = instance.updated_at

        return representation


class askSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = fiveFormAsk
        fields = '__all__'
    
    def create(self, validated_data):
        return fiveFormAsk.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.ask = validated_data.get('ask', instance.ask)
        instance.askweight = validated_data.get('askweight', instance.askweight)
        instance.formId = validated_data.get('formId', instance.formId)
        instance.is_image = validated_data.get('is_image', instance.is_image)
        instance.save()
        return instance

class responseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = fiveFormResponse
        fields = '__all__'
        read_only_fields = ['userId']
    
    def create(self, validated_data):
        validated_data['response'] = validated_data['response'].strip()
        validated_data['userId'] = self.context['request'].user
        return fiveFormResponse.objects.create(**validated_data)

class responseWithImageSerializer(serializers.ModelSerializer):
    image = serializers.StringRelatedField()
    class Meta:
        model = fiveFormResponse
        fields = '__all__'
        read_only_fields = ['userId']
    
    def create(self, validated_data):
        validated_data['response'] = validated_data['response'].strip()
        validated_data['userId'] = self.context['request'].user
        return fiveFormResponse.objects.create(**validated_data)

class responseWithImageRelatorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = fiveFormResponse
        fields = '__all__'
        read_only_fields = ['userId']
    
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        if str(instance.image) != 'None':
            representation["image"] = 'http://127.0.0.1:8000/media/'+str(instance.image.image)
        else:
            representation["image"] = 'None'
        representation["responseweight"] = instance.responseweight
        representation["response"] = instance.response
        representation["userId"] = instance.userId.first_name
        representation["askId"] = instance.askId.id
        representation["Ask"] = instance.askId.ask
        representation["askweight"] = instance.askId.askweight
        representation["is_image"] = instance.askId.is_image
        representation["formId"] = instance.formId.id
        representation["formName"] = instance.formId.title
        representation["formStart_at"] = instance.formId.start_at
        representation["formEnd_at"] = instance.formId.end_at
        representation["created_at"] = instance.formId.created_at
        representation["updated_at"] = instance.formId.updated_at
        representation["sectorGroup"] = str(instance.formId.sectorId.sectorGroup.name)
        representation["sectorGroupId"] = int(instance.formId.sectorId.sectorGroup.id)
        representation["sector"] = str(instance.formId.sectorId.name)
        representation["sectorId"] = int(instance.formId.sectorId.id)
        
        return representation

class responseImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = fiveFormResponseImage
        fields = '__all__'
