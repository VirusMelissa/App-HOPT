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
    stt = models.IntegerField(null=True, blank=True)
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


#  Mô hình Loại hàng
class Product_Type(models.Model):
    stt = models.IntegerField(unique=True)
    product_type_code = models.CharField(primary_key=True, max_length=50)
    product_type_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.product_type_name

# Mô hình Hàng
class Products(models.Model):
    stt = models.IntegerField(unique=True)
    product_code = models.CharField(primary_key=True, max_length=50)
    product_name = models.CharField(max_length=255,)
    product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE)
    origin_country = models.CharField(max_length=255)
    net_weight = models.FloatField()
    net_price = models.FloatField()
    sales_unit = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product_code

# Mô hình Nhà Cung Cấp
class Suppliers(models.Model):
    stt = models.IntegerField(unique=True)
    supplier_code = models.CharField(primary_key=True, max_length=50)
    supplier_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.supplier_name


# Mô hình Bill
class Bills(models.Model):
    stt = models.IntegerField(unique=True)
    bill_code = models.CharField(primary_key=True, max_length=50)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.bill_code


# Mô hình Hợp Đồng
class Contracts(models.Model):
    stt = models.IntegerField(unique=True)
    contract_number = models.CharField(primary_key=True, max_length=50)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.contract_number

# Mô hình Invoice
class Invoice(models.Model):
    stt = models.IntegerField(unique=True)
    invoice_number = models.CharField(primary_key=True, max_length=50)
    note = models.TextField(null=True, blank=True)

# Mô hình Packing List
class Packing_List(models.Model):
    stt = models.IntegerField(unique=True)
    packing_list_number = models.CharField(primary_key=True, max_length=50)
    note = models.TextField(null=True, blank=True)

# Mô hình CO
class Certificate_Of_Origin(models.Model): # CO
    stt = models.IntegerField(unique=True)
    co_number = models.CharField(primary_key=True, max_length=50)
    note = models.TextField(null=True, blank=True)

# Mô hình CQ
class Certificate_Of_Quality(models.Model): #CQ
    stt = models.IntegerField(unique=True)
    cq_number = models.CharField(primary_key=True, max_length=50)
    note = models.TextField(null=True, blank=True)

# Mô hình TKHQ
class Customs_Declaration(models.Model): #TKHQ
    stt = models.IntegerField(unique=True)
    declaration_number = models.CharField(primary_key=True, max_length=50)
    note = models.TextField(null=True, blank=True)

# Mô hình chứng từ
class Documents(models.Model):
    id = models.AutoField(primary_key=True)
    stt = models.IntegerField(unique=True)
    hawb = models.ForeignKey(Bills, on_delete=models.CASCADE)
    contract_number = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    packing_list = models.ForeignKey(Packing_List, on_delete=models.CASCADE, null=True, blank=True)
    co = models.ForeignKey(Certificate_Of_Origin, on_delete=models.CASCADE, null=True, blank=True)
    cq = models.ForeignKey(Certificate_Of_Quality, on_delete=models.CASCADE, null=True, blank=True)
    customs_declaration = models.ForeignKey(Customs_Declaration, on_delete=models.CASCADE, null=True, blank=True)

class Warehouse(models.Model):
    stt = models.IntegerField(unique=True)
    warehouse_code = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

class Orders(models.Model):
    stt = models.IntegerField(unique=True)
    order_number = models.CharField(primary_key=True, max_length=50)
    order_date = models.DateField(null=True, blank=True) # Ngày lập đơn hàng
    total_value = models.FloatField(null=True, blank=True) # Tổng trị giá


# Mô hình Khách hàng
class Customers(models.Model):
    stt = models.IntegerField(unique=True)
    customer_code = models.CharField(primary_key=True, max_length=50)
    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    workplace = models.CharField(max_length=255) # Đơn vị làm việc

    def __str__(self):
        return self.customer_name

# Mô hình Chi tiết khách hàng
class Customer_Detail(models.Model):
    stt = models.IntegerField(unique=True)
    customer_code = models.ForeignKey(Customers, on_delete=models.CASCADE)
    customer_type = models.CharField(max_length=50)
    field = models.CharField(max_length=50) # lĩnh vực 
    operation_scale = models.CharField(max_length=50) # quy mô hoạt động
    sales_channel = models.CharField(max_length=50, blank=True, null=True) # kênh bán hàng

    def __str__(self):
        return f"{self.customer_code.customer_name} - {self.customer_type}"


# Mô hình nhân viên
class Employees(models.Model):
    stt = models.IntegerField(unique=True)
    employee_code = models.CharField(primary_key=True, max_length=50)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # địa chỉ
    citizen_identification = models.CharField(max_length=20) # Số căn cước
    status = models.CharField(max_length=20)  # tình trạng thử việc hoặc chính thức
    position = models.CharField(max_length=50) # chức vụ Giám đốc, Sale, ...

    def __str__(self):
        return self.full_name


