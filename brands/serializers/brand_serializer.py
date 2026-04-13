from rest_framework import serializers



from ..models import Brand



class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


    def create(self,validated_data):
        return Brand.objects.create(**validated_data)
    
    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None