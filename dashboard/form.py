from django import forms
from .models import Pointers, wss_auth_user
from .validator import text_validate
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from taskapp.models import avalanche_axis
import re
import string


class pointer_form(forms.ModelForm):
    class Meta:
        model = Pointers
        fields = ["title", "longitude", "latitude", "point_type"]

    def clean_title(self):
        title = self.cleaned_data['title']
        if text_validate(title):
            raise ValidationError("Invalid title please enter only alphabet ")

        return title

    def clean_longitude(self):
        longitude = self.cleaned_data['longitude']
        if type(longitude) == float:
            if len(str(longitude).split('.')[0]) == 2 and len(str(longitude).split('.')[1]) > 1:
                return longitude
        raise ValidationError("Invalid longitude please enter only flot value ")

        return longitude

    def clean_latitude(self):
        latitude = self.cleaned_data['latitude']
        if type(latitude) == float:
            if len(str(latitude).split('.')[0]) == 2 and len(str(latitude).split('.')[1]) > 1:
                return latitude
        raise ValidationError("Invalid latitude please enter only flot value ")


class user_form(forms.ModelForm):
    confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name"]

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']

        if password != confirm_password:
            raise ValidationError("The two password fields didn’t match.")
        return confirm_password

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if text_validate(first_name):
            raise ValidationError("Invalid first name please enter only alphabet ")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if text_validate(last_name):
            raise ValidationError("Invalid last name please enter only alphabet ")

        return last_name


class user_update_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if text_validate(first_name):
            raise ValidationError("Invalid first name please enter only alphabet ")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if text_validate(last_name):
            raise ValidationError("Invalid last name please enter only alphabet ")

        return last_name


class add_wss_form(forms.ModelForm):
    confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = wss_auth_user
        fields = ["username", "password"]

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']

        if password != confirm_password:
            raise ValidationError("The two password fields didn’t match.")
        return confirm_password

import collections
class avalanche_axis_form(forms.ModelForm):
    class Meta:
        model = avalanche_axis
        fields = ["avalanche_axis", "avalanche_axis_code", "aor", "grids", "axis_code_afg"]

    def clean_axis_code_afg(self):
        axis_code_afg = self.cleaned_data['axis_code_afg']
        if avalanche_axis.objects.filter(axis_code_afg=axis_code_afg).exists():
            raise ValidationError("axis code afg already exists! please enter unique")
        return axis_code_afg

    def clean_grids(self):
        grids = list(self.cleaned_data['grids'].split(','))
        for i in grids:
            for j in str(i):
                if j in string.punctuation:
                    raise ValidationError(f"Punctuation {j} not allow")
            if len(i) > 4 or len(i) < 4:
                raise ValidationError(f"invalid grid id {i} ")

        for item, count in collections.Counter(grids).items():
            if count > 1:
                print(item)
                raise ValidationError(f"Duplicate value {item}")
        return grids


class update_avalanche_axis_form(forms.ModelForm):
    class Meta:
        model = avalanche_axis
        fields = ["avalanche_axis", "avalanche_axis_code", "aor", "axis_code_afg"]

    def clean_axis_code_afg(self):
        axis_code_afg = self.cleaned_data['axis_code_afg']
        if avalanche_axis.objects.filter(axis_code_afg=axis_code_afg).exists():
            raise ValidationError("axis code afg already exists! please enter unique")
        return axis_code_afg

