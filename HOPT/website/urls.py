from django.urls import path
from .views.home_views import Home
from .views.auth_views import LoginView, LogoutView, unauthorized_access
from .views.message_views import get_chat_messages, send_message, get_unread_count, mark_messages_as_read
from .views.user_views import UserManagement, CreateUserView, EditUserView, DeleteUserView
from .views.password_views import PasswordResetView, SendVerificationView, VerifyCodeView, ResetPasswordView
from .views.QuanLy_Kho.Goods_Receipt_views import Goods_Receipt_View, Add_Goods_Receipt_View, Edit_Goods_Receipt_View, Delete_Goods_Receipt_View
from .views.QuanLy_Kho.Goods_Issue_views import Goods_Issue_View, Add_Goods_Issue_View, Edit_Goods_Issue_View, Delete_Goods_Issue_View
from .views.QuanLy_Kho.Inventory_views import Inventory_View, Add_Inventory_View, Edit_Inventory_View

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
    path('warehouse-receipt/', Goods_Receipt_View, name='goods_receipt'),
    path('warehouse-receipt/add-product/', Add_Goods_Receipt_View, name='add_goods_receipt'),
    path('warehouse-receipt/edit/<int:entry_id>/', Edit_Goods_Receipt_View, name='edit_goods_receipt'),
    path('warehouse-receipt/delete/<int:entry_id>/', Delete_Goods_Receipt_View, name='delete_goods_receipt'),
    path('warehouse-issue/', Goods_Issue_View, name='goods_issue'),
    path('warehouse-issue/add-product/', Add_Goods_Issue_View, name='add_goods_issue'),
    path('warehouse-issue/edit/<int:issue_id>/', Edit_Goods_Issue_View, name='edit_goods_issue'),
    path('warehouse-issue/delete/<int:issue_id>/', Delete_Goods_Issue_View, name='delete_goods_issue'),
    path('warehouse-inventory/', Inventory_View, name='inventory'),
    path('warehouse-inventory/update/', Add_Inventory_View, name='add_inventory'),
    path('warehouse-inventory/edit/<int:inventory_id>/', Edit_Inventory_View, name='edit_inventory'),
]
