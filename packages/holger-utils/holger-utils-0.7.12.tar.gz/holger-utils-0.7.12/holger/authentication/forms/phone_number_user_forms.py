from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm, UsernameField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from ..models import PhoneNumberUser


class PhoneUserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required fields, plus a repeated password.
    """

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = PhoneNumberUser
        fields = ('first_name', 'last_name', 'cellphone')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user: PhoneNumberUser = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user


class PhoneUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"../password/\">this form</a>.")
    )

    class Meta:
        model = PhoneNumberUser
        fields = ('first_name', 'last_name',
                  'cellphone', 'password',
                  'email',
                  'is_superuser', 'is_staff', 'is_verify', 'is_active',
                  'user_permissions', 'groups',
                  'date_verify'
                  )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class PhoneUserLoginForm(AuthenticationForm):
    user_attr = {
        'autofocus': True,
        'class': ''
    }
    pass_attr = {
        'class': ''
    }
    username = UsernameField(widget=PhoneNumberPrefixWidget(attrs=user_attr))
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs=pass_attr),
    )
