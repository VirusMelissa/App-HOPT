from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from website.models import Goods_Issue, Orders, Products, Warehouse, Customers, Employees, Product_Type
from django.db.models.functions import ExtractYear
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import models
from .Goods_Issue_utils import get_filter_parameters, get_sorted_warehouse_list, get_yearly_totals, get_yearly_customer_totals, get_total_quantity_per_product_in_warehouse
from urllib.parse import urlencode
import json
from django.http import JsonResponse

def is_authorized(user):
    return user.role in ['warehouse_staff', 'admin']

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Goods_Issue_View(request):
    # Lấy các tham số tìm kiếm và lọc của main-content
    search_query_main, sort_by, sort_order, items_per_page, selected_years_main, selected_product_types, selected_warehouses = get_filter_parameters(request)

    # Lấy tham số tìm kiếm của sub-content
    search_query_sub = request.GET.get('search_sub', '')

    # Lấy tất cả các năm và loại hàng nếu không có bộ lọc nào
    available_years = Goods_Issue.objects.annotate(
        year=ExtractYear('issue_date')
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

    paginator = get_sorted_warehouse_list(search_query_main, selected_years_main, selected_product_types, selected_warehouses ,sort_by, sort_order, items_per_page)
    page_number = request.GET.get('page')
    issue_list = paginator.get_page(page_number)

    # Tính tổng số lượng hàng xuất theo năm
    yearly_totals = get_yearly_totals(selected_years_sub, search_query_sub)

    # Tính tổng số lượng hàng xuất theo khách hàng
    yearly_customer_totals, customers = get_yearly_customer_totals(selected_years_sub, search_query_sub)
    customer_list = [customer['customers__customer_code'] for customer in customers]  # Chuyển đổi về danh sách mã khách hàng

    columns = [
            {'name': 'STT', 'field': 'stt'},
            {'name': 'Mã hàng', 'field': 'products__product_code'},
            {'name': 'Đơn hàng', 'field': 'order__order_number'},
            {'name': 'Ngày xuất', 'field': 'issue_date'},
            {'name': 'Số lượng', 'field': 'quantity'},
            {'name': 'Kho', 'field': 'warehouse__name'},
            {'name': 'Khách hàng', 'field': 'customers__customer_name'},
            {'name': 'Người phụ trách', 'field': 'employees__full_name'},
        ]
    
    hidden_fields = [
        {'name': 'page', 'value': issue_list.number},
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
    base_pagination_url = f"?{urlencode(filtered_query_params)}"

    return render(request, 'QuanLy_Kho/Goods_Issue.html', {
        'list': issue_list,
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
        'yearly_customer_totals': yearly_customer_totals,
        'months': range(1, 13), # Truyền danh sách tháng từ 1 đến 12
        'customer_list': customer_list,
        'base_pagination_url': base_pagination_url,
        'hidden_fields': hidden_fields,
        'columns': columns,  
    })

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Add_Goods_Issue_View(request):
    # Lấy các tham số từ request
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')
    selected_years_sub = request.GET.get('year_sub', '')
    selected_years_main = request.GET.get('year_main', '')
    selected_product_types = request.GET.get('product_type', '')
    search_query_sub = request.GET.get('search_sub', '')
    search_query_main = request.GET.get('search_main', '')

    total_quantities = get_total_quantity_per_product_in_warehouse()  # Lấy số lượng tồn kho của từng sản phẩm theo kho
    # Chuyển đổi total_quantities thành chuỗi JSON
    total_quantities_json = json.dumps(total_quantities)

    if request.method == 'POST':
        # Các biến request POST
        order_id = request.POST.get('order')
        products_id = request.POST.get('products')
        issue_date = request.POST.get('issue_date')
        quantity = int(request.POST.get('quantity', 0))
        warehouse_id = request.POST.get('warehouse')
        customer_id = request.POST.get('customers')
        employee_id = request.POST.get('employees')

        try:
            # Lấy đối tượng từ các mã sản phẩm, kho, khách hàng và nhân viên
            order = Orders.objects.get(order_number=order_id)
            product = Products.objects.get(product_code=products_id)
            warehouse = Warehouse.objects.get(warehouse_code=warehouse_id)
            customer = Customers.objects.get(customer_code=customer_id)
            employee = Employees.objects.get(employee_code=employee_id)

            # Tìm số thứ tự stt mới
            last_stt = Goods_Issue.objects.aggregate(max_stt=models.Max('stt'))['max_stt']
            next_stt = (last_stt or 0) + 1

            new_issue = Goods_Issue(
                stt=next_stt,
                order=order,
                products=product,
                issue_date=issue_date,
                warehouse=warehouse,
                quantity=quantity,
                customers=customer,
                employees=employee
            )
            new_issue.save()

            # Điều hướng
            url = reverse('goods_issue')
            return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&items_per_page={items_per_page}&year_sub={selected_years_sub}&year_main={selected_years_main}&product_type={selected_product_types}&search_sub={search_query_sub}&search_main={search_query_main}")

        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')

    # Lấy dữ liệu cho template
    products = Products.objects.all()
    order = Orders.objects.all()
    warehouse = Warehouse.objects.all()
    customers = Customers.objects.all()
    employees = Employees.objects.all()

    return render(request, 'QuanLy_Kho/Add_product_Goods_Issue.html', {
        'products': products,
        'order': order,
        'total_quantities_json': total_quantities_json,  # Truyền chuỗi JSON vào template
        'warehouse': warehouse,
        'customers': customers,
        'employees': employees
    })

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Edit_Goods_Issue_View(request, issue_id):
    issue = get_object_or_404(Goods_Issue, id=issue_id)

    # Lấy các tham số từ request
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')
    selected_years_sub = request.GET.get('year_sub', '')
    selected_years_main = request.GET.get('year_main', '')
    selected_product_types = request.GET.get('product_type', '')
    search_query_sub = request.GET.get('search_sub', '')
    search_query_main = request.GET.get('search_main', '')

    total_quantities = get_total_quantity_per_product_in_warehouse()  # Lấy số lượng tồn kho của từng sản phẩm theo kho
    # Chuyển đổi total_quantities thành chuỗi JSON
    total_quantities_json = json.dumps(total_quantities)

    if request.method == 'POST':
        order_id = request.POST.get('order')
        products_id = request.POST.get('products')
        issue_date = request.POST.get('issue_date')
        quantity = request.POST.get('quantity')
        warehouse_id = request.POST.get('warehouse')
        customer_id = request.POST.get('customers')
        employee_id = request.POST.get('employees')

        try:
            order = Orders.objects.get(order_number=order_id)
            product = Products.objects.get(product_code=products_id)
            warehouse = Warehouse.objects.get(warehouse_code=warehouse_id)
            customer = Customers.objects.get(customer_code=customer_id)
            employee = Employees.objects.get(employee_code=employee_id)

            issue.products = product
            issue.order = order
            issue.issue_date = issue_date
            issue.quantity = quantity
            issue.warehouse = warehouse
            issue.customers = customer
            issue.employees = employee
            issue.save()

            url = reverse('goods_issue')  # Thay 'warehouse_issue' bằng tên URL của bạn nếu khác
            return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&items_per_page={items_per_page}&year_sub={selected_years_sub}&year_main={selected_years_main}&product_type={selected_product_types}&search_sub={search_query_sub}&search_main={search_query_main}")
        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')

    products = Products.objects.all()
    order = Orders.objects.all()
    warehouse = Warehouse.objects.all()
    customers = Customers.objects.all()
    employees = Employees.objects.all()
    return render(request, 'QuanLy_Kho/Edit_product_Goods_Issue.html', {
        'issue': issue,
        'products': products,
        'order': order,
        'total_quantities_json': total_quantities_json,
        'warehouse': warehouse,
        'customers': customers,
        'employees': employees
    })

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Delete_Goods_Issue_View(request, issue_id):
    issue = get_object_or_404(Goods_Issue, id=issue_id)

    # Lấy các tham số từ request
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')
    selected_years_sub = request.GET.get('year_sub', '')
    selected_years_main = request.GET.get('year_main', '')
    selected_product_types = request.GET.get('product_type', '')
    search_query_sub = request.GET.get('search_sub', '')
    search_query_main = request.GET.get('search_main', '')

    if request.method == 'POST':
        # Lưu lại số thứ tự của issue sẽ bị xóa
        issue_stt = issue.stt

        # Xóa đối tượng khi người dùng xác nhận
        issue.delete()

        # Cập nhật lại số thứ tự cho các mục còn lại
        remaining_entries = Goods_Issue.objects.filter(stt__gt=issue_stt).order_by('stt')
        for i, remaining_issue in enumerate(remaining_entries, start=issue_stt):
            remaining_issue.stt = i
            remaining_issue.save()

        url = reverse('goods_issue')  # Thay 'warehouse_issue' bằng tên URL của bạn nếu khác
        return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&items_per_page={items_per_page}&year_sub={selected_years_sub}&year_main={selected_years_main}&product_type={selected_product_types}&search_sub={search_query_sub}&search_main={search_query_main}")

    return render(request, 'QuanLy_Kho/confirm_delete_Goods_Issue.html', {'issue': issue})
