from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import AerosolOpticalDepthPolygon,PolygondataPM25
from rest_framework import serializers


class DateInputSerializer(serializers.Serializer):
    tanggal = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])

class PolygondataSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AerosolOpticalDepthPolygon
        geo_field = "geom"
        fields = ["aod_value"]

class PolygondataPM25Serializer(GeoFeatureModelSerializer):
    class Meta:
        model = PolygondataPM25
        geo_field = "geom"
        fields = ["pm25_value"]