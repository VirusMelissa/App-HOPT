from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Tạo lớp quản lý người dùng tùy chỉnh
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Người dùng phải có tên đăng nhập.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Mã hóa mật khẩu
        user.save(using=self._db)
        return user

    def create_admin(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return self.create_user(username, password, **extra_fields)

# Mô hình người dùng tùy chỉnh
class Accounts(AbstractBaseUser):
    ROLE_CHOICES = [
        ('admin', 'Quản trị viên'),
        ('warehouse_staff', 'Kho'),
        ('sales_staff', 'Sale'),
        ('technician', 'Kỹ thuật'),
        ('finance_staff', 'Nghiệp vụ'),
        ('team_R&D', 'R&D'),
        ('CEO', 'Giám Đốc'),
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='sales_staff')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
# Mô hình tin nhắn chat
class ChatMessage(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    department = models.CharField(max_length=50)  # Thêm trường để xác định phòng ban

    def __str__(self):
        return f"{self.user.username} ({self.department}): {self.message[:50]}"

# Mô hình trạng thái đã đọc tin nhắn
class MessageReadStatus(models.Model):
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('message', 'user')  # Đảm bảo mỗi người dùng chỉ có một trạng thái cho mỗi tin nhắn


# Mô hình Loại Hàng
class Product_Type(models.Model):
    id = models.AutoField(primary_key=True)
    product_type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.product_type


# Mô hình Sản Phẩm
class Products(models.Model):
    id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=50, unique=True)
    product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE)
    net_weight = models.FloatField()
    net_price = models.FloatField()
    sales_unit = models.CharField(max_length=255)
    product_description = models.TextField()

    def __str__(self):
        return self.product_code


# Mô hình Nhà Cung Cấp
class Suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.supplier_name


# Mô hình Bill
class Bills(models.Model):
    id = models.AutoField(primary_key=True)
    bill_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.bill_code


# Mô hình Hợp Đồng
class Contracts(models.Model):
    id = models.AutoField(primary_key=True)
    contract_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.contract_number


# Mô hình Phiếu Nhập Kho
class Warehouse_Receipts(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse_receipt_number = models.CharField(max_length=50, unique=True)
    receipt_date = models.DateField()
    other_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.warehouse_receipt_number


# Mô hình Nhập Kho
class Warehouse_Entries(models.Model):
    id = models.AutoField(primary_key=True)
    stt = models.IntegerField(null=True, blank=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    entry_date = models.DateField()
    quantity = models.IntegerField(blank=True)
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    warehouse_receipts = models.ForeignKey(Warehouse_Receipts, on_delete=models.CASCADE)
    bills = models.ForeignKey(Bills, on_delete=models.CASCADE)
    contracts = models.ForeignKey(Contracts, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.products} - {self.entry_date}'
