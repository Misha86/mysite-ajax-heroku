from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
import os


class CalendarWidget(forms.DateInput):
    class Media:
        css = {'all': ('css/jquery-ui.css',)}
        js = ('js/jquery-ui.js', 'js/loginsys.js', 'js/datepicker-uk.js', 'js/datepicker-ru.js')


class ProfileCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    from django.forms.utils import ErrorList

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):

        if label_suffix is None:
            label_suffix = ' <->'
        super(ProfileCreationForm, self).__init__(data, files, auto_id, prefix, initial,
                                                  error_class, label_suffix, empty_permitted, instance)

    # date_of_birth = forms.CharField(label=_("Дата народження"), required=False,
    #                                 widget=forms.DateInput(attrs={'class': 'form-control',
    #                                                               'placeholder': _('дата народження')}))
    date_of_birth = forms.CharField(label=_("Дата народження"), required=False,
                                    widget=CalendarWidget(format='%Y-%m-%d',
                                                          attrs={'class': 'form-control',
                                                                 'placeholder': _('дата народження'),
                                                                 'autocomplete': 'off'}))

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': _('введіть пароль'),
                                                                  'autocomplete': 'off'},
                                                           render_value=True))
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': _('повторіть пароль'),
                                                                  'autocomplete': 'off'}))
    # sex = forms.CharField(label=_("Стать"), max_length=20,
    #                       widget=forms.Select(choices=(('Man', _('Чоловік')), ('Woman', _('Жінка'))),
    #                                           attrs={'class': 'form-control', 'id': 'select'}))
    sex = forms.ChoiceField(label=_("Стать"), choices=(('Man', _('Чоловік')), ('Woman', _('Жінка'))),
                            widget=forms.RadioSelect(attrs={'id': 'select'}))
    avatar = forms.ImageField(label=_("Аватарка"), widget=forms.ClearableFileInput(attrs={'class': "btn btn-default"}),
                              required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'rows': 4,
                                                      'placeholder': _('логін')}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control', 'rows': 4,
                                                        'placeholder': _("ім'я")}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'rows': 4,
                                                       'placeholder': _("прізвище")}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'rows': 4, 'id': 'email',
                                                    'placeholder': _("e-mail")},)}

        labels = {'username': _("Логін"),
                  'first_name': _("Ім'я"),
                  'last_name': _("Прізвище"),
                  'email': _("E-mail")}

        error_messages = {
            'username': {
                'required': _('Будь-ласка, введіть логін')},
            'email': {
                'required': _('Будь-ласка, введіть E-mail')}
        }

        help_texts = {'username': None}

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        valid_password = validate_password(password1)
        if valid_password is not None:
            raise valid_password.ValidationError()
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("Паролі не співпадають!"),
                code='password_mismatch',
                )
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username", None)
        exists_user = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()
        if username is not None and exists_user:
            user = User.objects.get(username=username)
            if email == user.email:
                return email
        if not email:
            raise forms.ValidationError(_("Це поле обов'язкове."), code='require')
        elif email_exists:
            raise forms.ValidationError(_("Такий email вже зареєстрований."), code='email_exists')
        else:
            return email

    def save(self, commit=True):
        user = super(ProfileCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileUpdateForm(ProfileCreationForm):
    password = forms.CharField(label=_("Old password"),
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': _('введіть старий пароль'),
                                                                 'autocomplete': 'off'}))
    username = forms.CharField(label=_("Логін"), disabled=True, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'rows': 4,
               'placeholder': _('логін')}))

    class Meta(ProfileCreationForm.Meta):
        model = User
        # ProfileCreationForm.Meta.fields.insert(4, 'password')
        # fields = ProfileCreationForm.Meta.fields
        fields = ProfileCreationForm.Meta.fields + ['password']

    def clean_password(self):
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username")
        user = User.objects.get(username=username)
        if user is not None and user.check_password(password):
            return password
        elif password is not None:
            raise forms.ValidationError(_("Старий пароль не вірний!"))
