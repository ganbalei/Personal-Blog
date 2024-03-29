from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

#登录表单
class LoginForm(forms.Form):

    username_or_email = forms.CharField(label='用户名或邮箱',  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username_or_email, password=password)

        #先判断是否用户名登录
        if user is None:
            #再判断是否是邮箱登录
            if User.objects.filter(email=username_or_email, password=password):
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            else:
                raise forms.ValidationError('用户名或者密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

#注册表单
class RegForm(forms.Form):

    username = forms.CharField(label='用户名', max_length=15, min_length=3, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入3-15位用户名'}))

    password = forms.CharField(label='密码', max_length=20, min_length=8, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入8-20位密码'}))

    password_again = forms.CharField(label='再输入一次密码', max_length=20, min_length=8, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入8-20位密码'}))

    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))

    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击“发送验证码”发送到邮箱'}
        )
    )

    #自定义初始化方法，传入user
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):

        #判断验证码是否正确
        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password:
            raise forms.ValidationError('两次输入密码不一致')
        return password_again

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    # 验证验证码是否为空
    def clean_verification_code(self):
        verification_code = self.cleaned_data['verification_code']
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

#修改昵称表单
class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label='新的昵称',
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control','placeholder': '请输入新的昵称'}
        )
    )

    #自定义初始化方法，传入user
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        #判断用户是否登陆
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('新的昵称不能为空')
        return nickname_new

#绑定邮箱表单
class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control','placeholder': '请输入正确的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击“发送验证码”发送到邮箱'}
        )
    )

    #自定义初始化方法，传入user
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        #判断用户是否登陆
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户未登录')

        #判断用户是否已经绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定了邮箱')

        #判断验证码是否正确
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已经被绑定')
        return email

    #验证验证码是否为空
    def clean_verification_code(self):
        verification_code = self.cleaned_data['verification_code']
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧的密码', max_length=20, min_length=8, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入8-20位密码'}))

    new_password = forms.CharField(label='新的密码', max_length=20, min_length=8, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入8-20位密码'}))

    new_password_again = forms.CharField(label='再输入一次新的密码', max_length=20, min_length=8, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入8-20位密码'}))

    # 自定义初始化方法，传入user
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        #验证新的密码是否一致
        new_password = self.cleaned_data['new_password']
        new_password_again = self.cleaned_data['new_password_again']
        if new_password=='' or new_password != new_password_again:
            raise forms.ValidationError('两次输入的密码不一致')


    def clean_old_password(self):
        #判断旧的密码是否正确
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')
        return old_password

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'}
        )
    )

    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击“发送验证码”发送到邮箱'}
        )
    )

    new_password = forms.CharField(label='新的密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}))

    #自定义初始化方法，传入user
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    # 验证验证码是否正确
    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '')
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        code = self.request.session.get('forgot_password_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data