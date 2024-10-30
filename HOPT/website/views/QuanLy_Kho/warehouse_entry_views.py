from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from website.models import Warehouse_Entries, Suppliers, Bills, Contracts, Products, Product_Type, Warehouse_Receipts
from .warehouse_utils import get_filter_parameters, get_sorted_warehouse_list, get_yearly_totals
from django.db.models.functions import ExtractYear
from django.contrib import messages
from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect

def is_authorized(user):
    return user.role in ['warehouse_staff', 'admin']

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')  # Đổi redirect tới hàm unauthorized_access
def Warehouse_View(request):
    # Lấy các tham số tìm kiếm và lọc của main-content
    search_query_main, sort_by, sort_order, items_per_page, selected_years_main, selected_product_types = get_filter_parameters(request)

    # Lấy tham số tìm kiếm của sub-content
    search_query_sub = request.GET.get('search_sub', '')

    # Lấy tất cả các năm và loại hàng nếu không có bộ lọc nào
    available_years = Warehouse_Entries.objects.annotate(
        year=ExtractYear('entry_date')
    ).values_list('year', flat=True).distinct().order_by('-year')

    available_product_types = Product_Type.objects.all()

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
    paginator = get_sorted_warehouse_list(search_query_main, selected_years_main, selected_product_types, sort_by, sort_order, items_per_page)
    page_number = request.GET.get('page')
    warehouse_list = paginator.get_page(page_number)

    # Tính tổng số lượng theo tháng cho sub-content
    yearly_totals = get_yearly_totals(selected_years_sub, search_query_sub)

    return render(request, 'QuanLy_Kho/Warehouse_entry.html', {
        'list': warehouse_list,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'items_per_page': items_per_page,
        'selected_years_main': selected_years_main,
        'available_product_types': available_product_types,
        'selected_product_types': selected_product_types,
        'available_years': available_years,
        'selected_year_sub': selected_years_sub,
        'search_main': search_query_main,
        'search_sub': search_query_sub,  # Đảm bảo chuyển search_sub vào template
        'yearly_totals': yearly_totals,
        'months': range(1, 13)  # Truyền danh sách tháng từ 1 đến 12
    })


@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Add_Product_Warehouse_View(request):
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
        products_id = request.POST.get('products')
        entry_date = request.POST.get('entry_date')
        suppliers_id = request.POST.get('suppliers')
        warehouse_receipts_id = request.POST.get('warehouse_receipts')
        bills_id = request.POST.get('bills')
        contracts_id = request.POST.get('contracts')
        quantity = request.POST.get('quantity')

        try:
            product = Products.objects.get(id=products_id)
            supplier = Suppliers.objects.get(id=suppliers_id)
            warehouse_receipt = Warehouse_Receipts.objects.get(id=warehouse_receipts_id)
            bill = Bills.objects.get(id=bills_id)
            contract = Contracts.objects.get(id=contracts_id)

            # Tìm giá trị số thứ tự lớn nhất hiện tại
            last_stt = Warehouse_Entries.objects.aggregate(max_stt=models.Max('stt'))['max_stt']
            next_stt = (last_stt or 0) + 1  # Nếu không có stt nào, mặc định là 0 và cộng thêm 1

            new_entry = Warehouse_Entries(
                stt=next_stt,  # Đặt giá trị stt tự động
                products=product,
                entry_date=entry_date,
                suppliers=supplier,
                warehouse_receipts=warehouse_receipt,
                bills=bill,
                contracts=contract,
                quantity=quantity
            )
            new_entry.save()

            # Debugging: In ra thông tin redirect
            print(f"Redirecting to warehouse_entry with parameters: page={page_number}, sort={sort_by}, order={sort_order}, "
                  f"items_per_page={items_per_page}, year_sub={selected_years_sub}, year_main={selected_years_main}, "
                  f"product_type={selected_product_types}, search_sub={search_query_sub}, search_main={search_query_main}")

            url = reverse('warehouse_entry')  # Thay 'warehouse_entry' bằng tên URL của bạn nếu khác
            return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&items_per_page={items_per_page}&year_sub={selected_years_sub}&year_main={selected_years_main}&product_type={selected_product_types}&search_sub={search_query_sub}&search_main={search_query_main}")

        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
            print(f'Error occurred: {str(e)}')  # In lỗi ra console

    products = Products.objects.all()
    suppliers = Suppliers.objects.all()
    warehouse_receipts = Warehouse_Receipts.objects.all()
    bills = Bills.objects.all()
    contracts = Contracts.objects.all()
    return render(request, 'QuanLy_Kho/Add_product_warehouse_entry.html', {
        'products': products,
        'suppliers': suppliers,
        'warehouse_receipts': warehouse_receipts,
        'bills': bills,
        'contracts': contracts
    })

