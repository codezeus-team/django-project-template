from django import forms

from .models import Account


class ProfileForm(forms.Form):
    """User Profile Form"""
    email = forms.EmailField()
    username = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=40, required=False)
    last_name = forms.CharField(max_length=40, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self._build_initial()
        super(ProfileForm, self).__init__(*args, **kwargs)

    def _build_initial(self):
        for field in self.base_fields:
            self.base_fields[field].initial = getattr(self.user, field)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username != str(self.user.username) and Account.objects.filter(username=username).exists():
            raise forms.ValidationError('That username already exists.')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email != self.user.email and Account.objects.get(email=email):
            raise forms.ValidationError('That email already exists.')

        return email

    def save(self):
        for field, value in self.cleaned_data.iteritems():
            setattr(self.user, field, value)

        self.user.save()
        return self.user


class AvatarForm(forms.ModelForm):
    """Avatar Form"""
    class Meta:
        model = Account
        fields = ('avatar',)

    def __init__(self, *args, **kwargs):
        """Intialize Form"""
        self.user = kwargs.pop('user')

        # Get Avatar Upload
        if args[1] is not None:
            self.avatar = args[1]['avatar']

        super(AvatarForm, self).__init__(*args, **kwargs)

    def save(self, commit=False):
        super(AvatarForm, self).save(commit)

        self.user.avatar = self.avatar
        self.user.save()

        return self.user


class RegistrationForm(forms.Form):
    """Custom Registration form"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('Your email already is in use')
        return email

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Your passwords do not match')

    def save(self):
        user = Account.objects.create_user(
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )
        return user
