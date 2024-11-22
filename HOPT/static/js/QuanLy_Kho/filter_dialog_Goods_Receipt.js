window.onload = function() {
    loadSavedFilters(); // Gọi hàm load filter đã lưu từ localStorage khi load trang
};

function loadSavedFilters() {
    try {
        const savedYears = JSON.parse(localStorage.getItem('selectedYears')) || [];
        const savedProductTypes = JSON.parse(localStorage.getItem('selectedProductTypes')) || [];
        const savedWarehouses = JSON.parse(localStorage.getItem('selectedWarehouses')) || [];
        
        // Tick chọn các giá trị năm và loại hàng đã lưu trước đó
        savedYears.forEach(year => {
            const checkbox = document.querySelector(`#yearForm input[value="${year}"]`);
            if (checkbox) checkbox.checked = true;
        });

        savedProductTypes.forEach(type => {
            const checkbox = document.querySelector(`#productTypeForm input[value="${type}"]`);
            if (checkbox) checkbox.checked = true;
        });

        savedWarehouses.forEach(type => {
            const checkbox = document.querySelector(`#warehouseForm input[value="${type}"]`);
            if (checkbox) checkbox.checked = true;
        });
    } catch (error) {
        console.error("Error loading saved filters:", error);
        localStorage.removeItem('selectedYears');
        localStorage.removeItem('selectedProductTypes');
        localStorage.removeItem('selectedWarehouses');
    }
}

function openYearDialog() {
    const button = document.getElementById('yearButton');
    const dialog = document.getElementById('yearDialog');
    const rect = button.getBoundingClientRect();
    dialog.style.top = `${rect.bottom + window.scrollY}px`;
    dialog.style.left = `${rect.left + window.scrollX}px`;
    dialog.style.display = 'block';
}

function openProductTypeDialog() {
    const button = document.getElementById('productTypeButton');
    const dialog = document.getElementById('productTypeDialog');
    const rect = button.getBoundingClientRect();
    dialog.style.top = `${rect.bottom + window.scrollY}px`;
    dialog.style.left = `${rect.left + window.scrollX}px`;
    dialog.style.display = 'block';
}

function openWarehouseDialog() {
    const button = document.getElementById('warehouseButton');
    const dialog = document.getElementById('warehouseDialog');
    const rect = button.getBoundingClientRect();
    dialog.style.top = `${rect.bottom + window.scrollY}px`;
    dialog.style.left = `${rect.left + window.scrollX}px`;
    dialog.style.display = 'block';
}

function openClearFiltersDialog() {
    const button = document.getElementById('clearFiltersButton');
    const dialog = document.getElementById('clearFiltersDialog');
    const rect = button.getBoundingClientRect();
    dialog.style.top = `${rect.bottom + window.scrollY}px`;
    dialog.style.left = `${rect.left + window.scrollX}px`;
    dialog.style.display = 'block';
}

function closeYearDialog() {
    document.getElementById('yearDialog').style.display = "none";
}

function closeProductTypeDialog() {
    document.getElementById('productTypeDialog').style.display = "none";
}

function closeWarehouseDialog() {
    document.getElementById('warehouseDialog').style.display = "none";
}

function closeClearFiltersDialog() {
    document.getElementById('clearFiltersDialog').style.display = "none";
}

// Tính năng tìm kiếm Năm
function filterYears() {
    const input = document.getElementById('yearFilterInput');
    const filter = input.value.toUpperCase();
    const items = document.querySelectorAll('.year-item');

    items.forEach(item => {
        const label = item.textContent || item.innerText;
        item.style.display = label.toUpperCase().includes(filter) ? "" : "none";
    });
}

// Tính năng tìm kiếm Loại hàng
function filterProductTypes() {
    const input = document.getElementById('productTypeFilterInput');
    const filter = input.value.toUpperCase();
    const items = document.querySelectorAll('.product-type-item');

    items.forEach(item => {
        const label = item.textContent || item.innerText; // Lấy nội dung văn bản trực tiếp từ item
        item.style.display = label.toUpperCase().includes(filter) ? "" : "none";
    });
}

// Tính năng tìm kiếm kho hàng
function filterWarehouses() {
    const input = document.getElementById('warehouseFilterInput');
    const filter = input.value.toUpperCase();
    const items = document.querySelectorAll('.warehouse-item');

    items.forEach(item => {
        const label = item.textContent || item.innerText; // Lấy nội dung văn bản trực tiếp từ item
        item.style.display = label.toUpperCase().includes(filter) ? "" : "none";
    });
}

