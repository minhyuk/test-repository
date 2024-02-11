from django import forms

class RespiratoryGraphForm(forms.Form):
    csv_input = forms.CharField()
    time_input = forms.CharField()
    note_input = forms.CharField(required=False)
    
class SustainedAttentionForm(forms.Form):
    csv_input = forms.CharField()
    rate_input = forms.JSONField(required=False)
    time_input = forms.CharField()
    note_input = forms.CharField(required=False)