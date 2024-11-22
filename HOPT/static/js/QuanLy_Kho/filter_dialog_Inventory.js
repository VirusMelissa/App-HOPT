window.onload = function() {
    loadSavedFilters(); // Gọi hàm load filter đã lưu từ localStorage khi load trang
};

function loadSavedFilters() {
    try {
        const savedProductTypes = JSON.parse(localStorage.getItem('selectedProductTypes')) || [];
        const savedWarehouses = JSON.parse(localStorage.getItem('selectedWarehouses')) || [];
        
        // Tick chọn các giá trị năm và loại hàng đã lưu trước đó
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
        localStorage.removeItem('selectedProductTypes');
        localStorage.removeItem('selectedWarehouses');
    }
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


function closeProductTypeDialog() {
    document.getElementById('productTypeDialog').style.display = "none";
}

function closeWarehouseDialog() {
    document.getElementById('warehouseDialog').style.display = "none";
}

function closeClearFiltersDialog() {
    document.getElementById('clearFiltersDialog').style.display = "none";
}

function filterProductTypes() {
    const input = document.getElementById('productTypeFilterInput');
    const filter = input.value.toUpperCase();
    const items = document.querySelectorAll('.product-type-item');

    items.forEach(item => {
        const label = item.textContent || item.innerText; // Lấy nội dung văn bản trực tiếp từ item
        item.style.display = label.toUpperCase().includes(filter) ? "" : "none";
    });
}

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
    if (filterType === 'productType') {
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
    if (filterType === 'productType') {
        urlParams.delete('product_type');  // Xóa bộ lọc Loại hàng
    } else if (filterType === 'warehouse') {
        urlParams.delete('warehouse');  // Xóa bộ lọc Kho
    } else if (filterType === 'all') {
        // Xóa toàn bộ các bộ lọc
        urlParams.delete('product_type');
        urlParams.delete('warehouse');
    }

    // Cập nhật URL mà không làm mất các tham số lọc còn lại
    window.location.search = urlParams.toString();
}


function applyFilters(event, filterType) {
    event.preventDefault();

    // Lấy các giá trị đã lưu trong localStorage
    let selectedProductTypes = JSON.parse(localStorage.getItem('selectedProductTypes')) || [];
    let selectedWarehouses = JSON.parse(localStorage.getItem('selectedWarehouses')) || [];
    
    if (filterType === 'productType') {
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

