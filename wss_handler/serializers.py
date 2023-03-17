from rest_framework import serializers



class ws_auth_serializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)
    packet_id = serializers.CharField(max_length=200)
    session_id = serializers.CharField(max_length=200)
    log_message = serializers.CharField(max_length=200)
    class Meta:
        fields = ["username", "password", "packet_id", "session_id", "log_message"]



class message_ack_serializer(serializers.Serializer):
    sequence_num = serializers.IntegerField()
    packet_id =serializers.IntegerField()




