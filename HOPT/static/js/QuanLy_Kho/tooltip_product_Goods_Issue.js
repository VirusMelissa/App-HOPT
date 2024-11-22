document.addEventListener('DOMContentLoaded', function () {
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
        // console.log("Warehouse:", warehouseId, "Product:", productId); kiểm tra dữ liệu

        const quantityAvailable = (totalQuantities[warehouseId] && totalQuantities[warehouseId][productId]) || 0;

        availableQuantityInput.value = quantityAvailable;

        quantityInput.value = '';
    }

    // Vì dùng select2 nên không thể dùng theo này productSelect.addEventListener('change', updateAvailableQuantity);
    // Sự kiện thay đổi mã hàng và mã kho
    $(productSelect).on('change', updateAvailableQuantity);
    $(warehouseSelect).on('change', updateAvailableQuantity);
    updateAvailableQuantity();

    const inputs = document.querySelectorAll('.form-group input, .form-group select');
    const form = document.getElementById('form');

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
