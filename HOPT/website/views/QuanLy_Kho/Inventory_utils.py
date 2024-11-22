from django.db.models import Q, Sum
from django.core.paginator import Paginator
from website.models import Inventory, Goods_Receipt, Goods_Issue
import json

def get_previous_inventory(product_code, warehouse_code, year):
    """
    Tính toán tồn trước đó của một sản phẩm trong một kho cụ thể, trước năm được chọn.
    """
    # Tổng số lượng nhập của sản phẩm trước năm được chọn
    total_received = Goods_Receipt.objects.filter(
        products__product_code=product_code,
        warehouse__warehouse_code=warehouse_code,
        receipt_date__year__lt=year  # Các năm trước
    ).aggregate(Sum('quantity'))['quantity__sum'] or 0

    # Tổng số lượng xuất của sản phẩm trước năm được chọn
    total_issued = Goods_Issue.objects.filter(
        products__product_code=product_code,
        warehouse__warehouse_code=warehouse_code,
        issue_date__year__lt=year  # Các năm trước
    ).aggregate(Sum('quantity'))['quantity__sum'] or 0

    # Tồn trước đó = tổng nhập - tổng xuất
    previous_inventory = total_received - total_issued
    return previous_inventory

def get_inventory_data_for_year(selected_year):
    inventory_data = []
    
    # Lấy danh sách tất cả mã hàng và mã kho từ các hàng nhập kho
    goods_receipts = Goods_Receipt.objects.values('products__product_code', 'warehouse__warehouse_code').distinct()

    # Tính toán tồn trước đó, tổng nhập, tổng xuất, tồn hiện tại cho từng mã hàng
    for item in goods_receipts:
        product_code = item['products__product_code']
        warehouse_code = item['warehouse__warehouse_code']

        # Tính tồn trước đó
        previous_inventory = get_previous_inventory(product_code, warehouse_code, selected_year)

        # Tính tổng nhập trong năm được chọn
        total_received = Goods_Receipt.objects.filter(
            products__product_code=product_code,
            warehouse__warehouse_code=warehouse_code,
            receipt_date__year=selected_year
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        # Tính tổng xuất trong năm được chọn
        total_issued = Goods_Issue.objects.filter(
            products__product_code=product_code,
            warehouse__warehouse_code=warehouse_code,
            issue_date__year=selected_year
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        # Tính tồn hiện tại
        current_inventory = previous_inventory + total_received - total_issued

        # Thêm vào danh sách dữ liệu tồn kho
        inventory_data.append({
            'product_code': product_code,
            'warehouse_code': warehouse_code,
            'previous_inventory': previous_inventory,
            'total_received': total_received,
            'total_issued': total_issued,
            'current_inventory': current_inventory,
            'inventory_valuation': 0,  # Để trống theo yêu cầu
        })

    return inventory_data

def get_filter_parameters(request):
    search_query_main = request.GET.get('search_main', '')
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')

    selected_product_types = request.GET.get('product_type', '')
    selected_warehouses = request.GET.get('warehouse', '')

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

    return search_query_main, sort_by, sort_order, items_per_page, selected_product_types, selected_warehouses

def get_sorted_warehouse_list(search_query_main, selected_product_types, selected_warehouses, sort_by, sort_order, items_per_page, selected_year=None):
    valid_sort_fields = ['stt', 'product__product_code', 'warehouse__name', 'previous_inventory', 'total_received', 'total_issued', 'current_inventory', 'min_inventory', 'inventory_valuation']

    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'
    
    if sort_by not in valid_sort_fields:
        sort_by = 'stt'
    
    order_by_clause = f"{'-' if sort_order == 'desc' else ''}{sort_by}"

    inventory_list = Inventory.objects.select_related('product', 'warehouse')

    if selected_year:
        inventory_list = inventory_list.filter(years=selected_year)

    if search_query_main:
        inventory_list = inventory_list.filter(
            Q(product__product_code__icontains=search_query_main) |
            Q(warehouse__name__icontains=search_query_main)
        )

    if selected_product_types:
        inventory_list = inventory_list.filter(product__product_type__product_type_code__in=selected_product_types)

    if selected_warehouses:
        inventory_list = inventory_list.filter(warehouse__warehouse_code__in=selected_warehouses)

    inventory_list = inventory_list.order_by(order_by_clause)

    paginator = Paginator(inventory_list, int(items_per_page))
    return paginator

def get_yearly_totals(selected_years_sub, search_query_sub=''):
    """Tính tổng số lượng nhập và xuất theo tháng của năm được chọn."""
    # Lọc và làm duy nhất trước khi union
    receipt_codes = Goods_Receipt.objects.filter(
        receipt_date__year=selected_years_sub,
        products__product_code__icontains=search_query_sub
    ).values_list('products__product_code', flat=True).distinct()

    issue_codes = Goods_Issue.objects.filter(
        issue_date__year=selected_years_sub,
        products__product_code__icontains=search_query_sub
    ).values_list('products__product_code', flat=True).distinct()

    # Union mà không gọi distinct sau đó
    # Kết hợp, làm duy nhất và sắp xếp theo mã hàng
    product_codes = sorted(set(receipt_codes) | set(issue_codes))  # Kết hợp và làm duy nhất bằng Python

    yearly_totals = []

    for product_code in product_codes:
        monthly_totals = [{'receipt': 0, 'issue': 0} for _ in range(12)]
        total_quantity_receipt = 0
        total_quantity_issue = 0

        for month in range(1, 13):
            receipt_total = Goods_Receipt.objects.filter(
                receipt_date__year=selected_years_sub,
                receipt_date__month=month,
                products__product_code=product_code
            ).aggregate(total=Sum('quantity'))['total'] or 0

            issue_total = Goods_Issue.objects.filter(
                issue_date__year=selected_years_sub,
                issue_date__month=month,
                products__product_code=product_code
            ).aggregate(total=Sum('quantity'))['total'] or 0

            monthly_totals[month - 1]['receipt'] = receipt_total
            monthly_totals[month - 1]['issue'] = issue_total

            total_quantity_receipt += receipt_total
            total_quantity_issue += issue_total

        yearly_totals.append({
            'product_code': product_code,
            'monthly_totals': monthly_totals,
            'total_receipt': total_quantity_receipt,
            'total_issue': total_quantity_issue,
        })

    return yearly_totals



