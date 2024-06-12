from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
import random
import string
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db import models
from datetime import date

def generate_random_username(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="", widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'Username'
            self.fields['username'].label = ''
            self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['password1'].label = ''
            self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
            self.fields['password2'].label = ''
            self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'role', 'start_date', 'address')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Tùy chỉnh các thuộc tính của trường 'username'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        
    
class EmployeeSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="",required=False,widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'role', 'start_date', 'address', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(EmployeeSignUpForm, self).__init__(*args, **kwargs)

        self.role = kwargs.pop('role', None)  # Lấy giá trị role từ kwargs

        if self.role:
            self.fields['role'].initial = self.role
            
        self.fields['username'] = forms.CharField(initial=generate_random_username())
        self.fields['username'].widget.attrs['class'] = 'form-control'

        self.fields['password1'] = forms.CharField(initial='employee123')
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = 'Password'

        self.fields['password2'] = forms.CharField(initial='employee123')
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = 'Confirm Password'

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        start_date = cleaned_data.get('start_date')

        # Kiểm tra ngày sinh phải lớn hơn 18 tuổi
        if date_of_birth:
            age_limit = timezone.now().date() - timezone.timedelta(days=365 * 18)
            if date_of_birth > age_limit:
                self.add_error('date_of_birth', 'Bạn phải đủ 18 tuổi trở lên để đăng ký.')
        
        # Kiểm tra ngày vào làm phải sau ngày sinh
        if date_of_birth and start_date:
            if start_date <= date_of_birth:
                self.add_error('start_date', 'Ngày vào làm phải sau ngày sinh.')

        return cleaned_data
    

class FormThemBN(forms.ModelForm):
    hoten = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Họ tên", "class": "form-control"}), label="")
    gioitinh = forms.ChoiceField(required=True, choices=[('M', 'Male'), ('F', 'Female')], widget=forms.Select(attrs={"class": "form-control"}), label="")
    namsinh = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder": "Năm sinh", "class": "form-control"}), label="")
    diachi = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Địa chỉ", "class": "form-control"}), label="")
    ngaykham = forms.DateField(required=True, widget=forms.DateInput(attrs={"type": "date", "class": "form-control","readonly": "readonly"}), label="")

    class Meta:
        model = Benhnhan
        exclude = ("patient",)


class FormPhieuKB(forms.Form):
    hoten = forms.CharField(disabled=True, required=True, widget=forms.TextInput(attrs={"placeholder": "Họ tên", "class": "form-control"}), label="")
    ngaykham = forms.DateField(disabled=True, required=True, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}), label="")
    trieuchung = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Triệu chứng", "class": "form-control"}), label="Symptoms")
    dudoan = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Dự đoán", "class": "form-control"}), label="Predictions")


class FormthemThuocPKB(forms.Form):
    
    tenThuoc = forms.ChoiceField(required=True, widget=forms.Select(attrs={"class": "form-control"}), label="")
    donvi = forms.ChoiceField(required=True, choices=[('vien', 'viên'), ('chai', 'chai')], widget=forms.Select(attrs={"class": "form-control"}), label="")
    soluong = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder":"Số lượng","class":"form-control"}), label="")
    cachdung = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Cách dùng", "class": "form-control"}), label="")
    
    def clean(self):
        cleaned_data = super().clean()
        tenThuoc = cleaned_data.get('tenThuoc')
        soluong = cleaned_data.get('soluong')
        donvi = cleaned_data.get('donvi')
        if tenThuoc and soluong:
            thuoc = Thuoc.objects.get(tenThuoc=tenThuoc)
            if donvi == 'vien':
                if soluong > thuoc.soviencon:
                    self.add_error('soluong', f'Số viên thuốc chỉ còn lại {thuoc.soviencon} viên')
                else:
                    thuoc.soviencon = thuoc.soviencon - soluong
            else:
                if soluong > thuoc.sochaicon:
                    self.add_error('soluong', f'Số chai thuốc chỉ còn lại {thuoc.sochaicon} chai')
                else:
                    thuoc.sochaicon = thuoc.sochaicon - soluong
            thuoc.save()


                    
class FormthemLoaiThuoc(forms.Form):
    tenThuoc = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Tên thuốc", "class": "form-control"}), label="")
    giatheovien = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder":"Giá theo viên","class":"form-control"}), label="")
    giatheochai = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder":"Giá theo chai","class":"form-control"}), label="")



        
class AddBill(forms.Form):
    tienkham = forms.IntegerField(disabled=True,required=True, widget=forms.TextInput(attrs={"placeholder":"cure cost","class":"form-control"}), label="")
    tienthuoc = forms.IntegerField(disabled=True,required=False, widget=forms.TextInput(attrs={"placeholder":"medicine cost","class":"form-control"}), label="")


        
class thietbiForm(forms.ModelForm):
    class Meta:
        model = thietbiYte
        fields = ['name', 'supplier', 'quantity', 'import_date', 'price', 'purpose']
        widgets = {
            'import_date': forms.DateInput(attrs={'type': 'date'}),
        }
class ReportForm(forms.Form):
    month = forms.ChoiceField(choices=[(i, i) for i in range(1, 13)], label='Tháng')
    year = forms.ChoiceField(choices=[(i, i) for i in range(2020, 2031)], label='Năm')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())