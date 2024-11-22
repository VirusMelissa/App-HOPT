from django.db.models import Q, Sum
from django.core.paginator import Paginator
from website.models import Goods_Receipt
import json

def get_filter_parameters(request):
    # Các phần đã có trước
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
    """Lấy danh sách warehouse đã được lọc và sắp xếp."""
    valid_sort_fields = [
        'stt', 'products__product_code', 'receipt_date', 'quantity', 'suppliers__supplier_name',
        'warehouse__name', 'bills__bill_code', 'contracts__contract_number'
    ]

    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'
    
    if sort_by not in valid_sort_fields:
        sort_by = 'stt'
    
    order_by_clause = f"{'-' if sort_order == 'desc' else ''}{sort_by}"

    warehouse_list = Goods_Receipt.objects.select_related('products', 'suppliers', 'warehouse', 'bills', 'contracts')

    # Thêm điều kiện tìm kiếm nếu có
    if search_query_main:
        warehouse_list = warehouse_list.filter(
            Q(products__product_code__icontains=search_query_main) |
            Q(suppliers__supplier_name__icontains=search_query_main) |
            Q(warehouse__name__icontains=search_query_main) |
            Q(bills__bill_code__icontains=search_query_main) |
            Q(contracts__contract_number__icontains=search_query_main)
        )

    # Thêm điều kiện lọc theo năm nếu có
    if selected_years_main:
        warehouse_list = warehouse_list.filter(receipt_date__year__in=selected_years_main)

    # Thêm điều kiện lọc theo loại hàng nếu có
    if selected_product_types:
        warehouse_list = warehouse_list.filter(products__product_type__product_type_code__in=selected_product_types)

    if selected_warehouses:
        warehouse_list = warehouse_list.filter(warehouse__warehouse_code__in=selected_warehouses)

    # Sắp xếp danh sách dựa trên cột và thứ tự được chọn
    warehouse_list = warehouse_list.order_by(order_by_clause)

    # Phân trang dữ liệu
    paginator = Paginator(warehouse_list, int(items_per_page))
    return paginator

def get_yearly_totals(selected_years_sub, search_query_sub=''):
    """Tính tổng số lượng theo tháng của năm được chọn."""
    product_codes = Goods_Receipt.objects.filter(receipt_date__year=selected_years_sub).values_list('products__product_code', flat=True).distinct().order_by('products__product_code')
    
    if search_query_sub:
        product_codes = product_codes.filter(products__product_code__icontains=search_query_sub)
    
    yearly_totals = []

    for product_code in product_codes:
        monthly_totals = [0] * 12  # Khởi tạo danh sách 12 tháng
        total_quantity = 0

        for month in range(1, 13):
            total = Goods_Receipt.objects.filter(
                receipt_date__year=selected_years_sub,
                receipt_date__month=month,
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
