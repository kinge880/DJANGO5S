from rest_framework import serializers, status
from sectors.models import branch, sectors, userSectors, sectorsImage, sectorsGroup
from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework.response import Response

class userSectorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = userSectors
        fields = '__all__'

class imageSectorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = sectorsImage
        fields = '__all__'

class SectorImageSerializer(serializers.ModelSerializer):
    image = serializers.StringRelatedField()
    class Meta:
        model = sectors
        fields = '__all__'

class SectorGroupImageSerializer(serializers.ModelSerializer):
    image = serializers.StringRelatedField()
    class Meta:
        model = sectorsGroup
        fields = '__all__'

class sectorsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = sectorsGroup
        fields = '__all__'
    
    def update(self, instance, validated_data):
        sectorGroup = instance
        super().update(instance, validated_data)
        
        if validated_data.get('is_active') != None:
            sectors.objects.filter(sectorGroup = sectorGroup.id).update(is_active = validated_data.get('is_active'))
        
        if validated_data.get('branchName') != None:
            sectors.objects.filter(sectorGroup = sectorGroup.id).update(branchName = validated_data.get('branchName'))
       
        return instance
    
class sectorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = sectors
        fields = '__all__'

class branchSerializers(serializers.ModelSerializer):
    class Meta:
        model = branch
        fields = '__all__'
        extra_kwargs = {
                'number': {
                    'validators': [
                        UniqueValidator(
                            queryset=branch.objects.all(),
                            message = 'Já existe uma filial com esse número!'
                        )
                    ]
                }
            }
