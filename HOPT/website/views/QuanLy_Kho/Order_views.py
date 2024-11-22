from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from website.models import Order_Details, Customers, Products, Product_Type
from .Order_utils import get_filter_parameters, get_sorted_order_list, get_yearly_totals
from django.db.models.functions import ExtractYear
from urllib.parse import urlencode


def is_authorized(user):
    return user.role in ['sales_staff', 'admin', 'CEO']


@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Order_View(request):
    search_query_main, sort_by, sort_order, items_per_page, selected_years_main, selected_product_types, selected_customers, selected_order_status = get_filter_parameters(request)

    search_query_sub = request.GET.get('search_sub', '')

    available_years = Order_Details.objects.annotate(
        year=ExtractYear('order_date')
    ).values_list('year', flat=True).distinct().order_by('-year')

    available_product_types = Product_Type.objects.all()
    available_statuses = Order_Details.objects.values_list('order_status', flat=True).distinct()

    selected_years_sub = request.GET.get('year_sub', None)
    if selected_years_sub is None or selected_years_sub == '[]':
        selected_years_sub = available_years[0] if available_years else None
    else:
        try:
            selected_years_sub = int(selected_years_sub)
        except (ValueError, TypeError):
            selected_years_sub = available_years[0] if available_years else None

    paginator = get_sorted_order_list(search_query_main, selected_years_main, selected_product_types, selected_order_status, sort_by, sort_order, items_per_page)
    page_number = request.GET.get('page')
    order_list = paginator.get_page(page_number)

    yearly_totals = get_yearly_totals(selected_years_sub, search_query_sub)

    columns = [
        {'name': 'STT', 'field': 'stt'},
        {'name': 'Mã hàng', 'field': 'products__product_code'},
        {'name': 'Số lượng', 'field': 'quantity'},
        {'name': 'Đơn giá', 'field': 'unit_price'},
        {'name': 'Ngày đặt hàng', 'field': 'order_date'},
        {'name': 'Số hợp đồng', 'field': 'contracts__contract_number'},
        {'name': 'Mã xác nhận đơn hàng', 'field': 'order_confirmation__order_code'},
        {'name': 'Khách hàng', 'field': 'customers__name'},
        {'name': 'Nhân viên phụ trách', 'field': 'employees__full_name'},
        {'name': 'Ngày tạm ứng', 'field': 'advance_date'},
        {'name': 'Ngày bắt đầu', 'field': 'from_date'},
        {'name': 'Ngày kết thúc', 'field': 'to_date'},
        {'name': 'Tình trạng đơn hàng', 'field': 'order_status'},
        {'name': 'Ngày dự kiến 1', 'field': 'estimated_date_1'},
        {'name': 'Ngày dự kiến 2', 'field': 'estimated_date_2'},
        {'name': 'Số hóa đơn 1', 'field': 'inv_1__invoice_number'},
        {'name': 'Mã packing list 1', 'field': 'pkl_1__packing_list_code'},
        {'name': 'Số lượng lô 1', 'field': 'quantity_batch_1'},
        {'name': 'HAWB 1', 'field': 'hawb_1__bill_code'},
        {'name': 'Số hóa đơn 2', 'field': 'inv_2__invoice_number'},
        {'name': 'Mã packing list 2', 'field': 'pkl_2__packing_list_code'},
        {'name': 'Số lượng lô 2', 'field': 'quantity_batch_2'},
        {'name': 'HAWB 2', 'field': 'hawb_2__bill_code'},
        {'name': 'Số hóa đơn 3', 'field': 'inv_3__invoice_number'},
        {'name': 'Mã packing list 3', 'field': 'pkl_3__packing_list_code'},
        {'name': 'Số lượng lô 3', 'field': 'quantity_batch_3'},
        {'name': 'HAWB 3', 'field': 'hawb_3__bill_code'},
        {'name': 'Số hóa đơn 4', 'field': 'inv_4__invoice_number'},
        {'name': 'Mã packing list 4', 'field': 'pkl_4__packing_list_code'},
        {'name': 'Số lượng lô 4', 'field': 'quantity_batch_4'},
        {'name': 'HAWB 4', 'field': 'hawb_4__bill_code'},
        {'name': 'Số hóa đơn 5', 'field': 'inv_5__invoice_number'},
        {'name': 'Mã packing list 5', 'field': 'pkl_5__packing_list_code'},
        {'name': 'Số lượng lô 5', 'field': 'quantity_batch_5'},
        {'name': 'HAWB 5', 'field': 'hawb_5__bill_code'},
        {'name': 'Số lượng chưa về', 'field': 'quantity_pending'},
        {'name': 'Ghi chú', 'field': 'note'},
    ]

    hidden_fields = [
        {'name': 'page', 'value': order_list.number},
        {'name': 'sort', 'value': sort_by},
        {'name': 'order', 'value': sort_order},
        {'name': 'items_per_page', 'value': items_per_page},
        {'name': 'year_main', 'value': ",".join(map(str, selected_years_main)) if selected_years_main else ''},
        {'name': 'product_type', 'value': ",".join(map(str, selected_product_types)) if selected_product_types else ''},
        {'name': 'order_status', 'value': ",".join(map(str, selected_order_status)) if selected_order_status else ''},
        {'name': 'search_main', 'value': search_query_main}
    ]

    query_params = {
        'sort': sort_by,
        'order': sort_order,
        'items_per_page': items_per_page,
        'year_main': ",".join(map(str, selected_years_main)) if selected_years_main else '',
        'product_type': ",".join(map(str, selected_product_types)) if selected_product_types else '',
        'order_status': ",".join(map(str, selected_order_status)) if selected_order_status else '',
        'search_main': search_query_main,
    }
    filtered_query_params = {k: v for k, v in query_params.items() if v}
    base_pagination_url = f"&{urlencode(filtered_query_params)}"

    return render(request, 'Order.html', {
        'list': order_list,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'items_per_page': items_per_page,
        'selected_years_main': selected_years_main,
        'available_years': available_years,
        'available_product_types': available_product_types,
        'selected_product_types': selected_product_types,
        'available_statuses': available_statuses,
        'selected_order_status': selected_order_status,
        'search_main': search_query_main,
        'yearly_totals': yearly_totals,
        'columns': columns,
        'hidden_fields': hidden_fields,
        'base_pagination_url': base_pagination_url,
    })
