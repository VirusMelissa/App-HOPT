from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.db.models.functions import ExtractYear
from website.models import Warehouse_Entries
import ast

def get_filter_parameters(request):
    """Lấy và xử lý các tham số lọc từ request."""
    search_query_main = request.GET.get('search_main', '')
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')
    selected_years_main = request.GET.get('year_main', '')  # Cho phần main
    selected_product_types = request.GET.get('product_type', '')

    # Xử lý selected_years_main
    if not selected_years_main:
        selected_years_main = []
    else:
        try:
            selected_years_main = ast.literal_eval(selected_years_main)
            if isinstance(selected_years_main, int):
                selected_years_main = [selected_years_main]
        except (ValueError, SyntaxError):
            selected_years_main = []

    # Xử lý selected_product_types
    if not selected_product_types:
        selected_product_types = []
    else:
        try:
            selected_product_types = ast.literal_eval(selected_product_types)
            if isinstance(selected_product_types, int):
                selected_product_types = [selected_product_types]
        except (ValueError, SyntaxError):
            selected_product_types = []

    return search_query_main, sort_by, sort_order, items_per_page, selected_years_main, selected_product_types

def get_sorted_warehouse_list(search_query_main, selected_years_main, selected_product_types, sort_by, sort_order, items_per_page):
    """Lấy danh sách warehouse đã được lọc và sắp xếp."""
    valid_sort_fields = [
        'stt', 'products__product_code', 'suppliers__supplier_name',
        'warehouse_receipts__warehouse_receipt_number', 'bills__bill_code',
        'contracts__contract_number', 'entry_date', 'quantity'
    ]

    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'
    
    if sort_by not in valid_sort_fields:
        sort_by = 'stt'
    
    order_by_clause = f"{'-' if sort_order == 'desc' else ''}{sort_by}"

    warehouse_list = Warehouse_Entries.objects.select_related(
        'products', 'suppliers', 'warehouse_receipts', 'bills', 'contracts'
    )

    # Thêm điều kiện tìm kiếm nếu có
    if search_query_main:
        warehouse_list = warehouse_list.filter(
            Q(products__product_code__icontains=search_query_main) |
            Q(suppliers__supplier_name__icontains=search_query_main) |
            Q(warehouse_receipts__warehouse_receipt_number__icontains=search_query_main) |
            Q(bills__bill_code__icontains=search_query_main) |
            Q(contracts__contract_number__icontains=search_query_main)
        )

    # Thêm điều kiện lọc theo năm nếu có
    if selected_years_main:
        warehouse_list = warehouse_list.filter(entry_date__year__in=selected_years_main)

    # Thêm điều kiện lọc theo loại hàng nếu có
    if selected_product_types:
        warehouse_list = warehouse_list.filter(products__product_type__id__in=selected_product_types)

    # Sắp xếp danh sách dựa trên cột và thứ tự được chọn
    warehouse_list = warehouse_list.order_by(order_by_clause)

    # Phân trang dữ liệu
    paginator = Paginator(warehouse_list, int(items_per_page))
    return paginator

def get_yearly_totals(selected_years_sub, search_query_sub=''):
    """Tính tổng số lượng theo tháng của năm được chọn."""
    product_codes = Warehouse_Entries.objects.filter(entry_date__year=selected_years_sub).values_list('products__product_code', flat=True).distinct().order_by('products__product_code')
    
    if search_query_sub:
        product_codes = product_codes.filter(products__product_code__icontains=search_query_sub)
    
    yearly_totals = []

    for product_code in product_codes:
        monthly_totals = [0] * 12  # Khởi tạo danh sách 12 tháng
        total_quantity = 0

        for month in range(1, 13):
            total = Warehouse_Entries.objects.filter(
                entry_date__year=selected_years_sub,
                entry_date__month=month,
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
