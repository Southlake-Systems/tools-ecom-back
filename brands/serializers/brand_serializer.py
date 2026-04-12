from rest_framework import serializers



from ..models import Brand



class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


    def create(self,validated_data):
        return Brand.objects.create(**validated_data)