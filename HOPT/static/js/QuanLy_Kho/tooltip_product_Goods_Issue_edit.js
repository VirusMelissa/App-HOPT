document.addEventListener('DOMContentLoaded', function () {
    // Chạy lại khi DOM đã được tải
    $('select.select-field').select2({
        placeholder: 'Chọn một giá trị',
        allowClear: true
    });

    $('select.select-field-customers').select2({
        placeholder: 'Chọn một giá trị',
        allowClear: true
    });

    let totalQuantities = {};

    try {
        const totalQuantitiesElement = document.getElementById("total_quantities");
        if (totalQuantitiesElement) {
            totalQuantities = JSON.parse(totalQuantitiesElement.textContent);
            console.log("Dữ liệu totalQuantities:", totalQuantities);
        } else {
            console.error("không tìm thấy phần tử total_quantities.");
        }
    } catch (error) {
        console.error("Lỗi khi phân tích cú pháp JSON:", error.message);
    }

    const productSelect = document.getElementById('products');
    const warehouseSelect = document.getElementById('warehouse');
    const availableQuantityInput = document.getElementById('available_quantity');
    const quantityInput = document.getElementById('quantity');

    function updateAvailableQuantity() {
        const warehouseId = warehouseSelect.value;
        const productId = productSelect.value;

        // Lấy số lượng còn lại từ totalQuantities
        const quantityAvailable = (totalQuantities[warehouseId] && totalQuantities[warehouseId][productId]) || 0;

        // Lấy số lượng cần xuất (có thể đã có giá trị)
        const quantityToIssue = parseInt(quantityInput.value, 10) || 0;

        // Cập nhật lại số lượng còn lại
        availableQuantityInput.value = quantityAvailable + quantityToIssue;

        // Nếu cần, reset lại số lượng cần xuất nếu nó không hợp lệ
        if (!quantityInput.value || parseInt(quantityInput.value, 10) > availableQuantityInput.value) {
            quantityInput.value = '';  // Chỉ đặt lại nếu cần
        }
    }

    // Cập nhật số lượng khi thay đổi sản phẩm hoặc kho
    $(productSelect).on('change', updateAvailableQuantity);
    $(warehouseSelect).on('change', updateAvailableQuantity);

    updateAvailableQuantity();  // Cập nhật ngay khi trang được tải

    const inputs = document.querySelectorAll('.form-group input, .form-group select');
    const form = document.getElementById('form');

    // Xử lý tooltip và validate
    inputs.forEach(input => {
        const tooltip = input.nextElementSibling;

        validateInput(input, tooltip);

        input.addEventListener('focus', () => {
            validateInput(input, tooltip);
        });

        input.addEventListener('input', () => {
            validateInput(input, tooltip);
        });
    });

    form.addEventListener('submit', (event) => {
        let hasError = false;
        inputs.forEach(input => {
            const tooltip = input.nextElementSibling;
            validateInput(input, tooltip);
            if (tooltip.classList.contains('show')) {
                hasError = true;
            }
        });

        if (hasError) {
            event.preventDefault();
        }
    });

    function validateInput(input, tooltip) {
        const value = input.value.trim();
        let errorMessage = '';

        switch (input.name) {
            case 'quantity':
                const availableQuantity = parseInt(availableQuantityInput.value, 10) || 0;
                if (!value) {
                    errorMessage = 'Số lượng không được để trống.';
                } else if (isNaN(value) || value <= 0) {
                    errorMessage = 'Số lượng phải là một số dương.';
                } else if (parseInt(value, 10) > availableQuantity) {
                    errorMessage = 'Số lượng không được lớn hơn số lượng hiện tại trong kho.';
                }
                break;
            case 'issue_date':
                if (!value) {
                    errorMessage = 'Ngày xuất không được để trống.';
                }
                break;
        }

        if (tooltip) {
            if (errorMessage) {
                tooltip.querySelector('.tooltip-text').textContent = errorMessage;
                tooltip.classList.add('show');
            } else {
                tooltip.classList.remove('show');
            }
        }
    }
});
