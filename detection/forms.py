from django import forms
from .models import BusinessDetectionTool, PreDetectionRequest, DetectionTool

class BusinessDetectionToolForm(forms.ModelForm):
    tools = forms.ModelMultipleChoiceField(
        queryset=DetectionTool.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = BusinessDetectionTool
        fields = ['tools']

class PreDetectionRequestForm(forms.ModelForm):
    tools = forms.ModelMultipleChoiceField(
        queryset=DetectionTool.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = PreDetectionRequest
        fields = ['tools']
