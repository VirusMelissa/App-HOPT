// Thêm biến theo dõi trạng thái
let isYearFilterApplied = false; // Đánh dấu liệu bộ lọc năm đã được áp dụng hay chưa
let isProductTypeFilterApplied = false; // Đánh dấu liệu bộ lọc loại hàng đã được áp dụng hay chưa

// Hàm này sẽ được gọi khi trang được tải
window.onload = function() {
    // Kiểm tra xem có giá trị nào trong localStorage không
    const savedYears = JSON.parse(localStorage.getItem('selectedYears')) || [];
    const savedProductTypes = JSON.parse(localStorage.getItem('selectedProductTypes')) || [];

    // Xử lý tick chọn cho các checkbox dựa vào bộ lọc đã lưu
    tickSavedCheckboxes(savedYears, savedProductTypes);
};

// Xóa bộ nhớ lưu trữ của nút "Lưu" khi tải lại trang bằng F5 hoặc Enter
window.addEventListener('beforeunload', function(event) {
    if (!isYearFilterApplied) {
        localStorage.removeItem('selectedYears');
    }
    if (!isProductTypeFilterApplied) {
        localStorage.removeItem('selectedProductTypes');
    }
});

// Hàm tick chọn cho các checkbox đã lưu
function tickSavedCheckboxes(savedYears, savedProductTypes) {
    const yearCheckboxes = document.querySelectorAll('#yearForm input[name="year_main"]');
    yearCheckboxes.forEach(checkbox => {
        // Tick chọn nếu bộ lọc năm đã lưu hoặc tick tất cả nếu không có giá trị lưu
        checkbox.checked = savedYears.length === 0 || savedYears.includes(checkbox.value);
    });

    const productTypeCheckboxes = document.querySelectorAll('#productTypeForm input[name="product_types"]');
    productTypeCheckboxes.forEach(checkbox => {
        // Tick chọn nếu bộ lọc loại hàng đã lưu hoặc tick tất cả nếu không có giá trị lưu
        checkbox.checked = savedProductTypes.length === 0 || savedProductTypes.includes(checkbox.value);
    });
}

function openYearDialog() {
    const dialog = document.getElementById('yearDialog');
    const button = document.getElementById('yearButton');
    positionDialog(dialog, button);
    dialog.style.display = "block";
}

function openProductTypeDialog() {
    const dialog = document.getElementById('productTypeDialog');
    const button = document.getElementById('productTypeButton');
    positionDialog(dialog, button);
    dialog.style.display = "block";
}

function closeYearDialog() {
    document.getElementById('yearDialog').style.display = "none";
}

function closeProductTypeDialog() {
    document.getElementById('productTypeDialog').style.display = "none";
}

// Lưu bộ lọc năm vào localStorage
function saveYearSelection() {
    const selectedYears = Array.from(document.querySelectorAll('#yearForm input[name="year_main"]:checked'))
        .map(input => input.value);
    localStorage.setItem('selectedYears', JSON.stringify(selectedYears));
    isYearFilterApplied = true; // Đánh dấu rằng bộ lọc năm đã được áp dụng
    closeYearDialog();
}

// Lưu bộ lọc loại hàng vào localStorage
function saveProductTypeSelection() {
    const selectedProductTypes = Array.from(document.querySelectorAll('#productTypeForm input[name="product_types"]:checked'))
        .map(input => input.value);
    localStorage.setItem('selectedProductTypes', JSON.stringify(selectedProductTypes));
    isProductTypeFilterApplied = true; // Đánh dấu rằng bộ lọc loại hàng đã được áp dụng
    closeProductTypeDialog();
}

function positionDialog(dialog, button) {
    const rect = button.getBoundingClientRect();
    dialog.style.top = `${rect.bottom + window.scrollY}px`;
    dialog.style.left = `${rect.left + window.scrollX}px`;
}

function filterYears() {
    const input = document.getElementById('yearFilterInput');
    const filter = input.value.toUpperCase();
    const items = document.querySelectorAll('.year-item');
    items.forEach(item => {
        const label = item.querySelector('label').textContent;
        item.style.display = label.toUpperCase().includes(filter) ? "" : "none";
    });
}

function filterProductTypes() {
    const input = document.getElementById('productTypeFilterInput');
    const filter = input.value.toUpperCase();
    const items = document.querySelectorAll('.product-type-item');
    items.forEach(item => {
        const label = item.querySelector('label').textContent;
        item.style.display = label.toUpperCase().includes(filter) ? "" : "none";
    });
}

// Khi người dùng bấm "Lưu bộ lọc"
document.getElementById('submitButton').addEventListener('click', function(event) {
    event.preventDefault();
    applyFilters();
});

function applyFilters() {
    // Lấy các giá trị từ localStorage
    const selectedYears = JSON.parse(localStorage.getItem('selectedYears')) || [];
    const selectedProductTypes = JSON.parse(localStorage.getItem('selectedProductTypes')) || [];

    // Kiểm tra xem có ít nhất một bộ lọc được áp dụng không
    if (selectedYears.length > 0 || selectedProductTypes.length > 0) {
        isYearFilterApplied = true;
        isProductTypeFilterApplied = true;
    }

    // Tạo URL với các tham số đã có trước đó và thêm năm, loại sản phẩm vào
    const urlParams = new URLSearchParams(window.location.search);

    // Giữ lại các tham số đã có trên URL
    const formElements = document.getElementById('filterForm').elements;
    for (const element of formElements) {
        if (element.name && element.type === 'hidden' && element.value) {
            urlParams.set(element.name, element.value);
        }
    }

    // Thêm các giá trị bộ lọc mới
    if (selectedYears.length > 0) {
        urlParams.set('year_main', selectedYears.join(','));
    } else {
        urlParams.delete('year_main');
    }

    if (selectedProductTypes.length > 0) {
        urlParams.set('product_type', selectedProductTypes.join(','));
    } else {
        urlParams.delete('product_type');
    }

    // Chuyển hướng đến URL mới
    window.location.search = urlParams.toString();
}
