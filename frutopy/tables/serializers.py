from rest_framework import serializers
from tables.models import Sample, ML_Model, SP_Model


class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'


class ML_ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ML_Model
        fields = '__all__'

class SP_ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SP_Model
        fields = '__all__'