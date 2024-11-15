from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Account


#ログイン機能

class AccountForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    class Meta():
        model = User
        
        fields = ('username','password')
        labels = {'username':"ユーザーID"}
        

class AddAccountForm(forms.ModelForm):
    
    class Meta():
    
        model = Account
        
        fields = ('account_image',)
        labels = {'account_image':"写真アップロード",}


# 検索機能
class SearchForm(forms.Form):
        keyword = forms.CharField(label='', max_length=50)











# class UserCreateForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         #htmlの表示を変更可能にする
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['password1'].widget.attrs['class'] = 'form-control'
#         self.fields['password2'].widget.attrs['class'] = 'form-control'


#     class Meta:
#         model = User
#         fields = ("username", "password1", "password2")
        


# class LoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         #htmlの表示を変更可能にする
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['password'].widget.attrs['class'] = 'form-control'