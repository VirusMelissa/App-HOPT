from django.db.models import Q, Sum
from django.core.paginator import Paginator
from website.models import Goods_Issue, Goods_Receipt
import json
from django.db import models

def get_total_quantity_per_product_in_warehouse():
    # Lấy tổng số lượng sản phẩm nhận được vào kho
    quantities = Goods_Receipt.objects.values('products__product_code', 'warehouse__warehouse_code') \
        .annotate(total_received=Sum('quantity'))
    
    # Lấy tổng số lượng sản phẩm được xuất kho
    issued_quantities = Goods_Issue.objects.values('products__product_code', 'warehouse__warehouse_code') \
        .annotate(total_issued=Sum('quantity'))
    
    # Chuyển đổi danh sách thành từ điển để tra cứu dễ dàng hơn
    total_received = {(item['warehouse__warehouse_code'], item['products__product_code']): item['total_received'] for item in quantities}
    total_issued = {(item['warehouse__warehouse_code'], item['products__product_code']): item['total_issued'] for item in issued_quantities}
    
    # Tính toán lượng hàng tồn kho có sẵn bằng cách trừ số lượng đã xuất kho khỏi số lượng đã nhận
    total_quantities = {}
    for (warehouse_code, product_code), received_qty in total_received.items():
        issued_qty = total_issued.get((warehouse_code, product_code), 0)
        available_qty = received_qty - issued_qty
        
        if warehouse_code not in total_quantities:
            total_quantities[warehouse_code] = {}
        total_quantities[warehouse_code][product_code] = available_qty
    
    return total_quantities


def get_filter_parameters(request):
    search_query_main = request.GET.get('search_main', '')
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')
    

    selected_years_main = request.GET.get('year_main', '')
    selected_product_types = request.GET.get('product_type', '')
    selected_warehouses = request.GET.get('warehouse', '')

    # Xử lý danh sách năm
    try:
        if selected_years_main.startswith("["):
            selected_years_main = json.loads(selected_years_main)
        else:
            selected_years_main = selected_years_main.split(',')
        selected_years_main = [int(year) for year in selected_years_main if year]
    except (json.JSONDecodeError, ValueError):
        selected_years_main = []

    # Xử lý danh sách loại hàng
    try:
        if selected_product_types.startswith("["):
            selected_product_types = json.loads(selected_product_types)
        else:
            selected_product_types = selected_product_types.split(',')
        selected_product_types = [ptype for ptype in selected_product_types if ptype]
    except json.JSONDecodeError:
        selected_product_types = []

    # Xử lý danh sách kho
    try:
        if selected_warehouses.startswith("["):
            selected_warehouses = json.loads(selected_warehouses)
        else:
            selected_warehouses = selected_warehouses.split(',')
        selected_warehouses = [wh for wh in selected_warehouses if wh]
    except json.JSONDecodeError:
        selected_warehouses = []

    return search_query_main, sort_by, sort_order, items_per_page, selected_years_main, selected_product_types, selected_warehouses

def get_sorted_warehouse_list(search_query_main, selected_years_main, selected_product_types, selected_warehouses, sort_by, sort_order, items_per_page):
    valid_sort_fields = ['stt', 'products__product_code', 'order__order_number', 'issue_date', 'quantity', 'warehouse__name', 'customers__customer_name', 'employees__full_name']

    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'
    
    if sort_by not in valid_sort_fields:
        sort_by = 'stt'
    
    order_by_clause = f"{'-' if sort_order == 'desc' else ''}{sort_by}"

    issue_list = Goods_Issue.objects.select_related('products', 'order', 'warehouse', 'customers', 'employees')

    if search_query_main:
        issue_list = issue_list.filter(
            Q(products__product_code__icontains=search_query_main) |
            Q(order__order_number__icontains=search_query_main) |
            Q(warehouse__name__icontains=search_query_main) |
            Q(customers__customer_name__icontains=search_query_main) |
            Q(employees__full_name__icontains=search_query_main)
        )

    if selected_years_main:
        issue_list = issue_list.filter(issue_date__year__in=selected_years_main)

    if selected_product_types:
        issue_list = issue_list.filter(products__product_type__product_type_code__in=selected_product_types)

    if selected_warehouses:
        issue_list = issue_list.filter(warehouse__warehouse_code__in=selected_warehouses)

    issue_list = issue_list.order_by(order_by_clause)

    paginator = Paginator(issue_list, int(items_per_page))
    return paginator

def get_yearly_totals(selected_years_sub, search_query_sub=''):
    product_codes = Goods_Issue.objects.filter(issue_date__year=selected_years_sub).values_list('products__product_code', flat=True).distinct().order_by('products__product_code')
    
    if search_query_sub:
        product_codes = product_codes.filter(products__product_code__icontains=search_query_sub)
    
    yearly_totals = []

    for product_code in product_codes:
        monthly_totals = [0] * 12
        total_quantity = 0

        for month in range(1, 13):
            total = Goods_Issue.objects.filter(
                issue_date__year=selected_years_sub,
                issue_date__month=month,
                products__product_code=product_code
            ).aggregate(total=Sum('quantity'))['total'] or 0
            monthly_totals[month - 1] = total
            total_quantity += total

        yearly_totals.append({
            'product_code': product_code,
            'monthly_totals': monthly_totals,
            'total_quantity': total_quantity,
        })

    return yearly_totals


def get_yearly_customer_totals(selected_year_sub, search_query_sub=''):
    # Lấy mã hàng duy nhất và danh sách khách hàng
    product_codes = Goods_Issue.objects.filter(issue_date__year=selected_year_sub).values_list('products__product_code', flat=True).distinct().order_by('products__product_code')
    customers = Goods_Issue.objects.filter(issue_date__year=selected_year_sub).values('customers__customer_code').distinct().order_by('customers__customer_code')

    if search_query_sub:
        product_codes = product_codes.filter(products__product_code__icontains=search_query_sub)
    
    yearly_customer_totals = []
    
    for product_code in product_codes:
        customer_totals = []
        total_quantity = 0
        
        for customer in customers:
            customer_code = customer['customers__customer_code']
            total = Goods_Issue.objects.filter(
                issue_date__year=selected_year_sub,
                products__product_code=product_code,
                customers__customer_code=customer_code
            ).aggregate(total=Sum('quantity'))['total'] or 0
            customer_totals.append(total)
            total_quantity += total

        yearly_customer_totals.append({
            'product_code': product_code,
            'customer_totals': customer_totals,
            'total_quantity': total_quantity,
        })

    return yearly_customer_totals, customers
