from django.urls import path
from .views.home_views import Home
from .views.auth_views import LoginView, LogoutView, unauthorized_access
from .views.message_views import get_chat_messages, send_message, get_unread_count, mark_messages_as_read
from .views.user_views import UserManagement, CreateUserView, EditUserView, DeleteUserView
from .views.password_views import PasswordResetView, SendVerificationView, VerifyCodeView, ResetPasswordView
from .views.QuanLy_Kho.warehouse_entry_views import Warehouse_View, Add_Product_Warehouse_View, Edit_Warehouse_Entry_View, Delete_Warehouse_Entry_View

urlpatterns = [
    path('', Home, name='index'),

    # Xác thực tài khoản
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('unauthorized-access/', unauthorized_access, name='unauthorized_access'),

    # Chat box
    path('get-chat-messages/<str:department>/', get_chat_messages, name='get_chat_messages'),
    path('send-message/<str:department>/', send_message, name='send_message'),
    path('get-unread-count/<str:department>/', get_unread_count, name='get_unread_count'),
    path('mark-messages-as-read/<str:department>/', mark_messages_as_read, name='mark_messages_as_read'),

    # Quên mật khẩu
    path('password-reset/', PasswordResetView, name='password_reset'),
    path('send-verification/', SendVerificationView, name='send_verification'),
    path('verify-code/', VerifyCodeView, name='verify_code'),
    path('reset-password/', ResetPasswordView, name='reset_password'),

    # Quản lý người dùng
    path('user-management/', UserManagement, name='user_management'),
    path('create-user/', CreateUserView, name='create_user'),
    path('edit-user/<int:user_id>/', EditUserView, name='edit_user'),
    path('delete-user/<int:user_id>/', DeleteUserView, name='delete_user'),

    # Quản lý kho
    path('warehouse-entry/', Warehouse_View, name='warehouse_entry'),
    path('warehouse-entry/add-product/', Add_Product_Warehouse_View, name='add_warehouse_entry'),
    path('warehouse-entry/edit/<int:entry_id>/', Edit_Warehouse_Entry_View, name='edit_warehouse_entry'),
    path('warehouse-entry/delete/<int:entry_id>/', Delete_Warehouse_Entry_View, name='delete_warehouse_entry'),
]
