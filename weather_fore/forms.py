from django import forms
from django.db.models import Q

from .models import weather_grids, weather_codes, Grids, weather_area_update_message, weather_code_update_message
from django.core.exceptions import ValidationError
import string

class weather_grid_form(forms.ModelForm):
    class Meta:
        model = weather_grids
        fields = ["name", "sect_id", "forecast_area"]

    def clean_sect_id(self):
        sect_id = self.cleaned_data['sect_id']
        if '.' in sect_id:
            if sect_id.split('.')[1] == "":
                raise ValidationError("Enter the proper float")
            try:
                if isinstance(float(sect_id), float):
                    return float(sect_id)
            except Exception as e:
                print(e)
        raise ValidationError("invalid number please enter float")

    def clean_forecast_area(self):
        forecast_area = self.cleaned_data['forecast_area']
        if len(str(forecast_area)) > 3 or len(str(forecast_area)) < 3:
            raise ValidationError("please enter 3 integers")
        if forecast_area.isdigit():
            return forecast_area
        raise ValidationError("Please enter integer numbers")






class grids_form(forms.Form):
    grid_id = forms.CharField(label='Your name', max_length=1000000)


    def clean_grid_id(self):
        grids = list(self.cleaned_data['grid_id'].split(','))
        print(grids)
        for i in grids:
            for j in str(i):
                if j in string.punctuation:
                    raise ValidationError(f"Punctuation {j} not allow")
            if len(i) > 4 or len(i) < 4:
                raise ValidationError(f"invalid grid id {i} ")
            elif Grids.objects.filter(grid_id=i).exists():
                raise ValidationError(f"{i} is already exist. enter unique")


        return grids



# grid update form

class weather_grid_form_update(forms.ModelForm):
    class Meta:
        model = weather_grids
        fields = ["name", "sect_id", "forecast_area"]


    def clean_sect_id(self):
        sect_id = self.cleaned_data['sect_id']
        if '.' in sect_id:
            try:
                if isinstance(float(sect_id), float):
                    return sect_id
            except Exception as e:
                print(e)
        raise ValidationError("invalid number please enter float")

    def clean_forecast_area(self):
        forecast_area = self.cleaned_data['forecast_area']
        if forecast_area.isdigit():
            return forecast_area
        raise ValidationError("Please enter integer numbers")




class code_form(forms.ModelForm):
    class Meta:
        model = weather_codes
        fields = ['forecast', 'code', 'relation_in_char', 'intensity', 'area', 'legend']

    def clean_relation_in_char(self):
        relation_in_char = self.cleaned_data['relation_in_char']
        if "-" in relation_in_char and ":" in relation_in_char:
            raise ValidationError("relation allow only one from - or :")

        elif "-" not in relation_in_char and ":" not in relation_in_char:
            raise ValidationError("relation required - or :")
        elif "-" in relation_in_char:
            if weather_codes.objects.filter(Q(relation_in_char=relation_in_char) | Q(relation_in_char=relation_in_char.replace("-", ":"))).exists():
                raise ValidationError("Already exists")
        elif ":" in relation_in_char:
            if weather_codes.objects.filter(Q(relation_in_char=relation_in_char) | Q(relation_in_char=relation_in_char.replace(":", "-"))).exists():
                raise ValidationError(f"Already exists {relation_in_char}")

        return relation_in_char







class weather_area_update_form(forms.ModelForm):
    class Meta:
        model = weather_area_update_message
        fields = ['grid_id', 'action_code', 'area_id', 'area_name']


class weather_code_update_form(forms.ModelForm):
    class Meta:
        model = weather_code_update_message
        fields = ['action_code', "avalanche_code", "code_details"]





