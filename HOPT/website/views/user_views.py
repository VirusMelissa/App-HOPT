from django.shortcuts import render, redirect
from website.forms import CustomUserCreationForm
from website.models import Accounts
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required(login_url='login')
def UserManagement(request):
    if request.user.role == 'admin':
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort', 'role')
        sort_order = request.GET.get('order', 'asc')

        # Đảm bảo sort_order luôn là 'asc' hoặc 'desc'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'

        # Sắp xếp
        order_by = sort_by if sort_order == 'asc' else f'-{sort_by}'

        # Lấy danh sách người dùng với điều kiện tìm kiếm
        users_list = Accounts.objects.all()

        if search_query:
            users_list = users_list.filter(
                Q(username__icontains=search_query) | 
                Q(fullname__icontains=search_query) | 
                Q(email__icontains=search_query) | 
                Q(phone_number__icontains=search_query) | 
                Q(role__icontains=search_query)
            )

        users_list = users_list.order_by(order_by)  # Sắp xếp danh sách người dùng

        paginator = Paginator(users_list, 10)  # Phân trang 10 người dùng mỗi trang
        page_number = request.GET.get('page')
        users = paginator.get_page(page_number)

        return render(request, 'QuanLy_User/User_management.html', {
            'users': users,
            'sort_by': sort_by,
            'sort_order': sort_order
        })
    else:
        raise PermissionDenied


# Tạo người dùng
login_required(login_url='login')
def CreateUserView(request):
    if request.user.role == 'admin':
        username_error = None  # Thêm biến để lưu lỗi tên người dùng
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                # Lấy dữ liệu từ form đã được kiểm tra hợp lệ
                username = form.cleaned_data['username']
                raw_password = form.cleaned_data['password1']  # Mật khẩu đã được kiểm tra
                hashed_password = make_password(raw_password)  # Mã hóa mật khẩu
                fullname = form.cleaned_data['fullname']
                phone = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                role = form.cleaned_data['role']
                
                # Kiểm tra xem username đã tồn tại chưa
                if Accounts.objects.filter(username=username).exists():
                    username_error = "Tên người dùng đã tồn tại."
                    return render(request, 'QuanLy_User/Create_user.html', {'form': form, 'username_error': username_error})

                # Tạo người dùng mới
                Accounts.objects.create(
                    username=username,
                    password=hashed_password,
                    fullname=fullname,
                    email=email,
                    phone_number=phone,
                    role=role
                )

                return redirect('user_management')  # Chuyển hướng sau khi tạo thành công
            else:
                print(form.errors)  # In ra lỗi để kiểm tra nếu form không hợp lệ
        else:
            form = CustomUserCreationForm()

        return render(request, 'QuanLy_User/Create_user.html', {'form': form})
    else:
        raise PermissionDenied

# Sửa người dùng
@login_required(login_url='login')
def EditUserView(request, user_id):
    if request.user.role == 'admin':
        try:
            user = Accounts.objects.get(id=user_id)
        except Accounts.DoesNotExist:
            raise Http404("Người dùng không tồn tại")

        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save(commit=False)
                raw_password = form.cleaned_data.get('password1')

                if raw_password:
                    hashed_password = make_password(raw_password)
                    user.password = hashed_password

                user.save()  # Lưu thay đổi

                # Nếu người dùng hiện tại chính là người vừa được chỉnh sửa, cập nhật session
                if request.user.id == user.id:
                    request.session['role'] = user.role

                return redirect('user_management')
        else:
            form = CustomUserCreationForm(instance=user)

        return render(request, 'QuanLy_User/Edit_user.html', {'form': form})
    else:
        raise PermissionDenied

# Xóa người dùng
@login_required(login_url='login')
def DeleteUserView(request, user_id):
    if request.user.role == 'admin':
        try:
            user = Accounts.objects.get(id=user_id)
            user.delete()  # Xóa người dùng
        except Accounts.DoesNotExist:
            raise Http404("Người dùng không tồn tại")
        
        return redirect('user_management')
    else:
        raise PermissionDenied