@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Edit_Warehouse_Entry_View(request, entry_id):
    entry = get_object_or_404(Warehouse_Entries, id=entry_id)

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
        products_id = request.POST.get('products')
        entry_date = request.POST.get('entry_date')
        suppliers_id = request.POST.get('suppliers')
        warehouse_receipts_id = request.POST.get('warehouse_receipts')
        bills_id = request.POST.get('bills')
        contracts_id = request.POST.get('contracts')
        quantity = request.POST.get('quantity')

        # print(f"POST data: products_id={products_id}, entry_date={entry_date}, suppliers_id={suppliers_id}, "
        #      f"warehouse_receipts_id={warehouse_receipts_id}, bills_id={bills_id}, contracts_id={contracts_id}, quantity={quantity}")

        try:
            product = Products.objects.get(id=products_id)
            supplier = Suppliers.objects.get(id=suppliers_id)
            warehouse_receipt = Warehouse_Receipts.objects.get(id=warehouse_receipts_id)
            bill = Bills.objects.get(id=bills_id)
            contract = Contracts.objects.get(id=contracts_id)

            entry.products = product
            entry.entry_date = entry_date
            entry.suppliers = supplier
            entry.warehouse_receipts = warehouse_receipt
            entry.bills = bill
            entry.contracts = contract
            entry.quantity = quantity
            entry.save()

            url = reverse('warehouse_entry')  # Thay 'warehouse_entry' bằng tên URL của bạn nếu khác
            return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&items_per_page={items_per_page}&year_sub={selected_years_sub}&year_main={selected_years_main}&product_type={selected_product_types}&search_sub={search_query_sub}&search_main={search_query_main}")
        except Exception as e:
            print(f"Error: {str(e)}")
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')

    products = Products.objects.all()
    suppliers = Suppliers.objects.all()
    warehouse_receipts = Warehouse_Receipts.objects.all()
    bills = Bills.objects.all()
    contracts = Contracts.objects.all()
    return render(request, 'QuanLy_Kho/Edit_product_warehouse_entry.html', {
        'entry': entry,
        'products': products,
        'suppliers': suppliers,
        'warehouse_receipts': warehouse_receipts,
        'bills': bills,
        'contracts': contracts
    })


@login_required(login_url='login')
@user_passes_test(is_authorized, login_url='unauthorized_access')
def Delete_Warehouse_Entry_View(request, entry_id):
    entry = get_object_or_404(Warehouse_Entries, id=entry_id)

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
        # Lưu lại số thứ tự của entry sẽ bị xóa
        entry_stt = entry.stt

        # Xóa đối tượng khi người dùng xác nhận
        entry.delete()

        # Cập nhật lại số thứ tự cho các mục còn lại
        remaining_entries = Warehouse_Entries.objects.filter(stt__gt=entry_stt).order_by('stt')
        for i, remaining_entry in enumerate(remaining_entries, start=entry_stt):
            remaining_entry.stt = i
            remaining_entry.save()

        url = reverse('warehouse_entry')  # Thay 'warehouse_entry' bằng tên URL của bạn nếu khác
        return HttpResponseRedirect(f"{url}?page={page_number}&sort={sort_by}&order={sort_order}&items_per_page={items_per_page}&year_sub={selected_years_sub}&year_main={selected_years_main}&product_type={selected_product_types}&search_sub={search_query_sub}&search_main={search_query_main}")

    # Nếu là GET, hiển thị trang xác nhận xóa
    return render(request, 'QuanLy_Kho/confirm_delete_warehouse_entry.html', {'entry': entry})


