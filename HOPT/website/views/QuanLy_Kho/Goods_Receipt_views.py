from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from website.models import Goods_Receipt, Suppliers, Bills, Contracts, Products, Product_Type, Warehouse
from .Goods_Receipt_utils import get_filter_parameters, get_sorted_warehouse_list, get_yearly_totals
from django.db.models.functions import ExtractYear
from django.contrib import messages
from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

def is_authorized(user):
    return user.role in ['warehouse_staff', 'admin']

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')  # Đổi redirect tới hàm unauthorized_access
def Goods_Receipt_View(request):
    # Lấy các tham số tìm kiếm và lọc của main-content
    search_query_main, sort_by, sort_order, items_per_page, selected_years_main, selected_product_types, selected_warehouses = get_filter_parameters(request)

    # Lấy tham số tìm kiếm của sub-content
    search_query_sub = request.GET.get('search_sub', '')

    # Lấy tất cả các năm và loại hàng nếu không có bộ lọc nào
    available_years = Goods_Receipt.objects.annotate(
        year=ExtractYear('receipt_date')
    ).values_list('year', flat=True).distinct().order_by('-year')

    available_product_types = Product_Type.objects.all()
    available_warehouses = Warehouse.objects.all()

    # Xử lý selected_year_sub
    selected_years_sub = request.GET.get('year_sub', None)
    if selected_years_sub is None or selected_years_sub == '[]':
        selected_years_sub = available_years[0] if available_years else None
    else:
        try:
            selected_years_sub = int(selected_years_sub)
        except (ValueError, TypeError):
            selected_years_sub = available_years[0] if available_years else None

    # Lấy danh sách warehouse và phân trang cho main-content
    paginator = get_sorted_warehouse_list(search_query_main, selected_years_main, selected_product_types, selected_warehouses ,sort_by, sort_order, items_per_page)
    page_number = request.GET.get('page')
    warehouse_list = paginator.get_page(page_number)

    # Tính tổng số lượng theo tháng cho sub-content
    yearly_totals = get_yearly_totals(selected_years_sub, search_query_sub)

    columns = [
            {'name': 'STT', 'field': 'stt'},
            {'name': 'Mã hàng', 'field': 'products__product_code'},
            {'name': 'Ngày nhập', 'field': 'receipt_date'},
            {'name': 'Số lượng', 'field': 'quantity'},
            {'name': 'Nhà cung cấp', 'field': 'suppliers__supplier_name'},
            {'name': 'Kho', 'field': 'warehouse__name'},
            {'name': 'Mã bill', 'field': 'bills__bill_code'},
            {'name': 'Số hợp đồng', 'field': 'contracts__contract_number'},
        ]

    hidden_fields = [
        {'name': 'page', 'value': warehouse_list.number},
        {'name': 'sort', 'value': sort_by},
        {'name': 'order', 'value': sort_order},
        {'name': 'items_per_page', 'value': items_per_page},
        {'name': 'year_sub', 'value': selected_years_sub},
        {'name': 'year_main', 'value': ",".join(map(str, selected_years_main)) if selected_years_main else ''},
        {'name': 'product_type', 'value': ",".join(map(str, selected_product_types)) if selected_product_types else ''},
        {'name': 'warehouse', 'value': ",".join(map(str, selected_warehouses)) if selected_warehouses else ''},
        {'name': 'search_sub', 'value': search_query_sub},
        {'name': 'search_main', 'value': search_query_main}
    ]

    # Tạo URL cơ bản cho phân trang, bỏ qua `page`
    query_params = {
        'sort': sort_by,
        'order': sort_order,
        'items_per_page': items_per_page,
        'year_sub': selected_years_sub,
        'year_main': ",".join(map(str, selected_years_main)) if selected_years_main else '',
        'product_type': ",".join(map(str, selected_product_types)) if selected_product_types else '',
        'warehouse': ",".join(map(str, selected_warehouses)) if selected_warehouses else '',
        'search_main': search_query_main,
        'search_sub': search_query_sub
    }

    # Loại bỏ các mục có giá trị rỗng hoặc None
    filtered_query_params = {k: v for k, v in query_params.items() if v}
    base_pagination_url = f"&{urlencode(filtered_query_params)}"

    return render(request, 'QuanLy_Kho/Goods_Receipt.html', {
        'list': warehouse_list,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'items_per_page': items_per_page,
        'selected_years_main': selected_years_main,
        'available_product_types': available_product_types,
        'selected_product_types': selected_product_types,
        'available_warehouses': available_warehouses,
        'selected_warehouses': selected_warehouses,
        'available_years': available_years,
        'selected_year_sub': selected_years_sub,
        'search_main': search_query_main,
        'search_sub': search_query_sub,  # Đảm bảo chuyển search_sub vào template
        'yearly_totals': yearly_totals,
        'months': range(1, 13), # Truyền danh sách tháng từ 1 đến 12
        'base_pagination_url': base_pagination_url,
        'hidden_fields': hidden_fields,
        'columns': columns,  
    })


