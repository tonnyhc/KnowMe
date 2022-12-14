from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model, password_validation
from django.forms import TextInput, PasswordInput

from knowme.accounts.models import Profile, ProfileReport

UserModel = get_user_model()

#TODO: make the registration with Email confirmation
class UserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username')
        field_classes = {
            'email': auth_forms.UsernameField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat password'

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email']



class CustomAuthForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture', 'first_name', 'last_name', 'bio', 'gender', 'birth_date']
        widgets = {
            'picture': forms.FileInput(),
            'first_name': forms.TextInput(attrs={'placeholder': "First Name"}),
            'last_name': forms.TextInput(attrs={'placeholder': "Last Name"}),
            'bio': forms.Textarea(attrs={'placeholder': "Enter a bio to introduce yourself to the world! "}),
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'first_name': "First Name",
            'last_name': "Last Name",
            'bio': "Bio",
            'birth_date': "Birth Date",
            'gender': "Gender",
            'picture': "Profile Picture",
        }


class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(
        label=("Old Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

    new_password1 = forms.CharField(
        label=("New Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("Repeat New"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


class ReportProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileReport
        fields = ['text']


