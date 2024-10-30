from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
import random
import string
from website.models import Accounts  # Import mô hình Accounts

# Khôi phục mật khẩu
def PasswordResetView(request):
    error_message = None  # Khởi tạo biến error_message

    if request.method == 'POST':
        username = request.POST.get('username')
        
        # Kiểm tra username có tồn tại không
        try:
            user = Accounts.objects.get(username=username)
            request.session['username'] = username  # Lưu username vào session
            return redirect('send_verification')  # Chuyển hướng đến trang gửi mã xác nhận
        except Accounts.DoesNotExist:
            error_message = 'Tên người dùng không tồn tại.'

    return render(request, 'ThayDoi_Password/password_reset.html', {'error_message': error_message})


def SendVerificationView(request):
    if request.method == 'POST':
        username = request.session.get('username')
        method = request.POST.get('method')

        # Tạo mã xác nhận ngẫu nhiên
        verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        request.session['verification_code'] = verification_code
        request.session['code_sent_time1'] = timezone.now().timestamp()  # Lưu timestamp
        request.session['code_sent_time2'] = timezone.now().isoformat()

        # Lấy thông tin người dùng
        try:
            user = Accounts.objects.get(username=username)
            email = user.email
            phone_number = user.phone_number
        except Accounts.DoesNotExist:
            return redirect('password_reset')  # Nếu không tìm thấy người dùng, quay lại trang reset

        # Gửi mã xác nhận theo phương thức đã chọn
        if method == 'email':
            send_mail(
                'Mã xác nhận khôi phục mật khẩu',
                f'Mã xác nhận của bạn là: {verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        elif method == 'phone':
            # Code gửi SMS (nếu có)
            pass
        elif method == 'zalo':
            # Code gửi Zalo (nếu có)
            pass

        return redirect('verify_code')

    return render(request, 'ThayDoi_Password/send_verification.html')


def VerifyCodeView(request):
    error_message = None  # Khởi tạo biến error_message

    if request.method == 'POST':
        user_code = request.POST.get('code')
        verification_code = request.session.get('verification_code')
        sent_time_timestamp = request.session.get('code_sent_time1')  # Lấy timestamp

        # Kiểm tra nếu sent_time không tồn tại hoặc mã xác nhận không khớp
        if sent_time_timestamp is None:
            error_message = 'Mã xác nhận đã hết hạn hoặc không còn tồn tại'
        elif user_code == verification_code:
            # Chuyển đổi timestamp thành datetime
            sent_time = timezone.datetime.fromtimestamp(sent_time_timestamp, timezone.get_current_timezone())

            # So sánh thời gian để kiểm tra xem mã xác nhận có hợp lệ không
            if timezone.now() <= sent_time + timezone.timedelta(minutes=2):
                # Mã xác nhận hợp lệ
                # Xóa mã xác nhận và thời gian khỏi session để nó không còn hiệu lực
                del request.session['code_sent_time1']

                return redirect('reset_password')  # Chuyển đến trang đổi mật khẩu
            else:
                error_message = 'Mã xác nhận đã hết hạn'
        else:
            error_message = 'Mã xác nhận không chính xác'

    return render(request, 'ThayDoi_Password/verify_code.html', {'error_message': error_message})



def ResetPasswordView(request):
    error_message = None  # Khởi tạo biến error_message

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        username = request.session.get('username')

        if password == confirm_password:
            # Mã hóa và cập nhật mật khẩu
            hashed_password = make_password(password)

            try:
                user = Accounts.objects.get(username=username)
                user.password = hashed_password
                user.save()  # Lưu thay đổi mật khẩu

                # Xóa thông tin khỏi session
                del request.session['username']
                del request.session['verification_code']

                return redirect('login')  # Chuyển hướng về trang đăng nhập
            except Accounts.DoesNotExist:
                error_message = 'Tên người dùng không tồn tại. Vui lòng thử lại.'

        else:
            error_message = 'Mật khẩu không khớp. Vui lòng thử lại.'

    return render(request, 'ThayDoi_Password/reset_password.html', {'error_message': error_message})