@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Add_Goods_Receipt_View(request):
    # Lấy các tham số từ request để khi thực hiện xong thao tác load lại trang vẫn giữ nguyên tham số cũ
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')
    selected_years_sub = request.GET.get('year_sub', '')
    selected_years_main = request.GET.get('year_main', '')
    selected_product_types = request.GET.get('product_type', '')
    selected_warehouses = request.GET.get('warehouse', '')
    search_query_sub = request.GET.get('search_sub', '')
    search_query_main = request.GET.get('search_main', '')

    if request.method == 'POST':
        products_id = request.POST.get('products')
        receipt_date = request.POST.get('receipt_date')
        quantity = request.POST.get('quantity')
        suppliers_id = request.POST.get('suppliers')
        warehouse_id = request.POST.get('warehouse')
        bills_id = request.POST.get('bills')
        contracts_id = request.POST.get('contracts')

        try:
            product = Products.objects.get(product_code=products_id)
            supplier = Suppliers.objects.get(supplier_code=suppliers_id)
            warehouse = Warehouse.objects.get(warehouse_code=warehouse_id)
            bill = Bills.objects.get(bill_code=bills_id)
            contract = Contracts.objects.get(contract_number=contracts_id)

            # Tìm giá trị số thứ tự lớn nhất hiện tại
            last_stt = Goods_Receipt.objects.aggregate(max_stt=models.Max('stt'))['max_stt']
            next_stt = (last_stt or 0) + 1  # Nếu không có stt nào, mặc định là 0 và cộng thêm 1

            new_entry = Goods_Receipt(
                stt=next_stt,  # Đặt giá trị stt tự động
                products=product,
                receipt_date=receipt_date, # vế bên phải lấy từ if request.method == 'POST':
                suppliers=supplier,
                warehouse=warehouse, # vế bên phải lấy từ try:
                bills=bill,
                contracts=contract,
                quantity=quantity
            )
            new_entry.save()

            url = reverse('goods_receipt')  # Thay 'warehouse_entry' bằng tên URL của bạn nếu khác
            return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&items_per_page={items_per_page}&year_sub={selected_years_sub}&year_main={selected_years_main}&product_type={selected_product_types}&warehouse={selected_warehouses}&search_sub={search_query_sub}&search_main={search_query_main}")

        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
            print(f'Error occurred: {str(e)}')  # In lỗi ra console

    products = Products.objects.all()
    suppliers = Suppliers.objects.all()
    warehouse = Warehouse.objects.all()
    bills = Bills.objects.all()
    contracts = Contracts.objects.all()
    return render(request, 'QuanLy_Kho/Add_product_Goods_Receipt.html', {
        'products': products,
        'suppliers': suppliers,
        'warehouse': warehouse,
        'bills': bills,
        'contracts': contracts
    })

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Edit_Goods_Receipt_View(request, entry_id):
    entry = get_object_or_404(Goods_Receipt, id=entry_id)

    # Lấy các tham số từ request
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')
    selected_years_sub = request.GET.get('year_sub', '')
    selected_years_main = request.GET.get('year_main', '')
    selected_product_types = request.GET.get('product_type', '')
    selected_warehouses = request.GET.get('warehouse', '')
    search_query_sub = request.GET.get('search_sub', '')
    search_query_main = request.GET.get('search_main', '')

    if request.method == 'POST':
        products_id = request.POST.get('products')
        receipt_date = request.POST.get('receipt_date')
        suppliers_id = request.POST.get('suppliers')
        warehouse_id = request.POST.get('warehouse')
        bills_id = request.POST.get('bills')
        contracts_id = request.POST.get('contracts')
        quantity = request.POST.get('quantity')

        try:
            product = Products.objects.get(product_code=products_id)
            supplier = Suppliers.objects.get(supplier_code=suppliers_id)
            warehouse = Warehouse.objects.get(warehouse_code=warehouse_id)
            bill = Bills.objects.get(bill_code=bills_id)
            contract = Contracts.objects.get(contract_number=contracts_id)

            entry.products = product
            entry.receipt_date = receipt_date
            entry.suppliers = supplier
            entry.warehouse = warehouse
            entry.bills = bill
            entry.contracts = contract
            entry.quantity = quantity
            entry.save()

            url = reverse('goods_receipt')  # Thay 'warehouse_entry' bằng tên URL của bạn nếu khác
            return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&items_per_page={items_per_page}&year_sub={selected_years_sub}&year_main={selected_years_main}&product_type={selected_product_types}&warehouse={selected_warehouses}&search_sub={search_query_sub}&search_main={search_query_main}")
        except Exception as e:
            print(f"Error: {str(e)}")
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')

    products = Products.objects.all()
    suppliers = Suppliers.objects.all()
    warehouse = Warehouse.objects.all()
    bills = Bills.objects.all()
    contracts = Contracts.objects.all()
    return render(request, 'QuanLy_Kho/Edit_product_Goods_Receipt.html', {
        'entry': entry,
        'products': products,
        'suppliers': suppliers,
        'warehouse': warehouse,
        'bills': bills,
        'contracts': contracts
    })

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Delete_Goods_Receipt_View(request, entry_id):
    entry = get_object_or_404(Goods_Receipt, id=entry_id)

    # Lấy các tham số từ request
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')
    selected_years_sub = request.GET.get('year_sub', '')
    selected_years_main = request.GET.get('year_main', '')
    selected_product_types = request.GET.get('product_type', '')
    selected_warehouses = request.GET.get('warehouse', '')
    search_query_sub = request.GET.get('search_sub', '')
    search_query_main = request.GET.get('search_main', '')

    if request.method == 'POST':
        # Lưu lại số thứ tự của entry sẽ bị xóa
        entry_stt = entry.stt

        # Xóa đối tượng khi người dùng xác nhận
        entry.delete()

        # Cập nhật lại số thứ tự cho các mục còn lại
        remaining_entries = Goods_Receipt.objects.filter(stt__gt=entry_stt).order_by('stt')
        for i, remaining_entry in enumerate(remaining_entries, start=entry_stt):
            remaining_entry.stt = i
            remaining_entry.save()

        url = reverse('goods_receipt')  # Thay 'warehouse_entry' bằng tên URL của bạn nếu khác
        return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&items_per_page={items_per_page}&year_sub={selected_years_sub}&year_main={selected_years_main}&product_type={selected_product_types}&warehouse={selected_warehouses}&search_sub={search_query_sub}&search_main={search_query_main}")

    # Nếu là GET, hiển thị trang xác nhận xóa
    return render(request, 'QuanLy_Kho/confirm_delete_Goods_Receipt.html', {'entry': entry})


