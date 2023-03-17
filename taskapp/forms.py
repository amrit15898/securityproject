from django.core.exceptions import ValidationError
from django import forms

#
# class send_message_form(forms.ModelForm):
#     class Meta:
#         model = Avalanche
#         fields = [
#             "message_str",
#             "sequence_num",
#             "packet_id",
#             "grid_id",
#             "fragment_id",
#             "no_fragment",
#             "axis_id"
#         ]

class FileFieldForm(forms.Form):
    file_field = forms.FileField()
