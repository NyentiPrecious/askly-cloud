from django import forms
from django.contrib.auth.models import User
from .models import Survey, Question

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["username", "email", "password"]

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["title", "description"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text"]

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["title", "description"]