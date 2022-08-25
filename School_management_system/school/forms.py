from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from .validators import username_validation
from .config import GENDER_CHOICE, MODE_OF_STAY_CHOICE


class SelectDate(forms.DateInput):
    input_type = "date"


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        validators=[username_validation, MinLengthValidator(5), MaxLengthValidator(15)],
        help_text="Username should be Alphanumeric of length 5 to 15",
    )
    email = forms.EmailField()
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"id": "view-pwd"}),
    )
    password2 = forms.CharField(
        label=_("Re-enter password"),
        widget=forms.PasswordInput(attrs={"id": "view-pwd1"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class MyLoginAuthForm(AuthenticationForm):
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "id": "view-pwd"}
        ),
    )

    error_messages = {
        "invalid_login": _("Please enter a correct Username & Password"),
        "inactive": _(
            "This account is inactive. Activation link is sent to your email."
        ),
    }


class NewStudentForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 30}))
    dob = forms.DateField(widget=SelectDate())
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    father_name = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 30}))
    mother_name = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 30}))
    sibilings = forms.IntegerField()
    address = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 100}))
    parent_mobile = forms.IntegerField(
        widget=forms.TextInput(
            attrs={"type": "number", "min": "1000000000", "max": "9999999999"}
        )
    )
    date_of_joining = forms.DateField(widget=SelectDate())
    mode_of_stay = forms.ChoiceField(choices=MODE_OF_STAY_CHOICE)
    fees = forms.IntegerField()
    class_teacher_id = forms.IntegerField(required=False)


class EditStudentForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 30}))
    dob = forms.DateField(widget=SelectDate())
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    father_name = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 30}))
    mother_name = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 30}))
    sibilings = forms.IntegerField()
    address = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 100}))
    parent_mobile = forms.IntegerField(
        widget=forms.TextInput(
            attrs={"type": "number", "min": "1000000000", "max": "9999999999"}
        )
    )
    date_of_joining = forms.DateField(widget=SelectDate())
    mode_of_stay = forms.ChoiceField(choices=MODE_OF_STAY_CHOICE)
    fees = forms.IntegerField()
    class_teacher_id = forms.IntegerField(required=False)


class NewTeacherForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 30}))
    dob = forms.DateField(widget=SelectDate())
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    phone_number = forms.IntegerField(
        widget=forms.TextInput(
            attrs={"type": "number", "min": "1000000000", "max": "9999999999"}
        )
    )
    email = forms.EmailField()
    address = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 100}))
    date_of_joining = forms.DateField(widget=SelectDate())
    salary = forms.IntegerField()
    subject = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 10}))
    previous_organization = forms.CharField(
        widget=forms.TextInput(attrs={"maxlength": 30})
    )


class EditTeacherForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 30}))
    dob = forms.DateField(widget=SelectDate())
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    phone_number = forms.IntegerField(
        widget=forms.TextInput(
            attrs={"type": "number", "min": "1000000000", "max": "9999999999"}
        )
    )
    email = forms.EmailField()
    address = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 100}))
    date_of_joining = forms.DateField(widget=SelectDate())
    salary = forms.IntegerField()
    subject = forms.CharField(widget=forms.TextInput(attrs={"maxlength": 10}))
    previous_organization = forms.CharField(
        widget=forms.TextInput(attrs={"maxlength": 30})
    )
