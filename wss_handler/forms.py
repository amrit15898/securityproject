from django import forms
from .models import ws_sessions
from django.core.exceptions import ValidationError


class wss_session_form(forms.ModelForm):
    class Meta:
        model = ws_sessions
        fields = ["packet_id", "username", "password"]

    def clean_packet_id(self):
        packet_id = self.cleaned_data['packet_id']
        packet_list = list(packet_id.split(','))
        for i in packet_list:
            try:
             if int(i) > 15:
                raise ValidationError(f"{i} invalid packet id(enter b/w 0-15)")
            except Exception as e:
                raise ValidationError(f"{i} invalid packet id(enter b/w 0-15) integer")

        return packet_id





