from django import forms

class RespiratoryGraphForm(forms.Form):
    csv_input = forms.CharField()
    time_input = forms.CharField()
    note_input = forms.CharField(required=False)