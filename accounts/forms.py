from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:     #RegistraitonForm un özelliklerini yazarız
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
        def save(self, commit=True):

            user = super(RegistrationForm, self)
            user.first_name = self.cleaned_data('first_name')
            user.last_name = self.cleaned_data('last_name')
            user.email = self.cleaned_data('email')

            if commit==True:
                user.save()

            return user
class EditProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields=(    #exclude formdan çıkarmak için, biz hepsini çıkarmak yernine gerekli olanı ekliyoruz
            "email",
            "first_name",
            "last_name",
            "password",
        )


