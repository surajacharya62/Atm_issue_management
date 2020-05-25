from .models import AtmTerminalIdDetails
from rest_framework import serializers


class AtmTerminalIdDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AtmTerminalIdDetails
        fields = ['s_n', 'atm_terminal_id']

    # s_n = serializers.IntegerField()
    # atm_terminal_id = serializers.CharField(max_length=8)

    # def create(self, validated_data):
    #     return AtmTerminalIdDetails.objects.create(validated_data)

    # def update(self, instance, validated_data):
    #     instance.s_n = validated_data.get('s_n', instance.s_n)
    #     instance.s_n = validated_data.get(
    #         'atm_terminal_id', instance.atm_terminal_id)
    #     return instance
