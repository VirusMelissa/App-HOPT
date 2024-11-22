from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from website.models import Inventory, Products, Warehouse, Product_Type, Goods_Receipt
from .Inventory_utils import get_filter_parameters, get_sorted_warehouse_list, get_inventory_data_for_year, get_yearly_totals
from django.db.models.functions import ExtractYear
from django.db import transaction
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import connection

def is_authorized(user):
    return user.role in ['warehouse_staff', 'admin', 'CEO']

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Inventory_View(request):
    # Lấy các năm từ Goods_Receipt
    available_years = Goods_Receipt.objects.annotate(year=ExtractYear('receipt_date')).values_list('year', flat=True).distinct().order_by('-year')

    # Lấy các tham số tìm kiếm và lọc của main-content
    search_query_main, sort_by, sort_order, items_per_page, selected_product_types, selected_warehouses = get_filter_parameters(request)
    search_query_sub = request.GET.get('search_sub', '')

    available_product_types = Product_Type.objects.all()
    available_warehouses = Warehouse.objects.all()

    # Xử lý selected_years_main
    selected_years_main = request.GET.get('year_main', None)
    if selected_years_main is None or selected_years_main == '[]':
        selected_years_main = available_years[0] if available_years else None
    else:
        try:
            selected_years_main = int(selected_years_main)
        except (ValueError, TypeError):
            selected_years_main = available_years[0] if available_years else None

    # Xử lý selected_year_sub
    selected_years_sub = request.GET.get('year_sub', None)
    if selected_years_sub is None or selected_years_sub == '[]':
        selected_years_sub = available_years[0] if available_years else None
    else:
        try:
            selected_years_sub = int(selected_years_sub)
        except (ValueError, TypeError):
            selected_years_sub = available_years[0] if available_years else None
    
    # Thêm bước lấy dữ liệu tồn kho cho năm đã chọn
    total_inventory = get_inventory_data_for_year(selected_years_main)

    paginator = get_sorted_warehouse_list(search_query_main, selected_product_types, selected_warehouses, sort_by, sort_order, items_per_page, selected_years_main)
    page_number = request.GET.get('page')
    inventory_list = paginator.get_page(page_number)

    # Tính tổng số lượng nhập và xuất theo tháng
    yearly_totals = get_yearly_totals(selected_years_sub, search_query_sub)

    columns = [
            {'name': 'STT', 'field': 'stt'},
            {'name': 'Mã hàng', 'field': 'products__product_code'},
            {'name': 'Kho', 'field': 'warehouse__name'},
            {'name': 'Tồn trước đó', 'field': 'previous_inventory'},
            {'name': 'Tổng nhập', 'field': 'total_received'},
            {'name': 'Tổng xuất', 'field': 'total_issued'},
            {'name': 'Tồn hiện tại', 'field': 'current_inventory'},
            {'name': 'Mức tồn tối thiểu', 'field': 'min_inventory'},
        ]
    
    hidden_fields = [
        {'name': 'page', 'value': inventory_list.number},
        {'name': 'sort', 'value': sort_by},
        {'name': 'order', 'value': sort_order},
        {'name': 'items_per_page', 'value': items_per_page},
        {'name': 'year_main', 'value': selected_years_main},
        {'name': 'product_type', 'value': ",".join(map(str, selected_product_types)) if selected_product_types else ''},
        {'name': 'warehouse', 'value': ",".join(map(str, selected_warehouses)) if selected_warehouses else ''},
        {'name': 'search_main', 'value': search_query_main}
    ]

    # Tạo URL cơ bản cho phân trang, bỏ qua `page`
    query_params = {
        'sort': sort_by,
        'order': sort_order,
        'items_per_page': items_per_page,
        'year_main': selected_years_main,
        'product_type': ",".join(map(str, selected_product_types)) if selected_product_types else '',
        'warehouse': ",".join(map(str, selected_warehouses)) if selected_warehouses else '',
        'search_main': search_query_main,
    }

    # Loại bỏ các mục có giá trị rỗng hoặc None
    filtered_query_params = {k: v for k, v in query_params.items() if v}
    base_pagination_url = f"&{urlencode(filtered_query_params)}"

    return render(request, 'QuanLy_Kho/Inventory.html', {
        'list': inventory_list,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'items_per_page': items_per_page,
        'selected_year_sub': selected_years_sub,
        'selected_years_main': selected_years_main,
        'available_product_types': available_product_types,
        'selected_product_types': selected_product_types,
        'available_warehouses': available_warehouses,
        'selected_warehouses': selected_warehouses,
        'search_sub': search_query_sub,
        'search_main': search_query_main,
        'base_pagination_url': base_pagination_url,
        'hidden_fields': hidden_fields,
        'columns': columns,
        'available_years': available_years,  
        'total_inventory': total_inventory,  
        'yearly_totals': yearly_totals,
        'months': range(1, 13), 
    })

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Add_Inventory_View(request):
    if request.method == 'POST':
        # print("Deleting all inventory records...")
        Inventory.objects.all().delete()

        # Đặt lại giá trị tự tăng của id về 1
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE inventory AUTO_INCREMENT = 1;")

        available_years = Goods_Receipt.objects.annotate(year=ExtractYear('receipt_date')).values_list('year', flat=True).distinct().order_by('-year')
        # print("Available years from Goods_Receipt:", list(available_years))

        with transaction.atomic():
            for selected_year in available_years:
                # print(f"Processing year: {selected_year}")
                counter = 1

                inventory_data = get_inventory_data_for_year(selected_year)
                
                for data in inventory_data:
                    #try:
                        product = Products.objects.get(product_code=data['product_code'])
                        warehouse = Warehouse.objects.get(warehouse_code=data['warehouse_code'])
                        # Kiểm tra trùng lặp trước khi thêm
                        if not Inventory.objects.filter(years=selected_year, product=product, warehouse=warehouse).exists():
                            # print(f"Adding inventory record for product {data['product_code']} in warehouse {data['warehouse_code']} for year {selected_year}")
                            Inventory.objects.create(
                                years=selected_year,
                                stt=counter,  # Gán STT từ biến đếm
                                product=product,
                                warehouse=warehouse,
                                previous_inventory=data['previous_inventory'],
                                total_received=data['total_received'],
                                total_issued=data['total_issued'],
                                current_inventory=data['current_inventory'],
                                min_inventory=data.get('min_inventory', 5),
                            )
                            counter += 1  # Tăng STT sau khi thêm bản ghi
                    # except Products.DoesNotExist:
                        # print(f"Product {data['product_code']} does not exist.")
                    # except Warehouse.DoesNotExist:
                        # print(f"Warehouse {data['warehouse_code']} does not exist.")

        # Thêm thông báo thành công vào URL sau khi cập nhật
        base_url = reverse('inventory')
        success_message = urlencode({'success': 'true'})
        return redirect(f"{base_url}?{success_message}")

    return redirect('inventory')

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Edit_Inventory_View(request, inventory_id):
    # Get the inventory item to edit
    inventory = get_object_or_404(Inventory, id=inventory_id)

    # Lấy các tham số từ request
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')
    selected_years_main = request.GET.get('year_main', '')
    selected_product_types = request.GET.get('product_type', '')
    selected_warehouses = request.GET.get('warehouse', '')
    search_query_main = request.GET.get('search_main', '')

    if request.method == 'POST':
        year = request.POST.get('years')
        products_id = request.POST.get('products')
        warehouse_id = request.POST.get('warehouse')
        previous_inventory = request.POST.get('previous_inventory')
        total_received = request.POST.get('total_received')
        total_issued = request.POST.get('total_issued')
        current_inventory = request.POST.get('current_inventory')
        min_inventory = request.POST.get('min_inventory')

        try:
            product = Products.objects.get(product_code=products_id)
            warehouse = Warehouse.objects.get(warehouse_code=warehouse_id)

            inventory.years = year
            inventory.product = product
            inventory.warehouse = warehouse
            inventory.previous_inventory = previous_inventory
            inventory.total_received = total_received
            inventory.total_issued = total_issued
            inventory.current_inventory = current_inventory
            inventory.min_inventory = min_inventory
            inventory.save()

            url = reverse('inventory')  # Thay bằng tên URL của bạn nếu khác
            return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&items_per_page={items_per_page}&year={selected_years_main}&product_type={selected_product_types}&warehouse={selected_warehouses}&search_main={search_query_main}")
        except Exception as e:
            print(f"Error: {str(e)}")
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')

    products = Products.objects.all()
    warehouse = Warehouse.objects.all()

    return render(request, 'QuanLy_Kho/Edit_Inventory.html', {
        'inventory': inventory,
        'products': products,
        'warehouse': warehouse,
    })