# Mô hình chi tiết nhân viên
class Employee_Detail(models.Model):
    stt = models.IntegerField(unique=True)
    employee_code = models.ForeignKey(Employees, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    contract_number = models.CharField(max_length=50) # số hợp đồng
    contract_sign_date = models.DateField()
    contract_duration = models.CharField(max_length=100)  # in years
    basic_salary = models.FloatField() # lương cơ bản
    allowances = models.FloatField(blank=True, null=True) # phụ cấp 

    def __str__(self):
        return f"{self.employee_code.full_name}"


# Mô hình Nhập Kho
class Goods_Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    stt = models.IntegerField(unique=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    receipt_date = models.DateField()
    quantity = models.IntegerField(blank=True)
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    bills = models.ForeignKey(Bills, on_delete=models.CASCADE)
    contracts = models.ForeignKey(Contracts, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.products} - {self.receipt_date}'
    
# Mô hình Xuất kho
class Goods_Issue(models.Model):
    id = models.AutoField(primary_key=True)
    stt = models.IntegerField(unique=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    issue_date = models.DateField()
    quantity = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    customers = models.ForeignKey(Customers, on_delete=models.CASCADE)
    employees = models.ForeignKey(Employees, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.products} - {self.issue_date} - {self.customers}'
    
class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    years = models.IntegerField()
    stt = models.IntegerField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE)  # Liên kết đến bảng sản phẩm
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)  # Liên kết đến bảng kho
    previous_inventory = models.IntegerField()  # Tồn trước đó
    total_received = models.IntegerField()  # Tổng nhập
    total_issued = models.IntegerField()  # Tổng xuất
    current_inventory = models.IntegerField()  # Tồn hiện tại
    min_inventory = models.IntegerField()

    class Meta:
        db_table = 'inventory'

class Order_Details(models.Model):
    id = models.AutoField(primary_key=True)
    stt = models.IntegerField(unique=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateField() # Ngày đặt hàng
    unit_price = models.FloatField() # đơn giá
    contracts = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    order_confirmation = models.ForeignKey(Orders, on_delete=models.CASCADE) # số xác nhận đơn hàng
    customers = models.ForeignKey(Customers, on_delete=models.CASCADE)
    employees = models.ForeignKey(Employees, on_delete=models.CASCADE) # Người phụ trách đặt đơn hàng
    advance_date = models.DateField(null=True, blank=True) # ngày tạm ứng
    from_date = models.DateField(null=True, blank=True) 
    to_date = models.DateField(null=True, blank=True)
    order_status = models.CharField(max_length=50) # tình trạng đơn hàng 
    estimated_date_1 = models.DateField(null=True, blank=True)  # hàng báo ngày dự kiến lần 1
    estimated_date_2 = models.DateField(null=True, blank=True)
    inv_1 = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='inv_1', null=True, blank=True)
    pkl_1 = models.ForeignKey(Packing_List, on_delete=models.CASCADE, related_name='pkl_1', null=True, blank=True)
    quantity_batch_1 = models.IntegerField(null=True, blank=True)
    hawb_1 = models.ForeignKey(Bills, on_delete=models.CASCADE, related_name='hawb_1', null=True, blank=True)
    inv_2 = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='inv_2', null=True, blank=True)
    pkl_2 = models.ForeignKey(Packing_List, on_delete=models.CASCADE, related_name='pkl_2', null=True, blank=True)
    quantity_batch_2 = models.IntegerField(null=True, blank=True)
    hawb_2 = models.ForeignKey(Bills, on_delete=models.CASCADE, related_name='hawb_2', null=True, blank=True)
    inv_3 = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='inv_3', null=True, blank=True)
    pkl_3 = models.ForeignKey(Packing_List, on_delete=models.CASCADE, related_name='pkl_3', null=True, blank=True)
    quantity_batch_3 = models.IntegerField(null=True, blank=True)
    hawb_3 = models.ForeignKey(Bills, on_delete=models.CASCADE, related_name='hawb_3', null=True, blank=True)
    inv_4 = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='inv_4', null=True, blank=True)
    pkl_4 = models.ForeignKey(Packing_List, on_delete=models.CASCADE, related_name='pkl_4', null=True, blank=True)
    quantity_batch_4 = models.IntegerField(null=True, blank=True)
    hawb_4 = models.ForeignKey(Bills, on_delete=models.CASCADE, related_name='hawb_4', null=True, blank=True)
    inv_5 = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='inv_5', null=True, blank=True)
    pkl_5 = models.ForeignKey(Packing_List, on_delete=models.CASCADE, related_name='pkl_5', null=True, blank=True)
    quantity_batch_5 = models.IntegerField(null=True, blank=True)
    hawb_5 = models.ForeignKey(Bills, on_delete=models.CASCADE, related_name='hawb_5', null=True, blank=True)
    quantity_pending = models.IntegerField(null=True) # số lượng hàng chưa về
    note = models.TextField(null=True, blank=True)
