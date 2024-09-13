from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from stagiaires.models import Stagiaire

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    nom = forms.CharField(max_length=20, required=True)
    prenom = forms.CharField(max_length=20, required=False)
    telephone = forms.CharField(max_length=20, required=False)
    ecole = forms.CharField(max_length=50, required=False)
    abbreviation = forms.CharField(max_length=10, required=False)
    filiere = forms.CharField(max_length=20, required=False)
    niveau = forms.CharField(max_length=20, required=False)
    user_type = forms.ChoiceField(choices=[(0, 'Administrateur'), (1, 'Stagiaire')], required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Stagiaire.objects.create(
                user=user,
                nom=self.cleaned_data['nom'],
                prenom=self.cleaned_data['prenom'],
                email=self.cleaned_data['email'],
                telephone=self.cleaned_data['telephone'],
                ecole=self.cleaned_data['ecole'],
                abbreviation=self.cleaned_data['abbreviation'],
                filiere=self.cleaned_data['filiere'],
                niveau=self.cleaned_data['niveau']
            )
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)