from django.shortcuts import render, redirect
from website.forms import CustomUserCreationForm
from website.models import Accounts
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http import HttpResponseRedirect

@login_required(login_url='login')
def UserManagement(request):
    if request.user.role == 'admin':
        search_query = request.GET.get('search', '')

        ROLE_MAPPING = {display: value for value, display in Accounts.ROLE_CHOICES}
        mapped_role = ROLE_MAPPING.get(search_query, search_query)  # Lấy giá trị ánh xạ hoặc giữ nguyên

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
                Q(role__icontains=mapped_role)
            )

        users_list = users_list.order_by(order_by)  # Sắp xếp danh sách người dùng

        paginator = Paginator(users_list, 10)  # Phân trang 10 người dùng mỗi trang
        page_number = request.GET.get('page')
        users = paginator.get_page(page_number)

        columns = [
            {'name': 'Tên người dùng', 'field': 'username'},
            {'name': 'Họ và tên', 'field': 'fullname'},
            {'name': 'Email', 'field': 'email'},
            {'name': 'Số điện thoại', 'field': 'phone_number'},
            {'name': 'Vai trò', 'field': 'role'},
        ]

        hidden_fields = [
            {'name': 'page', 'value': users.number},
            {'name': 'sort', 'value': sort_by},
            {'name': 'order', 'value': sort_order}
        ]

        return render(request, 'QuanLy_User/User_management.html', {
            'users': users,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'search': search_query,
            'hidden_fields': hidden_fields,
            'columns': columns,
        })
    else:
        raise PermissionDenied


# Tạo người dùng
login_required(login_url='login')
def CreateUserView(request):
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    search = request.GET.get('search', '')

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

                url = reverse('user_management')  # Thay 'warehouse_entry' bằng tên URL của bạn nếu khác
                return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&search={search}")
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
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    search = request.GET.get('search', '')

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

                url = reverse('user_management')  # Thay 'warehouse_entry' bằng tên URL của bạn nếu khác
                return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&search={search}")
        else:
            form = CustomUserCreationForm(instance=user)

        return render(request, 'QuanLy_User/Edit_user.html', {'form': form})
    else:
        raise PermissionDenied

# Xóa người dùng
@login_required(login_url='login')
def DeleteUserView(request, user_id):
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    search = request.GET.get('search', '')

    if request.user.role == 'admin':
        try:
            user = Accounts.objects.get(id=user_id)
            user.delete()  # Xóa người dùng
        except Accounts.DoesNotExist:
            raise Http404("Người dùng không tồn tại")
        
        url = reverse('user_management')  # Thay 'warehouse_entry' bằng tên URL của bạn nếu khác
        return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&search={search}")
    else:
        raise PermissionDenied

