from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Accounts

# Form đăng nhập người dùng
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Tên người dùng')
    password = forms.CharField(widget=forms.PasswordInput(), label='Mật khẩu')
  
# Ràng buộc mật khẩu: yêu cầu có ký tự viết hoa, chữ thường và số
def validate_password_strength(value):
    if not any(char.isdigit() for char in value):
        raise ValidationError("Mật khẩu phải chứa ít nhất một chữ số")
    if not any(char.islower() for char in value):
        raise ValidationError("Mật khẩu phải chứa ít nhất một chữ thường")
    if not any(char.isupper() for char in value):
        raise ValidationError("Mật khẩu phải chứa ít nhất một chữ hoa")

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(),
        validators=[validate_password_strength],
        required=False
    )
    password2 = forms.CharField(
        label="Nhập lại mật khẩu",
        widget=forms.PasswordInput(),
        required=False
    )

    class Meta:
        model = Accounts
        fields = ['username', 'fullname', 'email', 'phone_number', 'role']

    # Kiểm tra username chỉ cho phép ký tự chữ và số
    username = forms.CharField(
        label="Tên người dùng",
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9]*$',
                message="Tên người dùng chỉ được chứa chữ cái và số",
                code='invalid_username'
            )
        ],
        required=False
    )

    # Kiểm tra username chỉ cho phép ký tự chữ và số
    fullname = forms.CharField(
        label="Họ và tên",
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z1-9ÁÀẢÃẠÂÂẤẦẨẪẬĂẮẰẲẴẶĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌƠỚỜỞỠỢÔỐỒỔỖỘÙÚỦŨỤƯỨỪỬỮỰÝỲỶỸỴáàảãạââấầẩẫậăắằẳẵặđèéẻẽẹêếềểễệìíỉĩịòóỏõọơớờởỡợôốồổỗộùúủũụưứừửữựýỳỷỹỵ\s]+$',  # Cho phép ký tự chữ cái có dấu và khoảng trắng
                message="Họ và tên chỉ có chữ cái",
                code='invalid_fullname'
            )
        ],
        required=False
    )

    # Kiểm tra số điện thoại
    phone_number = forms.CharField(
        label="Số điện thoại",
        max_length=15,
        required=False
    )

    # Kiểm tra email hợp lệ
    email = forms.EmailField(
        label="Email",
        max_length=254,
        error_messages={
            'invalid': "Địa chỉ email không hợp lệ"
        },
        required=False
    )

    # Kiểm tra mật khẩu khớp nhau
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if not password1:  
            raise forms.ValidationError("Mật khẩu không được để trống")
        return password1

    # Kiểm tra mật khẩu khớp nhau
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password2:  
            raise forms.ValidationError("Nhập lại mật khẩu không được để trống")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu không khớp nhau")
        return password2

    # Kiểm tra các trường không được để trống
# Kiểm tra các trường không được để trống
    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")

        # Kiểm tra số điện thoại
        if not phone_number:
            self.add_error('phone_number', "Số điện thoại không được để trống")
        elif len(phone_number) < 10:
            self.add_error('phone_number', "Số điện thoại phải có ít nhất 10 chữ số")

        # Chỉ kiểm tra các trường không phải là mật khẩu
        for field in self.Meta.fields:
            if field != 'phone_number' and not cleaned_data.get(field):
                self.add_error(field, f"{self.fields[field].label} không được để trống")

    # Ghi đè phương thức save để mã hóa mật khẩu
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Mã hóa mật khẩu trước khi lưu
        if commit:
            user.save()
        return user

