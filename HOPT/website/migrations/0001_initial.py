# Generated by Django 5.1.1 on 2024-11-22 02:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stt', models.IntegerField(blank=True, null=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('fullname', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('role', models.CharField(choices=[('admin', 'Quản trị viên'), ('warehouse_staff', 'Kho'), ('sales_staff', 'Sale'), ('technician', 'Kỹ thuật'), ('finance_staff', 'Nghiệp vụ'), ('team_R&D', 'R&D'), ('CEO', 'Giám Đốc')], default='sales_staff', max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('bill_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate_Of_Origin',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('co_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate_Of_Quality',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('cq_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('contract_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('customer_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('workplace', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Customs_Declaration',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('declaration_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('employee_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=10)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('citizen_identification', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('position', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('invoice_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('order_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('total_value', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Packing_List',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('packing_list_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Type',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('product_type_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('product_type_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('supplier_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('supplier_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('warehouse_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('department', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stt', models.IntegerField(unique=True)),
                ('customer_type', models.CharField(max_length=50)),
                ('field', models.CharField(max_length=50)),
                ('operation_scale', models.CharField(max_length=50)),
                ('sales_channel', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.customers')),
            ],
        ),
        migrations.CreateModel(
            name='Employee_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stt', models.IntegerField(unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('contract_number', models.CharField(max_length=50)),
                ('contract_sign_date', models.DateField()),
                ('contract_duration', models.CharField(max_length=100)),
                ('basic_salary', models.FloatField()),
                ('allowances', models.FloatField(blank=True, null=True)),
                ('employee_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.employees')),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stt', models.IntegerField(unique=True)),
                ('co', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.certificate_of_origin')),
                ('contract_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.contracts')),
                ('cq', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.certificate_of_quality')),
                ('customs_declaration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.customs_declaration')),
                ('hawb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.bills')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.invoice')),
                ('packing_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.packing_list')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('stt', models.IntegerField(unique=True)),
                ('product_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('origin_country', models.CharField(max_length=255)),
                ('net_weight', models.FloatField()),
                ('net_price', models.FloatField()),
                ('sales_unit', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.product_type')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stt', models.IntegerField(unique=True)),
                ('quantity', models.IntegerField()),
                ('order_date', models.DateField()),
                ('unit_price', models.FloatField()),
                ('advance_date', models.DateField(blank=True, null=True)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('order_status', models.CharField(max_length=50)),
                ('estimated_date_1', models.DateField(blank=True, null=True)),
                ('estimated_date_2', models.DateField(blank=True, null=True)),
                ('quantity_batch_1', models.IntegerField(blank=True, null=True)),
                ('quantity_batch_2', models.IntegerField(blank=True, null=True)),
                ('quantity_batch_3', models.IntegerField(blank=True, null=True)),
                ('quantity_batch_4', models.IntegerField(blank=True, null=True)),
                ('quantity_batch_5', models.IntegerField(blank=True, null=True)),
                ('quantity_pending', models.IntegerField(null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('contracts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.contracts')),
                ('customers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.customers')),
                ('employees', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.employees')),
                ('hawb_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hawb_1', to='website.bills')),
                ('hawb_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hawb_2', to='website.bills')),
                ('hawb_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hawb_3', to='website.bills')),
                ('hawb_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hawb_4', to='website.bills')),
                ('hawb_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hawb_5', to='website.bills')),
                ('inv_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inv_1', to='website.invoice')),
                ('inv_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inv_2', to='website.invoice')),
                ('inv_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inv_3', to='website.invoice')),
                ('inv_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inv_4', to='website.invoice')),
                ('inv_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inv_5', to='website.invoice')),
                ('order_confirmation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.orders')),
                ('pkl_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pkl_1', to='website.packing_list')),
                ('pkl_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pkl_2', to='website.packing_list')),
                ('pkl_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pkl_3', to='website.packing_list')),
                ('pkl_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pkl_4', to='website.packing_list')),
                ('pkl_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pkl_5', to='website.packing_list')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.products')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('years', models.IntegerField()),
                ('stt', models.IntegerField()),
                ('previous_inventory', models.IntegerField()),
                ('total_received', models.IntegerField()),
                ('total_issued', models.IntegerField()),
                ('current_inventory', models.IntegerField()),
                ('min_inventory', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.products')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.warehouse')),
            ],
            options={
                'db_table': 'inventory',
            },
        ),
        migrations.CreateModel(
            name='Goods_Receipt',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stt', models.IntegerField(unique=True)),
                ('receipt_date', models.DateField()),
                ('quantity', models.IntegerField(blank=True)),
                ('bills', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.bills')),
                ('contracts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.contracts')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.products')),
                ('suppliers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.suppliers')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Goods_Issue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stt', models.IntegerField(unique=True)),
                ('issue_date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('customers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.customers')),
                ('employees', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.employees')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.orders')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.products')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='MessageReadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.chatmessage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('message', 'user')},
            },
        ),
    ]
