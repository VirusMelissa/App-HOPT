from django.db.models import Q, Sum
from django.core.paginator import Paginator
from website.models import Order_Details
import json


def get_filter_parameters(request):
    """
    Lấy các tham số lọc từ request.
    """
    search_query_main = request.GET.get('search_main', '')
    sort_by = request.GET.get('sort', 'stt')
    sort_order = request.GET.get('order', 'asc')
    items_per_page = request.GET.get('items_per_page', '20')

    selected_years_main = request.GET.get('year_main', '')
    selected_product_types = request.GET.get('product_type', '')
    selected_order_status = request.GET.get('order_status', '')

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

    # Xử lý danh sách trạng thái đơn hàng
    try:
        if selected_order_status.startswith("["):
            selected_order_status = json.loads(selected_order_status)
        else:
            selected_order_status = selected_order_status.split(',')
        selected_order_status = [status for status in selected_order_status if status]
    except json.JSONDecodeError:
        selected_order_status = []

    return search_query_main, sort_by, sort_order, items_per_page, selected_years_main, selected_product_types, selected_order_status


def get_sorted_order_list(search_query_main, selected_years_main, selected_product_types, selected_order_status, sort_by, sort_order, items_per_page):
    """
    Lấy danh sách đơn hàng đã được lọc và sắp xếp.
    """
    valid_sort_fields = [
        'stt',                          # STT
        'products__product_code',        # Mã hàng (sử dụng ForeignKey từ Products)
        'quantity',                      # Số lượng
        'unit_price',                    # Đơn giá
        'order_date',                    # Ngày đặt hàng
        'contracts__contract_number',    # Số hợp đồng (sử dụng ForeignKey từ Contracts)
        'order_confirmation__order_code', # Mã xác nhận đơn hàng (sử dụng ForeignKey từ Orders)
        'customers__name',               # Tên khách hàng (sử dụng ForeignKey từ Customers)
        'employees__full_name',          # Tên nhân viên phụ trách (sử dụng ForeignKey từ Employees)
        'advance_date',                  # Ngày tạm ứng
        'from_date',                     # Ngày bắt đầu
        'to_date',                       # Ngày kết thúc
        'order_status',                  # Tình trạng đơn hàng
        'estimated_date_1',              # Ngày dự kiến lần 1
        'estimated_date_2',              # Ngày dự kiến lần 2
        'inv_1__invoice_number',         # Số hóa đơn 1 (sử dụng ForeignKey từ Invoice)
        'pkl_1__packing_list_code',      # Mã packing list 1 (sử dụng ForeignKey từ Packing_List)
        'quantity_batch_1',              # Số lượng lô 1
        'hawb_1__bill_code',             # Mã bill 1 (sử dụng ForeignKey từ Bills)
        'inv_2__invoice_number',         # Số hóa đơn 2 (sử dụng ForeignKey từ Invoice)
        'pkl_2__packing_list_code',      # Mã packing list 2 (sử dụng ForeignKey từ Packing_List)
        'quantity_batch_2',              # Số lượng lô 2
        'hawb_2__bill_code',             # Mã bill 2 (sử dụng ForeignKey từ Bills)
        'inv_3__invoice_number',         # Số hóa đơn 3 (sử dụng ForeignKey từ Invoice)
        'pkl_3__packing_list_code',      # Mã packing list 3 (sử dụng ForeignKey từ Packing_List)
        'quantity_batch_3',              # Số lượng lô 3
        'hawb_3__bill_code',             # Mã bill 3 (sử dụng ForeignKey từ Bills)
        'inv_4__invoice_number',         # Số hóa đơn 4 (sử dụng ForeignKey từ Invoice)
        'pkl_4__packing_list_code',      # Mã packing list 4 (sử dụng ForeignKey từ Packing_List)
        'quantity_batch_4',              # Số lượng lô 4
        'hawb_4__bill_code',             # Mã bill 4 (sử dụng ForeignKey từ Bills)
        'inv_5__invoice_number',         # Số hóa đơn 5 (sử dụng ForeignKey từ Invoice)
        'pkl_5__packing_list_code',      # Mã packing list 5 (sử dụng ForeignKey từ Packing_List)
        'quantity_batch_5',              # Số lượng lô 5
        'hawb_5__bill_code',             # Mã bill 5 (sử dụng ForeignKey từ Bills)
        'quantity_pending',              # Số lượng hàng chưa về
        'note',                          # Chú thích
    ]


    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'
    
    if sort_by not in valid_sort_fields:
        sort_by = 'stt'
    
    order_by_clause = f"{'-' if sort_order == 'desc' else ''}{sort_by}"

    order_list = Order_Details.objects.select_related(
        'products', 'customers', 'contracts', 'order_confirmation',
        'inv_1', 'pkl_1', 'hawb_1',
        'inv_2', 'pkl_2', 'hawb_2',
        'inv_3', 'pkl_3', 'hawb_3',
        'inv_4', 'pkl_4', 'hawb_4',
        'inv_5', 'pkl_5', 'hawb_5'
    )

    # Thêm điều kiện tìm kiếm nếu có
    if search_query_main:
        order_list = order_list.filter(
            Q(products__product_code__icontains=search_query_main) |
            Q(contracts__contract_number__icontains=search_query_main) |
            Q(customers__name__icontains=search_query_main) |
            Q(order_confirmation__order_number__icontains=search_query_main)
        )

    # Thêm điều kiện lọc theo năm nếu có
    if selected_years_main:
        order_list = order_list.filter(from_date__year__in=selected_years_main)

    # Thêm điều kiện lọc theo loại hàng nếu có
    if selected_product_types:
        warehouse_list = warehouse_list.filter(products__product_type__product_type_code__in=selected_product_types)

    # Thêm điều kiện lọc theo tình trạng đơn hàng nếu có
    if selected_order_status:
        order_list = order_list.filter(order_status__in=selected_order_status)

    # Sắp xếp danh sách dựa trên cột và thứ tự được chọn
    order_list = order_list.order_by(order_by_clause)

    # Phân trang dữ liệu
    paginator = Paginator(order_list, int(items_per_page))
    return paginator


def get_yearly_totals(selected_year, search_query_sub=''):
    """
    Tính tổng số lượng sản phẩm theo tháng trong năm đã chọn.
    """
    product_codes = Order_Details.objects.filter(
        from_date__year=selected_year
    ).values_list('products__product_code', flat=True).distinct().order_by('products__product_code')
    
    if search_query_sub:
        product_codes = product_codes.filter(products__product_code__icontains=search_query_sub)
    
    yearly_totals = []

    for product_code in product_codes:
        monthly_totals = [0] * 12
        total_quantity = 0

        for month in range(1, 13):
            total = Order_Details.objects.filter(
                from_date__year=selected_year,
                from_date__month=month,
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
