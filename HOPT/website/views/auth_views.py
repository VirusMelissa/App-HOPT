# auth_views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from website.forms import LoginForm
from website.models import Accounts
from django.contrib import messages

def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Sử dụng phương thức authenticate() để xác thực người dùng
        user = authenticate(request, username=username, password=password)

        error_message = None
        if user is not None:
            # Đăng nhập người dùng và lưu thông tin trong request.user
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Tên người dùng hoặc mật khẩu không chính xác.'

        return render(request, 'Login.html', {
            'form': LoginForm(),
            'error_message': error_message
        })
    else:
        return render(request, 'Login.html', {'form': LoginForm()})

def LogoutView(request):
    # Sử dụng phương thức logout() để đăng xuất người dùng
    logout(request)
    return redirect('index')

def unauthorized_access(request):
    messages.error(request, "Bạn không có quyền truy cập vào trang này.")
    return redirect('index')  # Quay lại trang chủ
