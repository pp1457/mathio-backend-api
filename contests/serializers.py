from .models import Contest, Problem
from rest_framework import serializers

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id']

class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ['answer']

class SubmitAnswerSerializer(serializers.Serializer):
    user_answer = serializers.CharField(required=True, label='Answer')
