from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from userauths.models import User, Profile
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["phone", "username", "first_name",
                  "last_name", "email", "password1", "password2"]
        field_classes = {"username": UsernameField}
        widgets = {
            "username": forms.TextInput({"placeholder": _("Username")}),
            "phone": forms.TextInput({"placeholder": _("Phone No.")}),
            "first_name": forms.TextInput({"placeholder": _("First Name")}),
            "last_name": forms.TextInput({"placeholder": _("Last Name")}),
            "email": forms.EmailInput({"placeholder": _("Email")}),
            "password1": forms.PasswordInput(
                attrs={
                    "placeholder": _("New Password"),
                    "autocomplete": "new-password",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "placeholder": _("Confirm Password"),
                    "autocomplete": "new-password",
                }
            ),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "image"
        ]
        widgets = {
            'first_name': forms.TextInput({"placeholder": _("First Name")}),
            'last_name': forms.TextInput({"placeholder": _("Last Name")}),
            'username': forms.TextInput({"placeholder": _("Username")}),
            'phone': forms.TextInput({"placeholder": _("Phone")}),
            'email': forms.TextInput({"placeholder": _("Email")}),
        }


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Full Name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Bio"}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Phone"}))

    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']