function clearFilter(filterType) {
    if (filterType === 'year') {
        // Bỏ chọn tất cả các checkbox của bộ lọc "Năm"
        document.querySelectorAll('#yearForm input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        localStorage.removeItem('selectedYears');
    } else if (filterType === 'productType') {
        // Bỏ chọn tất cả các checkbox của bộ lọc "Loại hàng"
        document.querySelectorAll('#productTypeForm input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        localStorage.removeItem('selectedProductTypes');
    } else if (filterType === 'warehouse') {
        // Bỏ chọn tất cả các checkbox của bộ lọc "Kho"
        document.querySelectorAll('#warehouseForm input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        localStorage.removeItem('selectedWarehouses');
    } else if (filterType === 'all') {
        // Bỏ chọn tất cả các bộ lọc
        document.querySelectorAll('.dialog-content input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        localStorage.removeItem('selectedYears');
        localStorage.removeItem('selectedProductTypes');
        localStorage.removeItem('selectedWarehouses');
    }

    // Cập nhật URL và đóng hộp thoại sau khi xóa bộ lọc
    applyFiltersAfterClearing(filterType);
    closeClearFiltersDialog();
}

function applyFiltersAfterClearing(filterType) {
    // Lấy URL hiện tại
    const urlParams = new URLSearchParams(window.location.search);

    // Xóa các tham số tương ứng theo loại bộ lọc
    if (filterType === 'year') {
        urlParams.delete('year_main');  // Xóa bộ lọc Năm
    } else if (filterType === 'productType') {
        urlParams.delete('product_type');  // Xóa bộ lọc Loại hàng
    } else if (filterType === 'warehouse') {
        urlParams.delete('warehouse');  // Xóa bộ lọc Kho
    } else if (filterType === 'all') {
        // Xóa toàn bộ các bộ lọc
        urlParams.delete('year_main');
        urlParams.delete('product_type');
        urlParams.delete('warehouse');
    }

    // Cập nhật URL mà không làm mất các tham số lọc còn lại
    window.location.search = urlParams.toString();
}


function applyFilters(event, filterType) {
    event.preventDefault();

    // Lấy các giá trị đã lưu trong localStorage
    let selectedYears = JSON.parse(localStorage.getItem('selectedYears')) || [];
    let selectedProductTypes = JSON.parse(localStorage.getItem('selectedProductTypes')) || [];
    let selectedWarehouses = JSON.parse(localStorage.getItem('selectedWarehouses')) || [];
    
    if (filterType === 'year') {
        const checkedYears = Array.from(document.querySelectorAll('#yearForm input:checked')).map(input => input.value);
        selectedYears = [...new Set(checkedYears)];
        localStorage.setItem('selectedYears', JSON.stringify(selectedYears));
        closeYearDialog();
    } else if (filterType === 'productType') {
        const checkedProductTypes = Array.from(document.querySelectorAll('#productTypeForm input:checked')).map(input => input.value);
        selectedProductTypes = [...new Set(checkedProductTypes)];
        localStorage.setItem('selectedProductTypes', JSON.stringify(selectedProductTypes));
        closeProductTypeDialog();
    } else if (filterType === 'warehouse') {
        const checkedWarehouses = Array.from(document.querySelectorAll('#warehouseForm input:checked')).map(input => input.value);
        selectedWarehouses = [...new Set(checkedWarehouses)];
        localStorage.setItem('selectedWarehouses', JSON.stringify(selectedWarehouses));
        closeWarehouseDialog();
    }

    // Cập nhật URL
    const urlParams = new URLSearchParams(window.location.search);
    const formElements = document.getElementById('filterForm').elements;
    for (const element of formElements) {
        if (element.name && element.type === 'hidden' && element.value) {
            urlParams.set(element.name, element.value);
        }
    }

    // Thêm mảng `selectedYears` và `selectedProductTypes` vào URL dưới dạng chuỗi phân tách bằng dấu phẩy
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

    if (selectedWarehouses.length > 0) {
        urlParams.set('warehouse', selectedWarehouses.join(','));
    } else {
        urlParams.delete('warehouse');
    }

    // Cập nhật URL trình duyệt
    window.location.search = urlParams.toString();
}

