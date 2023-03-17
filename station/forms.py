from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re

class station_form(forms.ModelForm):
    class Meta:
        model = Station
        fields = ["station_name", "station_id", "latitude", "longitude", "terminal_id"]

    def clean_latitude(self):
        latitude = self.cleaned_data['latitude']
        if '.' in latitude:
            try:
                if isinstance(float(latitude), float):
                    return latitude
            except Exception as e:
                print(e)
        raise ValidationError("invalid latitude please enter float")

    def clean_longitude(self):
        longitude = self.cleaned_data['longitude']
        if '.' in longitude:
            try:
                if isinstance(float(longitude), float):
                    return longitude
            except Exception as e:
                print(e)
        raise ValidationError("invalid longitude please enter float")

    def clean_station_id(self):
        station_id = self.cleaned_data['station_id']
        if len(str(station_id)) > 5:
            raise ValidationError("Enter 5 digit number only")
        return station_id

    def clean_terminal_id(self):
        terminal_id = self.cleaned_data['terminal_id']
        if len(str(terminal_id)) > 5:
            raise ValidationError("Enter 5 digit number only")
        return terminal_id



class equation_form(forms.ModelForm):
    class Meta:
        model = Equation
        fields = ['equation']

    def clean_equation(self):
        equation = self.cleaned_data['equation']
        match = re.match(r'^\(?(\d*x)?\+?(\d*y)?\)?=?(\d+\.?\d*)$', equation)
        print(match)
        if match:
            if match.group(1) is None:
                raise ValidationError(f"Variable x is missing in equation {equation}")
            if match.group(2) is None:
                raise ValidationError(f"Variable y is missing in equation {equation}")
            if '.' in match.group(3):
                raise ValidationError(f"Equation {equation} has a non-integer value on the right-hand side.")
        else:
            raise ValidationError(f"Equation {equation} is not in the correct format.")

        return equation



